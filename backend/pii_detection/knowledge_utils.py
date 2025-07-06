import json
import os

PII_QUESTION_PATH = os.path.join(os.path.dirname(__file__), '../knowledge_base/PIIquestion.json')

def load_knowledge_base():
    """
    加载知识库 JSON 并转为适合大模型的 prompt 片段。
    每条规则格式化为：
    问题：xxx\n权威定义/正向上下文：xxx\n标准答案：xxx\n
    返回拼接后的字符串。
    """
    with open(PII_QUESTION_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    prompt_blocks = []
    for item in data:
        q = item.get('question', '').strip()
        pos_ctx = '\n'.join([ctx['content'] for ctx in item.get('positive_contexts', [])])
        ans = '\n'.join(item.get('answer', []))
        block = f"问题：{q}\n权威定义/正向上下文：{pos_ctx}\n标准答案：{ans}"
        prompt_blocks.append(block)
    return '\n\n'.join(prompt_blocks)
