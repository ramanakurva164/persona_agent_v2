import streamlit as st
from persona_detector import detect_persona
from kb_manager import load_kb, retrieve_answer
from responder import adapt_tone
from escalator import check_escalation, escalate_to_human
from utils import log_interaction
from intent_detector import detect_intent
from ai_agent import get_ai_response
from gtts import gTTS
import os
from playsound import playsound

def speak_text(text: str):
    """Convert text to speech and play it."""
    try:
        tts = gTTS(text=text, lang='en')
        filename = "response.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"TTS Error: {e}")

st.set_page_config(page_title="AdSparkX Support Agent", page_icon="🤖", layout="centered")

st.title("🤖 AdSparkX Customer Support Agent")

# Load Knowledge Base
kb = load_kb()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "context" not in st.session_state:
    st.session_state.context = {"intent": "", "last_issue": ""}

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "show_examples" not in st.session_state:
    st.session_state.show_examples = True

# User name input (always visible)
user_name = st.text_input("👤 Enter your name", value=st.session_state.user_name, key="name_input")
if user_name:
    st.session_state.user_name = user_name

# Show example questions when no chat history exists
if st.session_state.show_examples and not st.session_state.chat_history:
    st.info("👋 Welcome! I'm here to help you with AdSparkX support.")
    
    with st.expander("💡 **What can I help you with?** (Click to see examples)", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔐 **Login & Account Issues**")
            st.markdown("""
            - "I can't log into my account"
            - "My password reset isn't working"
            - "Account locked after failed attempts"
            - "Social login (Google/Apple) not working"
            """)
            
            st.markdown("### 💳 **Payment & Billing**")
            st.markdown("""
            - "My payment was declined"
            - "Unexpected charge on my card"
            - "Need a refund for duplicate charge"
            - "Update my billing information"
            """)
            
            st.markdown("### ⚙️ **API & Technical Issues**")
            st.markdown("""
            - "API returning 504 timeout errors"
            - "Integration with third-party failing"
            - "Webhook not receiving events"
            - "Authentication token expired"
            """)
        
        with col2:
            st.markdown("### 💰 **Business & Enterprise**")
            st.markdown("""
            - "What are your enterprise pricing plans?"
            - "Need custom SLA for my business"
            - "ROI reports and analytics"
            - "Volume discounts available?"
            """)
            
            st.markdown("### ⚡ **Performance Issues**")
            st.markdown("""
            - "Dashboard loading very slowly"
            - "Campaign reports taking too long"
            - "High latency on API calls"
            - "App freezing or crashing"
            """)
            
            st.markdown("### ✨ **Feature Requests**")
            st.markdown("""
            - "Can you add bulk upload feature?"
            - "Need custom reporting options"
            - "Integration with [platform name]"
            - "Mobile app availability?"
            """)
        
        st.markdown("---")
        st.markdown("**💬 Just type your question naturally - I'll understand and help you!**")

# Chat input
message = st.chat_input("Type your message..." if st.session_state.user_name else "Please enter your name first")

# Process message
if message and st.session_state.user_name:
    # Hide examples once user starts chatting
    st.session_state.show_examples = False
    
    try:
        # Step 1: Detect persona with conversation context
        persona = detect_persona(message, st.session_state.chat_history)
        
        # Step 2: Detect intent with conversation context
        intent = detect_intent(message, st.session_state.chat_history)
        
        # Step 3: Update context
        if intent != "general_query":
            st.session_state.context["intent"] = intent
            st.session_state.context["last_issue"] = message
        
        # Step 4: Check if escalation needed
        should_escalate = check_escalation(
            persona, 
            message, 
            intent, 
            st.session_state.chat_history
        )
        
        if should_escalate:
            # Human escalation
            escalation = escalate_to_human(
                message, 
                persona, 
                intent, 
                st.session_state.chat_history
            )
            reply = f"""⚠️ **Your issue has been escalated to a human agent**

**Assigned to:** {escalation['assigned_to']}
**Team:** {escalation['team']}
**Priority:** {escalation['priority'].upper()}
**Estimated Response:** {escalation['estimated_response']}

A specialist will reach out to you shortly. Thank you for your patience! 🙏"""
        
        else:
            # Step 5: Try KB first
            kb_answer = retrieve_answer(
                kb, 
                persona, 
                message, 
                intent, 
                st.session_state.chat_history
            )
            
            if kb_answer:
                # KB found answer - adapt tone
                reply = adapt_tone(persona, kb_answer)
            else:
                # Step 6: Use AI agent (Gemini) if KB doesn't have answer
                ai_response = get_ai_response(
                    message, 
                    persona, 
                    intent, 
                    st.session_state.chat_history
                )
                reply = adapt_tone(persona, ai_response)
        
        # Store in chat history
        st.session_state.chat_history.append({
            "user": st.session_state.user_name,
            "message": message,
            "reply": reply,
            "persona": persona,
            "intent": intent
        })
        
        # Log interaction
        try:
            log_interaction(st.session_state.user_name, persona, message, reply)
        except Exception as log_error:
            print(f"Logging error: {log_error}")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.chat_history.append({
            "user": st.session_state.user_name,
            "message": message,
            "reply": "I apologize, but I encountered an error. Please try again or contact support.",
            "persona": "unknown",
            "intent": "error"
        })

# Display chat history
for i, chat in enumerate(st.session_state.chat_history):
    with st.chat_message("user"):
        st.markdown(f"**{chat['user']}** *({chat['persona']})*")
        st.markdown(chat['message'])
    
    with st.chat_message("assistant"):
        st.markdown(chat["reply"])
        speak_text(chat["reply"])
        
        # Show intent badge
        if chat.get('intent'):
            intent_color = {
                "login_issue": "🔐",
                "payment_issue": "💳",
                "api_error": "⚙️",
                "billing_dispute": "💰",
                "feature_request": "✨",
                "performance_issue": "⚡",
                "integration_issue": "🔌",
                "general_query": "💬"
            }
            st.caption(f"{intent_color.get(chat['intent'], '💬')} {chat['intent'].replace('_', ' ').title()}")

# Sidebar with conversation stats
with st.sidebar:
    
    if st.session_state.chat_history:
        
        if st.button("🔄 Clear Conversation"):
            st.session_state.chat_history = []
            st.session_state.context = {"intent": "", "last_issue": ""}
            st.session_state.show_examples = True
            st.rerun()
    
    
    st.markdown("---")
    st.markdown("### 🆘 Need Help?")
    st.markdown("""
    **Quick Tips:**
    - Be specific about your issue
    - Include error messages if any
    - Mention what you've already tried
    - Ask follow-up questions 
    """)
    
    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("""
    **Email:** support@adsparkx.com  
    **Phone:** 1-800-ADSPARKX  
    **Hours:** 24/7 Support
    """)
