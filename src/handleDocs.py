from src.document import Document
from src.embedder import Embedder
from src.dataExtracter import extract_file_data
from src.saveData import storeVectors

def addHandler():
    files = input("enter ur documents: ")
    files = files.split()
    documents = []
    for file in files:
        text = extract_file_data("data/" + file)
        doc = Document(file, text)
        doc.chunkText()
        documents.append(doc)
    embedder = Embedder()
    for doc in documents:
        for chunk in doc.chunks:
            vector = embedder.embed(chunk)
            doc.chunksVector.append(vector.tolist())
    storeVectors(documents)    
