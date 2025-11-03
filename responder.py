def adapt_tone(persona, answer):
    if persona == "technical expert":
        return f"👨‍💻 *Technical Response:* {answer}\n\nYou can check the API documentation for deeper details."
    elif persona == "frustrated user":
        return f"💡 *Friendly Help:* I totally understand how that feels. {answer}\nWe’ll fix this together!"
    elif persona == "business exec":
        return f"📊 *Professional Response:* {answer}\nWould you like me to schedule a quick demo or send a proposal?"
    else:
        return f"🙂 *General Help:* {answer}"
