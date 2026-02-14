from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict
from app.config import VECTOR_STORE_DIR

class VectorStore:
    def __int__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384
        print("Model loaded!")

    def create_index(self, chunks:List[dict], collection_id:str)->int:
        '''Create and Save faiss index for the given chunks'''
        if not chunks:
            raise ValueError("No chunks to index")

        print(f"Creating embeddings for {len(chunks)} chunks...")
        texts = [chunk["Content"] for chunk in chunks]
        embeddings = self.model.encode(texts, show_progress_bar = True)

        print("Creating FAISS index...")
        index = faiss.IndexFlatL2(self.dimension)
        index.add(np.array(embedddings).astype('float32'))

        #Save index and metadata
        store_path = VECTOR_STORE_DIR / collection_id
        store_path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(index, str(store_path / "index.faiss"))

        with open(store_path / "chunks.pkl" ,"wb") as f:
            pickle.dump(chunks)

        def search(self, collection_id : str , query:str, k:int = 3)-> List[dict]:
            """Search for similar chunks"""
            store_path = VECTOR_STORE_DIR / collection_id

            if not (store_path /"index.faiss").exists():
                raise FileNotFoundError("Index not found for collection_id: {collection_id}")
            
            ##Load 

            index = faiss.read_index(str(store_path /"index.faiss"))

            with open(store_path / "chunks.pkl", "rb") as f:
                chunks = pickle.load(f)

            # Search

            query_embeddings = self.model,encode([query])
            distances , indices = index.search(np.array(query_embeddings).astype('float32'), k)

            results = []

            for idex, distance in zip(indices[0], distances[0]):
                if idx < len(chunks):
                    results.append({
                        "content": chunks[idx]["content"],
                        "page": chunks[idx]["page"],
                        "score": float(1/(1+distance))
                    })

            return results

             
            