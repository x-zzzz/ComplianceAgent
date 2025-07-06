import json
import os
from .knowledge_utils import PII_QUESTION_PATH

def find_knowledge_explanation(reason):
    """
    根据 overall_reason 关键词，查找知识库中最相关的解释。
    返回 answer 字段内容。
    """
    try:
        with open(PII_QUESTION_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 简单关键词匹配，可根据需要优化为更复杂的相似度匹配
        for item in data:
            if reason and (reason in item.get('question', '') or reason in ''.join(item.get('answer', ''))):
                return '\n'.join(item.get('answer', []))
        # 没有直接命中，返回第一个
        if data:
            return '\n'.join(data[0].get('answer', []))
    except Exception as e:
        return ''
    return ''
