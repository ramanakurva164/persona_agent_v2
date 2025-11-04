import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
load_dotenv()
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.0-flash")

def get_ai_response(message: str, persona: str, intent: str, conversation_history: list) -> str:
    """
    Generate AI response using Gemini when KB doesn't have an answer.
    """
    try:
        # Build conversation context
        context = "Previous conversation:\n"
        for chat in conversation_history[-5:]:  # Last 5 exchanges
            context += f"User ({chat.get('persona', 'unknown')}): {chat['message']}\n"
            context += f"Assistant: {chat['reply']}\n\n"
        
        prompt = f"""You are a helpful customer support agent for AdSparkX (a digital advertising platform).

Customer Profile: {persona}
Current Issue Type: {intent}

{context}

Current Question: {message}

Instructions:
1. Provide a helpful, accurate response based on the conversation context
2. Match the tone to the customer's persona:
   - Technical Expert: Be precise, use technical terms, provide code examples if needed
   - Frustrated User: Be empathetic, apologetic, and solution-focused
   - Business Executive: Be professional, focus on business impact and ROI
   - General User: Be friendly, clear, and avoid jargon
3. If you don't know the answer, admit it and offer to escalate
4. Keep responses concise but complete
5. Always end with a follow-up question to ensure the issue is resolved

Response:"""

        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"AI response error: {e}")
        return "I apologize, but I'm having trouble generating a response. Let me escalate this to a human agent who can assist you better."
