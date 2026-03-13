from backend.retriever import retrieve
from backend.llm_handler import ask_llm

def ask_sme_assist(query):
    docs = retrieve(query)
    context = "\n\n".join([d['text'] for d in docs])
    answer = ask_llm(context, query)
    return answer, docs