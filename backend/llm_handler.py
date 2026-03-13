import os
import streamlit as st
from groq import Groq

@st.cache_resource
def get_llm():
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    return client

client = get_llm()

def ask_llm(context, query):
    prompt = f"""
Answer the following question based on the context provided. If the answer is not in the context, say 'I could not find this information in the regulatory documents.'

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content