import os
from typing import List, Tuple
try:
    import faiss  # type: ignore
except Exception:
    faiss = None

class LocalFAISS:
    def __init__(self, dim: int = 384, path: str = "./runtime/vector/index.faiss"):
        self.dim = dim
        self.path = path
        self.index = faiss.IndexFlatL2(dim) if faiss else None
        self.vectors: List[Tuple[str, list]] = []  # (id, vector)

    def add(self, id_: str, vector: list):
        if self.index:
            import numpy as np
            vec = np.array(vector, dtype="float32").reshape(1, -1)
            self.index.add(vec)
        self.vectors.append((id_, vector))

    def search(self, vector: list, k: int = 4):
        # mock cosine similarity by naive scoring
        if not self.vectors:
            return []
        scored = []
        for id_, v in self.vectors:
            score = sum(a*b for a,b in zip(v, vector)) / (1+len(v))
            scored.append((id_, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]
