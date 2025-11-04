import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(token=st.secrets["HF_TOKEN"])

def detect_intent(message: str, conversation_history: list = None) -> str:
    """
    Detects user intent using HuggingFace model with conversation context.
    """
    try:
        # Build context
        context = ""
        if conversation_history:
            context = "Conversation context:\n"
            for chat in conversation_history[-2:]:
                context += f"User: {chat['message']}\nIntent was: {chat.get('intent', 'unknown')}\n"
        
        prompt = f"""{context}

Current message: "{message}"

Classify the intent of this customer support message. Return ONLY ONE of these labels:
- login_issue
- payment_issue
- api_error
- billing_dispute
- feature_request
- performance_issue
- integration_issue
- general_query

Intent:"""

        response = client.text_generation(
            prompt,
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            max_new_tokens=15,
            temperature=0.2
        )
        
        intent = response.strip().lower().replace("_", "_")
        
        # Validate
        valid_intents = ["login_issue", "payment_issue", "api_error", "billing_dispute", 
                        "feature_request", "performance_issue", "integration_issue", "general_query"]
        
        for valid in valid_intents:
            if valid in intent:
                return valid
        
        return fallback_intent_detection(message)
        
    except Exception as e:
        print(f"Intent detection error: {e}")
        return fallback_intent_detection(message)


def fallback_intent_detection(message: str) -> str:
    """Fallback keyword-based intent detection."""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["login", "sign in", "password", "authenticate", "locked"]):
        return "login_issue"
    elif any(word in message_lower for word in ["payment", "card", "declined", "transaction"]):
        return "payment_issue"
    elif any(word in message_lower for word in ["api", "timeout", "504", "500", "error code"]):
        return "api_error"
    elif any(word in message_lower for word in ["charge", "refund", "invoice", "billing"]):
        return "billing_dispute"
    elif any(word in message_lower for word in ["feature", "enhancement", "suggestion", "add"]):
        return "feature_request"
    elif any(word in message_lower for word in ["slow", "latency", "performance", "loading"]):
        return "performance_issue"
    elif any(word in message_lower for word in ["integration", "webhook", "third-party", "connect"]):
        return "integration_issue"
    else:
        return "general_query"
