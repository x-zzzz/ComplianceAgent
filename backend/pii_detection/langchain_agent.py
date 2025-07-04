from .presidio_client import analyze_text

def detect_pii_and_risk(text):
    results = analyze_text(text)
    pii_entities = []
    risk_level = "Low"
    for entity in results:
        entity_type = entity.get("entity_type")
        score = entity.get("score", 0)
        # 简单风险分级
        if entity_type in ["CreditCard", "BankAccount", "SSN"]:
            risk_level = "High"
        elif entity_type in ["PhoneNumber", "Email"]:
            risk_level = "Medium"
        pii_entities.append({
            "type": entity_type,
            "start": entity.get("start"),
            "end": entity.get("end"),
            "score": score
        })
    return {
        "entities": pii_entities,
        "risk_level": risk_level
    }
