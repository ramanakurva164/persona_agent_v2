ESCALATION_KEYWORDS = [
    "system down", "crash", "not working", "outage",
    "refund", "charged twice", "payment failed",
    "integration issue", "global", "everyone", "production"
]

def check_escalation(persona, query):
    """Check if escalation is needed."""
    q = query.lower()
    return any(word in q for word in ESCALATION_KEYWORDS)

def escalate_to_human(query, persona):
    """Assign escalation to a specific team."""
    if "technical" in persona:
        assigned = "Engineering Team"
    elif "business" in persona:
        assigned = "Account Manager"
    else:
        assigned = "Customer Support Lead"
    return {"assigned_to": assigned, "query": query}
