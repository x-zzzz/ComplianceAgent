from .langchain_chain import langchain_deepseek_chain

def detect_pii_and_risk(text, knowledge_base_prompt=None):
    """
    用 LangChain 构建 prompt，调用 deepseek 检测。
    返回格式需与前端兼容：{"entities": [...], "risk_level": ...}
    """
    result = langchain_deepseek_chain(text, knowledge_base_prompt)
    # 适配 deepseek 返回格式
    if isinstance(result, dict) and "entities" in result and "risk_level" in result:
        return result
    return {
        "entities": [],
        "risk_level": "未知",
        "raw_response": result
    }
