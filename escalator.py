ESCALATION_KEYWORDS = [
    "system down", "crash", "not working", "outage",
    "refund", "charged twice", "payment failed",
    "integration issue", "global", "everyone", "production"
]

def check_escalation(persona: str, message: str, intent: str, conversation_history: list) -> bool:
    """
    Determine if issue should be escalated to human agent.
    """
    message_lower = message.lower()
    if any(keyword in message_lower for keyword in ESCALATION_KEYWORDS):
        return True
    # Immediate escalation keywords
    urgent_keywords = ["legal", "lawsuit", "attorney", "lawyer", "sue", "complaint", "regulatory"]
    if any(keyword in message_lower for keyword in urgent_keywords):
        return True
    
    # Frustrated user with repeated issues
    if persona == "frustrated user":
        # Check if user has mentioned the same issue multiple times
        if conversation_history and len(conversation_history) >= 3:
            recent_intents = [chat.get('intent') for chat in conversation_history[-3:]]
            if recent_intents.count(intent) >= 2:  # Same issue mentioned twice
                return True
    
    # High-value business issues
    if persona == "business executive" and intent in ["billing_dispute", "integration_issue"]:
        return True
    
    # Technical issues that persist
    if persona == "technical expert" and intent == "api_error":
        if conversation_history and len(conversation_history) >= 2:
            return True
    
    # Explicit escalation request
    if any(phrase in message_lower for phrase in ["speak to human", "talk to agent", "escalate", "manager", "supervisor"]):
        return True
    
    return False


def escalate_to_human(message: str, persona: str, intent: str, conversation_history: list) -> dict:
    """
    Escalate to appropriate human agent.
    """
    # Route based on intent and persona
    if intent in ["billing_dispute", "payment_issue"]:
        team = "Billing Team"
        agent = "Sarah (Billing Specialist)"
    elif intent in ["api_error", "integration_issue"] or persona == "technical expert":
        team = "Technical Support"
        agent = "Mike (Senior Engineer)"
    elif persona == "business executive":
        team = "Account Management"
        agent = "Jennifer (Account Manager)"
    else:
        team = "General Support"
        agent = "Alex (Support Specialist)"
    
    # Build escalation summary
    summary = f"Issue: {intent}\nCustomer Type: {persona}\n"
    summary += f"Last Message: {message[:200]}\n"
    
    if conversation_history:
        summary += f"\nConversation Length: {len(conversation_history)} exchanges\n"
    
    return {
        "assigned_to": agent,
        "team": team,
        "priority": "high" if persona == "frustrated user" else "medium",
        "summary": summary,
        "estimated_response": "within 30 minutes"
    }
