import os
import re
from PyPDF2 import PdfReader
import chromadb
from chromadb.utils import embedding_functions

DATA_DIR = "../data"
DB_DIR = "../db"

# Initialize embedding model
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Initialize Chroma
chroma_client = chromadb.PersistentClient(path=DB_DIR)
collection = chroma_client.get_or_create_collection("sme_docs", embedding_function=embedding_function)

# Read and chunk PDFs
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def clean_text(text):
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Optional: remove special characters, but be cautious not to remove important punctuation
    text = re.sub(r'[^a-zA-Z0-9\s.,-]', '', text)
    return text

def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

for filename in os.listdir(DATA_DIR):
    if filename.endswith(".pdf"):
        path = os.path.join(DATA_DIR, filename)
        raw_text = read_pdf(path)
        cleaned_text = clean_text(raw_text)
        chunks = chunk_text(cleaned_text)
        
        ids = [f"{filename}_{idx}" for idx, chunk in enumerate(chunks)]
        
        collection.add(
            documents=chunks,
            ids=ids,
            metadatas=[{"source": filename}] * len(chunks)
        )

print("Ingestion complete!")