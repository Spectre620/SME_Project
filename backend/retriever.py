import streamlit as st
import chromadb
from chromadb.utils import embedding_functions

DB_DIR = "../db"

@st.cache_resource
def get_retriever():
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_or_create_collection("sme_docs", embedding_function=embedding_function)
    return collection

collection = get_retriever()

def retrieve(query, top_k=3):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    docs = []
    for doc, source in zip(results['documents'][0], results['metadatas'][0]):
        docs.append({"text": doc, "source": source["source"]})
    return docs