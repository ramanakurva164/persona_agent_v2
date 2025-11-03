import datetime

def log_interaction(user, persona, message, reply, file_path="logs.txt"):
    """Save chat logs for review."""
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {user} ({persona}): {message}\nBot: {reply}\n\n")
