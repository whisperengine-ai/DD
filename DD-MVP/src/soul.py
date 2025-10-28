"""
Soul: User's persistent ethical alignment and preferences.
Hybrid vector + metadata storage using JSON.
"""
import json
import numpy as np
from pathlib import Path
from typing import Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Soul:
    """Simplified user soul: preferences + ethical alignment."""
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.soul_file = self.data_dir / "soul_state.json"
        self.souls: Dict[str, Dict] = self._load()
        logger.info(f"Soul system initialized. {len(self.souls)} souls loaded.")
    
    def _load(self) -> Dict:
        """Load all souls from JSON."""
        if self.soul_file.exists():
            try:
                with open(self.soul_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data)} souls from {self.soul_file}")
                    return data
            except Exception as e:
                logger.error(f"Failed to load souls: {e}")
                return {}
        return {}
    
    def _save(self):
        """Persist to disk."""
        try:
            with open(self.soul_file, 'w', encoding='utf-8') as f:
                json.dump(self.souls, f, indent=2)
            logger.debug(f"Saved {len(self.souls)} souls to disk")
        except Exception as e:
            logger.error(f"Failed to save souls: {e}")
    
    def get_or_create(self, user_id: str) -> Dict:
        """Get existing soul or create new one."""
        if user_id not in self.souls:
            logger.info(f"Creating new soul for user: {user_id}")
            self.souls[user_id] = {
                'user_id': user_id,
                'vector': np.random.random(7).tolist(),  # 7D ROYGBIV
                'alignment_score': 0.5,
                'interaction_count': 0,
                'preferences': {},
                'created_at': datetime.utcnow().isoformat(),
                'last_updated': datetime.utcnow().isoformat()
            }
            self._save()
        return self.souls[user_id]
    
    def update(
        self,
        user_id: str,
        chroma_vector: np.ndarray,
        coherence: float
    ) -> Dict:
        """
        Update soul with new interaction data.
        Uses exponential moving average for vector.
        """
        soul = self.get_or_create(user_id)
        
        # Update vector (EMA with alpha=0.1)
        old_vector = np.array(soul['vector'])
        new_vector = 0.9 * old_vector + 0.1 * chroma_vector
        
        # Normalize to unit vector
        new_vector = new_vector / np.linalg.norm(new_vector)
        
        # Update alignment score (EMA with alpha=0.1)
        old_alignment = soul['alignment_score']
        new_alignment = 0.9 * old_alignment + 0.1 * coherence
        
        # Update soul
        soul['vector'] = new_vector.tolist()
        soul['alignment_score'] = float(np.clip(new_alignment, 0.0, 1.0))
        soul['interaction_count'] += 1
        soul['last_updated'] = datetime.utcnow().isoformat()
        
        self._save()
        
        logger.info(
            f"Soul updated for {user_id}: "
            f"alignment={soul['alignment_score']:.3f}, "
            f"interactions={soul['interaction_count']}"
        )
        
        return soul
    
    def get_vector(self, user_id: str) -> np.ndarray:
        """Get soul vector for comparison."""
        soul = self.get_or_create(user_id)
        return np.array(soul['vector'])
    
    def get_alignment(self, user_id: str) -> float:
        """Get user's alignment score."""
        soul = self.get_or_create(user_id)
        return soul['alignment_score']
    
    def set_preference(self, user_id: str, key: str, value: any):
        """Set a user preference."""
        soul = self.get_or_create(user_id)
        soul['preferences'][key] = value
        soul['last_updated'] = datetime.utcnow().isoformat()
        self._save()
    
    def get_preference(self, user_id: str, key: str, default=None):
        """Get a user preference."""
        soul = self.get_or_create(user_id)
        return soul['preferences'].get(key, default)
    
    def get_all_users(self) -> list:
        """Get list of all user IDs."""
        return list(self.souls.keys())
    
    def get_stats(self) -> Dict:
        """Get overall soul system statistics."""
        if not self.souls:
            return {
                'total_users': 0,
                'avg_alignment': 0.0,
                'total_interactions': 0
            }
        
        alignments = [s['alignment_score'] for s in self.souls.values()]
        interactions = [s['interaction_count'] for s in self.souls.values()]
        
        return {
            'total_users': len(self.souls),
            'avg_alignment': np.mean(alignments),
            'total_interactions': sum(interactions),
            'min_alignment': min(alignments),
            'max_alignment': max(alignments)
        }
