from src.document import Document
from typing import List
import json

def storeVectors(documents: List[Document]):
    with open("vector_store.jsonl", "a") as f:
        for doc in documents:
            for chunk, vec in zip(doc.chunks, doc.chunksVector):
                record = {
                    "text": chunk,
                    "vector": vec,
                    "source": doc.name
                }
                f.write(json.dumps(record) + "\n")