# intent_detector.py
def detect_intent(message: str) -> str:
    """
    Detects the main issue topic (intent) from the message.
    Used to carry context between user messages.
    """
    message = message.lower()
    if "login" in message or "sign in" in message:
        return "login_issue"
    elif "password" in message:
        return "password_reset"
    elif "payment" in message or "billing" in message:
        return "billing_issue"
    elif "error" in message or "bug" in message:
        return "technical_issue"
    elif "account" in message or "profile" in message:
        return "account_issue"
    else:
        return "general_query"
