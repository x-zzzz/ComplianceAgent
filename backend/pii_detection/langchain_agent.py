from .langchain_chain import langchain_deepseek_chain
import re
import json
import os
from .knowledge_utils import load_knowledge_base

# 新增：知识库结构化加载（兼容容器/本地）
KB_PATH = os.path.join(os.path.dirname(__file__), '../knowledge_base/PIIquestion.json')
with open(KB_PATH, 'r', encoding='utf-8') as f:
    KB_DATA = json.load(f)

def find_reason_from_kb(entity_text):
    """
    根据实体内容在知识库中查找最相关的原因（answer/正向上下文）。
    简单实现：遍历知识库，若实体内容与问题/正向上下文/答案有高相关性则返回。
    """
    for item in KB_DATA:
        # 直接包含或高相关性
        if any(entity_text in (item.get('question', '') + ' '.join([ctx['content'] for ctx in item.get('positive_contexts', [])]) + ' '.join(item.get('answer', []))) for _ in [0]):
            return '\n'.join(item.get('answer', []))
    # fallback: 返回第一个定义
    return KB_DATA[0]['answer'][0] if KB_DATA and 'answer' in KB_DATA[0] else "详见知识库"

def find_overall_reason(risk_level):
    """
    根据整体风险等级，返回知识库中最相关的合规风险说明。
    """
    # 简单实现：找“风险”或“敏感”相关定义
    for item in KB_DATA:
        if '敏感个人信息' in item.get('question', ''):
            return '\n'.join(item.get('answer', []))
    return "详见知识库"

def detect_pii_and_risk(text, knowledge_base_prompt=None):
    """
    用 LangChain 构建 prompt，调用 deepseek 检测。
    只返回 deepseek 的原始 JSON 结构（summary/details），便于前端直接展示。
    """
    result = langchain_deepseek_chain(text, knowledge_base_prompt)
    # 如果 deepseek 返回 summary/details 结构，直接返回
    if isinstance(result, dict) and "summary" in result and "details" in result:
        return result
    # 否则 fallback 旧逻辑
    # 解析 deepseek 返回的 content 字段
    details = []
    all_entities = []
    risk_levels = []
    content = None
    if isinstance(result, dict):
        content = result.get("content")
        if not content and "raw_response" in result and isinstance(result["raw_response"], dict):
            content = result["raw_response"].get("content")
    if content:
        sections = re.split(r"\n\s*\d+\. ", "\n" + content)
        for section in sections:
            if not section.strip():
                continue
            risk_match = re.search(r"风险等级[：:][\s]*([高中低未知]+)", section)
            risk = risk_match.group(1) if risk_match else "未知"
            risk_levels.append(risk)
            lines = [l for l in section.split("\n") if l.strip() and not l.strip().startswith("**风险等级**") and "风险等级" not in l]
            entities = []
            for line in lines:
                if ":" in line or "：" in line:
                    clean_line = re.sub(r"\*\*|\*", "", line).strip()
                    entities.append(clean_line)
                    all_entities.append(clean_line)
            # 为每条实体查找知识库原因
            reason = find_reason_from_kb(' '.join(entities)) if entities else "详见知识库"
            details.append({
                "entities": entities,
                "risk_level": risk,
                "reason": reason
            })
    # 取最高风险等级，不能为未知，优先级：高>中>低>未知
    level_order = {"高": 3, "中": 2, "低": 1, "未知": 0}
    final_level = "未知"
    filtered_levels = [r for r in risk_levels if r in ("高", "中", "低")]
    if filtered_levels:
        final_level = max(filtered_levels, key=lambda x: level_order.get(x, 0))
    elif risk_levels:
        final_level = max(risk_levels, key=lambda x: level_order.get(x, 0))
    # 总体原因
    overall_reason = find_overall_reason(final_level)
    return {
        "total_entities": len(all_entities),
        "risk_level": final_level,
        "overall_reason": overall_reason,
        "details": details,
        "raw_response": result
    }
