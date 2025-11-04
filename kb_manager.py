import os
import re
import difflib

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
        steps = re.findall(r"^\d+\.\s*(.*)$", raw, re.MULTILINE)
        causes = re.findall(r"^-\s*(.*)$", raw, re.MULTILINE)
        
        article["title"] = title.group(1).strip() if title else "Untitled"
        article["summary"] = summary.group(1).strip() if summary else ""
        article["steps"] = steps or []
        article["causes"] = causes or []
        article["tags"] = [t.strip().lower() for t in tags.group(1).split(",")] if tags else []
        
        kb.append(article)
    
    return kb


def retrieve_answer(kb, persona, query, intent="general_query", conversation_history=None):
    """
    Retrieve most relevant KB answer considering conversation context.
    """
    if not kb:
        return None
    
    query_lower = query.lower()
    
    # Enhance query with conversation context
    if conversation_history:
        recent_keywords = []
        for chat in conversation_history[-2:]:
            recent_keywords.extend(chat['message'].lower().split())
        query_lower += " " + " ".join(set(recent_keywords))
    
    best_article, best_score = None, 0
    
    for article in kb:
        # Build searchable text
        combined = " ".join([
            article["title"],
            article["summary"],
            " ".join(article["tags"]),
            " ".join(article["steps"][:3])  # Include first 3 steps
        ])
        
        # Calculate similarity
        score = difflib.SequenceMatcher(None, query_lower, combined.lower()).ratio()
        
        # Boost score if intent matches tags
        if intent != "general_query" and intent.replace("_", " ") in combined.lower():
            score += 0.2
        
        if score > best_score:
            best_score = score
            best_article = article
    
    # Return article if confidence is reasonable
    if best_article and best_score > 0.25:
        resp = f"**{best_article['title']}**\n\n"
        resp += f"**Summary:** {best_article['summary']}\n\n"
        
        if best_article['steps']:
            resp += "**Recommended Steps:**\n"
            for i, step in enumerate(best_article['steps'], 1):
                resp += f"{i}. {step}\n"
        
        if best_article["causes"]:
            resp += "\n**Possible Causes:**\n- " + "\n- ".join(best_article["causes"])
        
        return resp
    
    return None
