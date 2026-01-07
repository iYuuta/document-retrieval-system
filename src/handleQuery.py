from src.embedder import Embedder
from dotenv import load_dotenv
import numpy as np
import json
import requests
import os

def getAnswer(chunks, query):
    load_dotenv()
    address = os.getenv("OLLAMA_ADDRESS")
    context = "\n\n".join(chunk["text"] for chunk in chunks)
    prompt = prompt = f"Use the context below to answer the user's question.\nContext:\n{context}\nQuestion:\n{query}\n"
    try:
        response = requests.post(
            f"http://{address}/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
            },
        )
        print(response.json()["response"])
    except requests.exceptions.ConnectionError:
        print("Ollama server is not running")
    except Exception as e:
        print(f"Unexpected error: {e}")

def cosine_simularity(queryVector, chunkVector):
    dotProduct = np.dot(queryVector, chunkVector)
    queryMagnitude = np.linalg.norm(queryVector)
    chunkMagnitude = np.linalg.norm(chunkVector)
    magProduct = queryMagnitude * chunkMagnitude
    cosine_sim = dotProduct / magProduct
    return max(-1.0, min(1.0, cosine_sim))

def queryHandler():
    query = input("enter a question: ")
    embedder = Embedder()
    chunksData = []
    queryVector = embedder.embed(query)
    with open("vector_store.jsonl", "r") as f:
        for line in f:
            chunksData.append(json.loads(line))
    for chunk in chunksData:
        chunk["similarity"] = cosine_simularity(chunk["vector"], queryVector)
    sortedChunks = sorted(chunksData, key=lambda x: x["similarity"], reverse=True)
    topChunks = sortedChunks[:5]
    getAnswer(topChunks, query)