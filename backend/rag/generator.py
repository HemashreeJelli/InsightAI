import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(question, retrieved_chunks, chat_history=None):

    context = ""

    # Build context block
    for i, chunk in enumerate(retrieved_chunks):
        context += f"""
        [{i+1}]
        Source: {chunk['filename']}
        Page: {chunk['page_number']}

        {chunk['text']}
        """

    history_text = ""

    if chat_history:
        for msg in chat_history[-6:]:
            history_text += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
You are an AI research assistant.

Use ONLY the provided context to answer the question.

Give a detailed and well-structured answer.

If methods, models, or techniques are mentioned:
- explain what they do
- distinguish the proposed method from baseline methods
- summarize the methodology clearly

When analyzing tables or statistical tests (like t-tests), double-check that the metrics or values you quote match the exact pairs or rows being compared in the text context.

If the answer cannot be found in the context, say so explicitly.

CONVERSATION HISTORY:
{history_text}

RETRIEVED CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content