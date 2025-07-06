import logging
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

DEEPSEEK_API_URL = "https://api.deepseek.com"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")  # 从环境变量读取

# 注意：format字符串中如有大括号需转义
DEEPSEEK_PROMPT_TEMPLATE = '''你是一个医疗敏感个人信息检测助手，请严格根据知识库规则识别文本中的敏感个人信息。\n请以如下JSON格式返回：\n{{\n  "summary": {{\n    "total_entities": 敏感信息总数（整数）, \n    "risk_level": "高|中|低|未知", \n    "overall_reason": "整体风险说明，需简明扼要，引用知识库相关内容"\n  }},\n  "details": [\n    {{\n      "entities": ["实体1", "实体2", ...],\n      "risk_level": "高|中|低|未知",\n      "reason": "该条敏感信息的合规说明，引用知识库相关内容"\n    }},\n    ...\n  ]\n}}\n只返回JSON字符串，不要有多余解释。待检测文本如下：\n{input_text}'''

# 加载 .env 文件
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

def deepseek_detect(text, knowledge_base_prompt=None):
    """
    使用 OpenAI SDK 方式访问 deepseek API。
    knowledge_base_prompt: 拼接好的知识库 prompt
    """
    if knowledge_base_prompt:
        prompt = DEEPSEEK_PROMPT_TEMPLATE.format(input_text=text) + "\n知识库规则如下：\n" + knowledge_base_prompt
    else:
        prompt = DEEPSEEK_PROMPT_TEMPLATE.format(input_text=text)
    try:
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个医疗敏感个人信息检测助手。"},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            max_tokens=2048
        )
        content = response.choices[0].message.content
        # 只提取JSON部分，兼容 markdown 代码块
        try:
            # 去除 markdown 代码块标记
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            content = content.strip('`\n ')
            json_start = content.find('{')
            json_str = content[json_start:]
            result = json.loads(json_str)
            return result
        except Exception as e:
            logger.error(f"Deepseek返回内容非标准JSON: {content}")
            return {"content": content, "error": "非标准JSON", "exception": str(e)}
    except Exception as e:
        logger.error(f"Deepseek API 调用失败: {e}")
        return {"error": str(e)}
