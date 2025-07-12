import re

def simple_desensitize(text, entities):
    """
    对文本中的敏感实体进行简单脱敏（如用*替换）。
    entities: List[str]，每个为需脱敏的实体。
    """
    if not entities:
        return text
    result = text
    for entity in entities:
        if entity and len(entity) > 1:
            result = re.sub(re.escape(entity), '*' * len(entity), result)
    return result
