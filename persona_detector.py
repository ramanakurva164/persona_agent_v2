import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash-lite")

def detect_persona(message: str) -> str:
    """
    Detects customer persona using Gemini or fallback.
    """
    try:
        prompt = f"""
        You are a smart classifier that identifies the persona of a customer based on their message.
        Possible personas:
        1. Technical Expert – uses technical terms, APIs, code, integrations.
        2. Frustrated User – expresses anger, confusion, dissatisfaction.
        3. Business Executive – asks about pricing, plans, reports, enterprise solutions.
        4. General User – casual query.
        Message: "{message}"
        Return only persona name.
        """
        response = model.generate_content(prompt)
        persona = response.text.strip().lower()
        if not persona:
            raise ValueError("Empty response")
        return persona
    except Exception:
        # Fallback
        message = message.lower()
        if any(word in message for word in ["api", "developer", "code", "integration", "token"]):
            return "technical expert"
        elif any(word in message for word in ["angry", "frustrated", "not working", "crash", "disappointed"]):
            return "frustrated user"
        elif any(word in message for word in ["pricing", "plan", "business", "report", "enterprise"]):
            return "business executive"
        else:
            return "general user"
