from typing import List

class Document:
    def __init__(self, name: str, text: str):
        self.name = name
        self.text = text
        self.chunks: List[str] = []
        self.chunksVector = []
        
    def chunkText(self, chunkSize: int = 500):
        words = self.text.split()
        for i in range(0, len(words), chunkSize):
            self.chunks.append(" ".join(words[i:i + chunkSize]))
    def setChunksVector(self, vector):
        self.chunksVector = vector