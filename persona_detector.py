import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

# Initialize HuggingFace Inference Client
client = InferenceClient(token=os.getenv("HF_TOKEN"))

def detect_persona(message: str, conversation_history: list = None) -> str:
    """
    Detects customer persona using HuggingFace model with conversation context.
    """
    try:
        # Build context from conversation history
        context = ""
        if conversation_history:
            context = "Previous conversation:\n"
            for chat in conversation_history[-3:]:  # Last 3 exchanges
                context += f"User: {chat['message']}\n"
                context += f"Assistant: {chat['reply'][:100]}...\n"
        
        prompt = f"""{context}

Current message: "{message}"

You are a smart classifier that identifies the persona of a customer based on their message and conversation history.
Possible personas:
1. Technical Expert – uses technical terms, APIs, code, integrations, debugging language
2. Frustrated User – expresses anger, confusion, dissatisfaction, urgency
3. Business Executive – asks about pricing, plans, reports, enterprise solutions, ROI
4. General User – casual query, basic questions

Analyze the current message and conversation context. Return ONLY ONE of these exact labels:
- technical expert
- frustrated user
- business executive
- general user"""

        response = client.text_generation(
            prompt,
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            max_new_tokens=20,
            temperature=0.3
        )
        
        persona = response.strip().lower()
        
        # Validate response
        valid_personas = ["technical expert", "frustrated user", "business executive", "general user"]
        for valid in valid_personas:
            if valid in persona:
                return valid
        
        return fallback_persona_detection(message)
        
    except Exception as e:
        print(f"Persona detection error: {e}")
        return fallback_persona_detection(message)


def fallback_persona_detection(message: str) -> str:
    """Fallback keyword-based persona detection."""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["api", "code", "integration", "sdk", "error", "bug", "technical", "debug", "webhook", "token"]):
        return "technical expert"
    elif any(word in message_lower for word in ["angry", "frustrated", "terrible", "worst", "disappointed", "hate", "urgent", "immediately"]):
        return "frustrated user"
    elif any(word in message_lower for word in ["pricing", "plan", "enterprise", "business", "roi", "cost", "invoice", "billing"]):
        return "business executive"
    else:
        return "general user"
