"""
Chroma Triad: Perceptive/Emotional processing.
Simplified version with basic sentiment analysis and ROYGBIV vector mapping.
"""
import numpy as np
from typing import Dict, List
import logging
from vector_store import SimpleVectorStore

logger = logging.getLogger(__name__)


class ChromaTriad:
    """Simplified perceptive/emotional processing."""
    
    def __init__(self, vector_store: SimpleVectorStore):
        self.vectors = vector_store
        self.color_map = {
            'red': 0, 'orange': 1, 'yellow': 2, 'green': 3,
            'blue': 4, 'indigo': 5, 'violet': 6
        }
        # Simple sentiment word lists
        self.positive_words = {
            'good', 'great', 'love', 'happy', 'joy', 'wonderful',
            'excellent', 'amazing', 'beautiful', 'blessed', 'peace',
            'kind', 'compassion', 'wisdom', 'understanding'
        }
        self.negative_words = {
            'bad', 'hate', 'sad', 'terrible', 'awful', 'pain',
            'anger', 'fear', 'anxiety', 'worry', 'stress'
        }
    
    def process(self, text: str, user_id: str) -> Dict:
        """
        Simplified: Perception → Association → Creation in one pass.
        """
        logger.info(f"Chroma processing for user {user_id}")
        
        # 1. Perception: Basic sentiment analysis
        sentiment = self._simple_sentiment(text)
        
        # 2. Association: Map to ROYGBIV vector
        color_vector = self._text_to_color(text, sentiment)
        
        # 3. Creation: Store and retrieve similar memories
        vector_id = f"chroma_{user_id}_{abs(hash(text)) % 1000000}"
        self.vectors.upsert(
            id=vector_id,
            vector=color_vector,
            metadata={
                'user_id': user_id,
                'sentiment': sentiment,
                'text_snippet': text[:100]
            }
        )
        
        similar = self.vectors.search(color_vector, k=3)
        
        return {
            'sentiment': sentiment,
            'color_vector': color_vector.tolist(),
            'similar_memories': similar,
            'vector_id': vector_id
        }
    
    def _simple_sentiment(self, text: str) -> float:
        """Basic sentiment: count positive vs negative words."""
        words = set(text.lower().split())
        pos_count = len(words & self.positive_words)
        neg_count = len(words & self.negative_words)
        
        if pos_count + neg_count == 0:
            return 0.5  # Neutral
        
        return pos_count / (pos_count + neg_count)
    
    def _text_to_color(self, text: str, sentiment: float) -> np.ndarray:
        """
        Map text to 7D ROYGBIV vector.
        Simplified: Use character distribution + sentiment.
        """
        # Start with random seed based on text
        np.random.seed(abs(hash(text)) % 2**32)
        vector = np.random.random(7)
        
        # Adjust based on sentiment
        # High sentiment -> warmer colors (red, orange, yellow)
        # Low sentiment -> cooler colors (blue, indigo, violet)
        if sentiment > 0.5:
            vector[0:3] *= (1 + sentiment)  # Boost warm colors
        else:
            vector[4:7] *= (2 - sentiment)  # Boost cool colors
        
        # Normalize
        vector = vector / np.linalg.norm(vector)
        
        return vector
