import streamlit as st
from persona_detector import detect_persona
from kb_manager import load_kb, retrieve_answer
from responder import adapt_tone
from escalator import check_escalation, escalate_to_human
from utils import log_interaction
from intent_detector import detect_intent

st.set_page_config(page_title="Persona-Adaptive Support Agent", page_icon="🤖", layout="centered")

st.title("🤖 Persona-Adaptive Customer Support Agent")


kb = load_kb()

if "user_name" not in st.session_state:
    st.session_state.user_name = st.text_input("👤 Enter your name", "Ramana")
user = st.session_state.user_name


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "context" not in st.session_state:
    # initialize as empty strings so later assignments of str types are allowed
    st.session_state.context = {"intent": "", "last_issue": ""}
message = st.chat_input("Type your message...")


if message:
    persona = detect_persona(message)
    intent = detect_intent(message)

    # 🧠 Store context for specific issues
    if intent != "general_query":
        st.session_state.context["intent"] = intent
        st.session_state.context["last_issue"] = message

    # 🗣 Use last context if current query is vague
    elif intent == "general_query" and st.session_state.context["intent"]:
        message = f"(User is following up on previous {st.session_state.context['intent']}) " + message

    if check_escalation(persona, message):
        escalation = escalate_to_human(message, persona)
        reply = f"⚠️ Your issue has been escalated to a human agent.\n**Agent:** {escalation['assigned_to']}"
    else:
        answer = retrieve_answer(kb, persona, message)
        reply = adapt_tone(persona, answer)

    st.session_state.chat_history.append({
        "user": user,
        "message": message,
        "reply": reply,
        "persona": persona,
        "intent": intent
    })

    log_interaction(user, persona, message, reply)


# --- Display Chat ---
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(f"**{chat['user']} ({chat['persona']})**: {chat['message']}")
    with st.chat_message("assistant"):
        st.markdown(chat["reply"])
