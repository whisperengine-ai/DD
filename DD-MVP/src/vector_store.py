"""
Simple vector store using NumPy for local storage.
For production, replace with Faiss or Qdrant.
"""
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class SimpleVectorStore:
    """
    Dead simple vector store using NumPy + file persistence.
    """
    
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.vectors: Dict[str, np.ndarray] = {}
        self.metadata: Dict[str, Dict] = {}
        self._load()
    
    def _load(self):
        """Load from disk."""
        if self.storage_path.exists():
            try:
                data = np.load(self.storage_path, allow_pickle=True)
                self.vectors = data['vectors'].item()
                self.metadata = data['metadata'].item()
                logger.info(f"Loaded {len(self.vectors)} vectors from {self.storage_path}")
            except Exception as e:
                logger.error(f"Failed to load vectors: {e}")
                self.vectors = {}
                self.metadata = {}
        else:
            logger.info(f"No existing vector store found at {self.storage_path}")
    
    def _save(self):
        """Save to disk."""
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            np.savez(
                self.storage_path,
                vectors=self.vectors,
                metadata=self.metadata
            )
            logger.debug(f"Saved {len(self.vectors)} vectors to {self.storage_path}")
        except Exception as e:
            logger.error(f"Failed to save vectors: {e}")
    
    def upsert(self, id: str, vector: np.ndarray, metadata: Dict):
        """Insert or update vector."""
        self.vectors[id] = vector
        self.metadata[id] = metadata
        self._save()
    
    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict]:
        """Find k most similar vectors (cosine similarity)."""
        if len(self.vectors) == 0:
            return []
        
        similarities = []
        for vid, vec in self.vectors.items():
            try:
                sim = np.dot(query_vector, vec) / (
                    np.linalg.norm(query_vector) * np.linalg.norm(vec)
                )
                similarities.append((vid, float(sim), self.metadata.get(vid, {})))
            except Exception as e:
                logger.warning(f"Error calculating similarity for {vid}: {e}")
                continue
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return [
            {'id': vid, 'similarity': sim, 'metadata': meta}
            for vid, sim, meta in similarities[:k]
        ]
    
    def count(self) -> int:
        """Get total vector count."""
        return len(self.vectors)
    
    def get(self, id: str) -> Optional[Dict]:
        """Get a specific vector by ID."""
        if id in self.vectors:
            return {
                'id': id,
                'vector': self.vectors[id],
                'metadata': self.metadata.get(id, {})
            }
        return None
    
    def delete(self, id: str):
        """Delete a vector by ID."""
        if id in self.vectors:
            del self.vectors[id]
            if id in self.metadata:
                del self.metadata[id]
            self._save()
