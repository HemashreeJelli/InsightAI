import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(question, retrieved_chunks):

    context = ""

    # Build context block
    for i, chunk in enumerate(retrieved_chunks):
        context += f"""
        [{i+1}]
        Source: {chunk['filename']}
        Page: {chunk['page_number']}

        {chunk['text']}
        """

    prompt = f"""
You are an AI research assistant.

Use ONLY the provided context to answer the question.

Give a detailed and well-structured answer.

If methods, models, or techniques are mentioned:
- explain what they do
- distinguish the proposed method from baseline methods
- summarize the methodology clearly

If the answer cannot be found in the context, say so explicitly.

CONTEXT:
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