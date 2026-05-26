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
You are a query rewriting assistant.

Your job is to rewrite follow-up questions into standalone questions.

Use the chat history for context.

If the question is already standalone, return it unchanged.

CHAT HISTORY:
{history_text}

FOLLOW-UP QUESTION:
{current_question}

STANDALONE QUESTION:
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