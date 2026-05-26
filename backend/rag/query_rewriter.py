from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def rewrite_query(chat_history, current_question):

    # Convert chat history into readable format
    history_text = ""

    for msg in chat_history:
        history_text += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
You are a query rewriting assistant for a research-paper QA system.

Your task is to rewrite follow-up questions into COMPLETE standalone questions.

Rules:
- Preserve the original meaning exactly
- Resolve vague references like:
  - it
  - they
  - this method
  - the baseline
  - those results
- Use the chat history to infer what these references mean
- DO NOT answer the question
- ONLY return the rewritten standalone query
- If the question is already standalone, return it unchanged

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