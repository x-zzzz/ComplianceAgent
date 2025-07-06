import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

DEEPSEEK_API_URL = "https://api.deepseek.com"
DEEPSEEK_API_KEY = "sk-e752a0d356314ce1bd5d8d595797340a"  # 如有鉴权需求

def deepseek_detect(text, knowledge_base_prompt=None):
    """
    使用 OpenAI SDK 方式访问 deepseek API。
    knowledge_base_prompt: 拼接好的知识库 prompt
    """
    prompt = text
    if knowledge_base_prompt:
        prompt = f"请严格按照以下知识库规则识别医疗敏感个人信息：\n{knowledge_base_prompt}\n待检测文本：{text}"
    try:
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个医疗敏感个人信息检测助手，请严格根据知识库规则识别文本中的敏感个人信息并输出风险等级。"},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            max_tokens=1024
        )
        # 兼容 OpenAI SDK 返回格式
        return response.choices[0].message.model_dump() if hasattr(response.choices[0].message, 'model_dump') else {"content": response.choices[0].message.content}
    except Exception as e:
        logger.error(f"Deepseek API 调用失败: {e}")
        return {"error": str(e)}
