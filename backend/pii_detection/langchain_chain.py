
from .deepseek_client import deepseek_detect

def langchain_deepseek_chain(text, knowledge_base_prompt=None):
    """
    用 LangChain 构建 prompt，调用 deepseek 检测。
    """
    # knowledge_base_prompt 必须为知识库拼接好的内容
    prompt = knowledge_base_prompt or "请结合医疗敏感个人信息相关法律法规和标准进行识别。"
    full_prompt = f"请严格按照以下知识库规则识别医疗敏感个人信息：\n{prompt}\n待检测文本：{text}"
    # 这里用 deepseek_detect 作为 LLM 调用
    result = deepseek_detect(text, full_prompt)
    return result
