from src.embedder import Embedder
from dotenv import load_dotenv
import numpy as np
import json
import requests
import os
from src.db import get_docs
from src.db import Document as dbDocument

def getAnswer(docs: list[dbDocument], query):
    load_dotenv()
    port = os.getenv("OLLAMA_PORT")
    model = os.getenv("OLLAMA_MODEL")
    context = "\n\n".join(doc.content for doc in docs)
    if context:
        prompt = f"Use the context below to answer the user's question.\nContext:\n{context}\nQuestion:\n{query}\n"
    else:
        prompt = f"No relevant context was found. Please answer the user's question directly based on your own knowledge and reasoning.\nQuestion:\n{query}\n"
    try:
        response = requests.post(
            f"http://localhost:{port}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
        )
        print(response.json()["response"])
    except requests.exceptions.ConnectionError:
        print("Ollama server is not running")
    except Exception as e:
        print(f"Unexpected error: {e}")

def cosine_similarity(queryVector, chunkVector):
    dotProduct = np.dot(queryVector, chunkVector)
    queryMagnitude = np.linalg.norm(queryVector)
    chunkMagnitude = np.linalg.norm(chunkVector)
    magProduct = queryMagnitude * chunkMagnitude
    cosine_sim = dotProduct / magProduct
    return max(-1.0, min(1.0, cosine_sim))

def queryHandler():
    try:
        query = input("enter a question: ")
    except EOFError:
        exit()
    except KeyboardInterrupt:
        exit()
    embedder = Embedder()
    queryVector = embedder.embed(query)
    docs = get_docs()
    for doc in docs:
        doc.similarity = cosine_similarity(queryVector, doc.embedding)
    filteredDocs = [doc for doc in docs if doc.similarity > 0.2]
    sortedDocs = sorted(filteredDocs, key=lambda x: x.similarity, reverse=True)
    topDocs = sortedDocs[:5]
    getAnswer(topDocs, query)