def calculate_risk(intent, entities):
    score = 0
    reasons = []

    # --- Intent base risk ---
    intent_base = {
        'send_money': 30,
        'verify_document': 25,
        'hire_service': 15,
        'airport_transfer': 10,
        'check_status': 0,
    }
    score += intent_base.get(intent, 10)

    # --- Urgency risk ---
    urgency = entities.get('urgency', 'low')
    if urgency == 'high':
        score += 25
        reasons.append('High urgency request')
    elif urgency == 'medium':
        score += 10
        reasons.append('Medium urgency request')

    # --- Amount risk (for money transfers) ---
    amount = entities.get('amount')
    if amount:
        try:
            amount = float(amount)
            if amount > 100000:
                score += 25
                reasons.append('Very large transfer amount')
            elif amount > 50000:
                score += 15
                reasons.append('Large transfer amount')
            elif amount > 10000:
                score += 5
                reasons.append('Moderate transfer amount')
        except (ValueError, TypeError):
            pass

    # --- Document type risk ---
    doc_type = entities.get('document_type', '')
    if doc_type:
        doc_type_lower = str(doc_type).lower()
        if any(word in doc_type_lower for word in ['land', 'title', 'deed', 'property']):
            score += 20
            reasons.append('Land title verification — high risk document')
        elif any(word in doc_type_lower for word in ['id', 'passport', 'certificate']):
            score += 10
            reasons.append('Identity document verification')

    # --- Unknown recipient risk ---
    recipient = entities.get('recipient', '')
    if not recipient or str(recipient).lower() in ['unknown', 'someone', 'person']:
        if intent == 'send_money':
            score += 15
            reasons.append('Recipient not clearly identified')

    # --- Cap at 100 ---
    score = min(score, 100)

    # --- Label ---
    if score >= 60:
        label = 'high'
    elif score >= 35:
        label = 'medium'
    else:
        label = 'low'

    return score, label, reasons