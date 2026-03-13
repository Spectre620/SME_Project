import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from backend.rag_pipeline import ask_sme_assist
import speech_recognition as sr

st.title("SME Assist - Kenyan Compliance CoPilot")

# --- Voice input ---
def get_voice_query():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        return query
    except:
        return ""

def detect_risks(response_text):
    risks = []
    if "Turnover Tax" not in response_text:
        risks.append("Check if your business should register for Turnover Tax.")
    if "KRA PIN" not in response_text:
        risks.append("Obtain KRA PIN to avoid penalties.")
    if "County Permit" not in response_text:
        risks.append("Obtain County Business Permit.")
    return risks

# Streamlit input
col1, col2 = st.columns([0.9, 0.1])

with col1:
    query = st.text_input("Ask a compliance question:", key="query_input", label_visibility="collapsed")

with col2:
    if st.button("🎤", key="voice_button"):
        voice_query = get_voice_query()
        if voice_query:
            query = voice_query
            st.session_state.query_input = query

if query:
    with st.spinner("Analyzing regulations..."):
        response, docs = ask_sme_assist(query)

    st.subheader("Compliance Checklist")
    st.write(response)

    st.subheader("Potential Compliance Risks ⚠️")
    risks = detect_risks(response)
    for r in risks:
        st.write(f"- {r}")

    st.subheader("Sources")
    for doc in docs:
        st.write(doc['source'])

# Example pre-built queries
st.sidebar.subheader("Example Questions")
examples = [
    "What taxes does a small shop pay in Kenya?",
    "What licenses are needed for a bakery?",
    "How do I register for KRA tax?"
]
for q in examples:
    if st.sidebar.button(q):
        query = q