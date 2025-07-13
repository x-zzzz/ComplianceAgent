import requests

def analyze_text(text):
    try:
        payload = {
            "text": text,
            "language": "zh",  # 设置为中文
            "entities": [
                "PERSON",            # 人名
                "PHONE_NUMBER",      # 电话号码
                "EMAIL_ADDRESS",     # 电子邮件
                "CREDIT_CARD",       # 信用卡
                "DATE_TIME",         # 日期时间
                "LOCATION",          # 地址位置
                "ORGANIZATION"       # 组织机构
            ],
            "score_threshold": 0.3  # 降低阈值以提高检测灵敏度
        }
        response = requests.post(
            "http://presidio-analyzer:3000/analyze", 
            json=payload,
            timeout=30  # 设置超时时间
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Presidio API 请求失败: {str(e)}")
        return []  # 返回空列表，确保不会影响后续处理

def detect_pii_with_presidio(text):
    """
    使用 Presidio 检测文本中的 PII 信息
    """
    try:
        entities = analyze_text(text)
        
        if not entities:
            return {
                "text": text,
                "summary": {
                    "risk_level": "低",
                    "total_entities": 0,
                    "overall_reason": "未检测到敏感信息"
                },
                "details": []
            }

        # 简单的风险评估逻辑
        total_entities = len(entities)
        high_risk_entities = ["CREDIT_CARD", "MEDICAL_LICENSE", "PATIENT_ID"]
        medium_risk_entities = ["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS"]
        
        entity_groups = {}
        for entity in entities:
            entity_type = entity.get("entity_type", "UNKNOWN")
            if entity_type not in entity_groups:
                entity_groups[entity_type] = []
            entity_groups[entity_type].append(entity.get("text", ""))

        # 确定风险等级
        risk_level = "低"
        if any(entity.get("entity_type") in high_risk_entities for entity in entities):
            risk_level = "高"
        elif any(entity.get("entity_type") in medium_risk_entities for entity in entities):
            risk_level = "中"

        # 生成详细信息
        details = []
        for entity_type, texts in entity_groups.items():
            detail_risk = "高" if entity_type in high_risk_entities else \
                         "中" if entity_type in medium_risk_entities else "低"
            
            details.append({
                "entities": texts,
                "risk_level": detail_risk,
                "reason": f"发现{len(texts)}处{entity_type}类型的敏感信息"
            })

        return {
            "text": text,
            "summary": {
                "risk_level": risk_level,
                "total_entities": total_entities,
                "overall_reason": f"总共发现{total_entities}处敏感信息，包括" + 
                                ", ".join(f"{len(v)}处{k}" for k, v in entity_groups.items())
            },
            "details": details
        }
        
    except Exception as e:
        print(f"Presidio 检测过程发生错误: {str(e)}")
        # 发生错误时返回一个基本的响应
        return {
            "text": text,
            "summary": {
                "risk_level": "未知",
                "total_entities": 0,
                "overall_reason": f"检测过程发生错误: {str(e)}"
            },
            "details": []
        }
