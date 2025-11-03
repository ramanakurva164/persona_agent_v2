import os, re, difflib

def load_kb(file_path="adsparkx_kb.txt"):
    """Load structured KB."""
    if not os.path.exists(file_path):
        print("⚠️ KB not found")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    articles_raw = content.split("---ARTICLE---")
    kb = []
    for raw in articles_raw:
        raw = raw.strip()
        if not raw:
            continue
        article = {}
        title = re.search(r"Title:\s*(.*)", raw)
        summary = re.search(r"Summary:\s*(.*)", raw)
        tags = re.search(r"Tags:\s*(.*)", raw)
        steps = re.findall(r"\d+\.\s*(.*)", raw)
        causes = re.findall(r"-\s*(.*)", raw)
        article["title"] = title.group(1).strip() if title else "Untitled"
        article["summary"] = summary.group(1).strip() if summary else ""
        article["steps"] = steps or []
        article["causes"] = causes or []
        article["tags"] = [t.strip().lower() for t in tags.group(1).split(",")] if tags else []
        kb.append(article)
    return kb


def retrieve_answer(kb, persona, query):
    """Retrieve most relevant KB answer."""
    query_lower = query.lower()
    best_article, best_score = None, 0
    for article in kb:
        combined = " ".join([article["title"], article["summary"], " ".join(article["tags"])])
        score = difflib.SequenceMatcher(None, query_lower, combined.lower()).ratio()
        if score > best_score:
            best_score = score
            best_article = article
    if best_article and best_score > 0.3:
        resp = f"**{best_article['title']}**\n\n"
        resp += f"**Summary:** {best_article['summary']}\n\n"
        resp += "**Recommended Steps:**\n"
        for i, step in enumerate(best_article['steps'], 1):
            resp += f"{i}. {step}\n"
        if best_article["causes"]:
            resp += "\n**Possible Causes:**\n- " + "\n- ".join(best_article["causes"])
        return resp
    return "I couldn’t find relevant info — can you clarify the issue?"
