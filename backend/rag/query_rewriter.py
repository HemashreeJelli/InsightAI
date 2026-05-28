import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def rewrite_query(chat_history, current_question):
    # ==============================================================
    # 🎯 GUARD 1: If history is empty, skip rewriting completely
    # ==============================================================
    if not chat_history or len(chat_history) < 2:
        return current_question.strip()

    # ==============================================================
    # 🎯 GUARD 2: Heuristic check for inherently standalone phrases
    # ==============================================================
    text_lower = current_question.lower()
    standalone_indicators = ["paper", "methodology", "dataset", "results", "model", "approach"]
    
    # If the user explicitly asks a direct structural question, preserve it
    if any(word in text_lower for word in standalone_indicators):
        return current_question.strip()

    # If both guards pass, proceed to contextual LLM pronoun resolution
    history_text = ""
    for msg in chat_history:
        history_text += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
You are a query rewriting assistant for a research-paper QA system.

Your task is to rewrite follow-up questions into COMPLETE standalone questions.

Rules:
- Preserve the original meaning exactly
- Preserve important technical entities, methods, datasets, and topics
- Resolve vague references like:
  - it
  - they
  - this method
  - the baseline
- Keep the rewritten query concise
- Do not answer the question
- Return ONLY the rewritten standalone query

CHAT HISTORY:
{history_text}

FOLLOW-UP QUESTION:
{current_question}

REWRITTEN STANDALONE QUESTION:
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    return completion.choices[0].message.content.strip()