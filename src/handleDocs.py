from src.document import Document
from src.embedder import Embedder
from src.dataExtracter import extract_file_data
from typing import List
from src.db import insert_doc

def storeVectors(documents: List[Document]):
    for doc in documents:
        insert_doc(doc)
        
def addHandler():
    try:
        files = input("enter ur documents: ")
    except EOFError:
        exit()
    except KeyboardInterrupt:
        exit()
    files = files.split()
    documents = []
    for file in files:
        text = extract_file_data("data/" + file)
        if len(text) == 0:
            return
        doc = Document(file, text)
        doc.chunkText()
        documents.append(doc)
    embedder = Embedder()
    for doc in documents:
        for chunk in doc.chunks:
            vector = embedder.embed(chunk)
            doc.vectors.append(vector.tolist())
    storeVectors(documents)    
