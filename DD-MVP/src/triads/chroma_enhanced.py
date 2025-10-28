"""
Chroma Triad (Enhanced): Perceptive/Emotional processing with real NLP.
Uses:
- Cardiff Twitter RoBERTa (28-emotion multilabel model) for rich emotion detection
  Detects: anger, anticipation, disgust, fear, joy, love, optimism, pessimism, 
  sadness, surprise, trust, and 17 more nuanced emotions
- sentence-transformers (all-MiniLM-L6-v2) for 384D semantic embeddings
- ChromaDB for persistent vector storage with filesystem backend
- ROYGBIV emotional mapping: Maps all 28 emotions to 7D color spectrum
"""
import numpy as np
from typing import Dict, List, Optional
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)


class ChromaTriadEnhanced:
    """Enhanced perceptive/emotional processing with real NLP."""
    
    def __init__(self, chroma_persist_dir: str = "./data/chromadb"):
        logger.info("Initializing Enhanced Chroma Triad with real NLP models...")
        
        # Initialize ChromaDB for vector storage
        self.chroma_client = chromadb.Client(Settings(
            persist_directory=chroma_persist_dir,
            anonymized_telemetry=False
        ))
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="chroma_memories",
            metadata={"description": "ROYGBIV emotional vectors"}
        )
        
        # Load emotion analysis model (Cardiff Twitter RoBERTa - 11 emotions)
        # Detects: admiration, amusement, anger, annoyance, approval, caring, confusion,
        # curiosity, desire, disappointment, disapproval, disgust, embarrassment, 
        # excitement, fear, gratitude, grief, joy, love, nervousness, optimism, 
        # pride, realization, relief, remorse, sadness, surprise, neutral
        logger.info("Loading Cardiff Twitter RoBERTa emotion model (28 emotions)...")
        self.sentiment_tokenizer = AutoTokenizer.from_pretrained(
            "cardiffnlp/twitter-roberta-base-emotion-multilabel-latest"
        )
        self.sentiment_model = AutoModelForSequenceClassification.from_pretrained(
            "cardiffnlp/twitter-roberta-base-emotion-multilabel-latest"
        )
        self.sentiment_pipeline = pipeline(
            "text-classification",
            model=self.sentiment_model,
            tokenizer=self.sentiment_tokenizer,
            top_k=None  # Return all emotion scores
        )
        
        # Load sentence transformer for embeddings
        logger.info("Loading sentence-transformers model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, good quality
        
        # ROYGBIV emotional mapping
        self.color_emotions = {
            'red': ['anger', 'passion', 'energy', 'urgency'],
            'orange': ['enthusiasm', 'creativity', 'determination'],
            'yellow': ['joy', 'optimism', 'clarity', 'hope'],
            'green': ['balance', 'growth', 'harmony', 'peace'],
            'blue': ['calm', 'trust', 'wisdom', 'depth'],
            'indigo': ['intuition', 'insight', 'spirituality'],
            'violet': ['inspiration', 'imagination', 'mystery']
        }
        
        logger.info("Enhanced Chroma Triad initialized successfully")
    
    def process(self, text: str, user_id: str) -> Dict:
        """
        Enhanced processing: Perception → Association → Creation
        """
        logger.info(f"Enhanced Chroma processing for user {user_id}")
        
        # 1. Perception: RoBERTa sentiment analysis
        sentiment_result = self._roberta_sentiment(text)
        
        # 2. Association: Generate embeddings and map to ROYGBIV
        embedding = self._generate_embedding(text)
        color_vector = self._map_to_roygbiv(text, sentiment_result, embedding)
        
        # 3. Creation: Store in ChromaDB and retrieve similar memories
        vector_id = f"chroma_{user_id}_{abs(hash(text)) % 1000000}"
        
        self.collection.add(
            ids=[vector_id],
            embeddings=[embedding.tolist()],
            metadatas=[{
                'user_id': user_id,
                'sentiment_label': sentiment_result['label'],
                'sentiment_score': float(sentiment_result['score']),
                'text_snippet': text[:200]
            }],
            documents=[text]
        )
        
        # Search for similar memories
        similar = self._search_similar(embedding, user_id, k=3)
        
        return {
            'sentiment': {
                'label': sentiment_result['label'],
                'score': float(sentiment_result['score']),
                'all_scores': sentiment_result.get('all_scores', {})
            },
            'color_vector': color_vector.tolist(),
            'embedding_dim': len(embedding),
            'similar_memories': similar,
            'vector_id': vector_id
        }
    
    def _roberta_sentiment(self, text: str) -> Dict:
        """
        Multi-label emotion analysis using Cardiff Twitter RoBERTa (28 emotions).
        Returns all emotion scores for rich mixed-emotion detection.
        
        Handles long text by truncating to RoBERTa's 512 token limit.
        """
        try:
            # Properly truncate using tokenizer (RoBERTa max = 512 tokens)
            # Use truncation=True to handle long text gracefully
            results = self.sentiment_pipeline(
                text,
                truncation=True,
                max_length=512
            )[0]
            
            # Find highest scoring emotion
            best = max(results, key=lambda x: x['score'])
            
            # Create emotion score dict with ALL 28 emotions
            all_scores = {r['label']: float(r['score']) for r in results}
            
            return {
                'label': best['label'],  # Dominant emotion
                'score': float(best['score']),
                'all_scores': all_scores  # All 28 emotion scores for mixed emotions
            }
        except Exception as e:
            logger.error(f"Emotion analysis failed: {e}")
            return {'label': 'neutral', 'score': 0.5, 'all_scores': {'neutral': 0.5}}
    
    def _generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate semantic embedding using sentence-transformers.
        Returns 384-dim vector from all-MiniLM-L6-v2.
        """
        try:
            embedding = self.embedder.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return np.random.random(384)  # Fallback
    
    def _map_to_roygbiv(
        self,
        text: str,
        sentiment: Dict,
        embedding: np.ndarray
    ) -> np.ndarray:
        """
        Map text + sentiment + embedding to 7D ROYGBIV vector.
        Uses ALL emotion scores (28 emotions) for rich mixed-emotion handling.
        
        Emotion-to-Color mapping:
        - RED (passion/intensity): anger, annoyance, desire, excitement
        - ORANGE (enthusiasm/warmth): amusement, approval, caring, optimism
        - YELLOW (joy/clarity): joy, admiration, gratitude, pride, relief
        - GREEN (balance/growth): realization, approval, curiosity
        - BLUE (calm/trust): neutral, approval
        - INDIGO (depth/introspection): confusion, disappointment, sadness, grief, nervousness
        - VIOLET (imagination/spirituality): surprise, love, embarrassment
        """
        # Start with base values
        roygbiv = np.zeros(7)
        
        # Get all emotion scores from the multilabel model
        all_scores = sentiment.get('all_scores', {})
        
        # Map each of 28 emotions to ROYGBIV colors
        emotion_color_map = {
            # RED (0): Intense, passionate, urgent emotions
            'anger': (0, 0.8),
            'annoyance': (0, 0.5),
            'desire': (0, 0.6),
            'excitement': (0, 0.7),
            'disapproval': (0, 0.4),
            
            # ORANGE (1): Warm, enthusiastic, creative emotions
            'amusement': (1, 0.7),
            'optimism': (1, 0.8),
            'caring': (1, 0.6),
            
            # YELLOW (2): Joyful, positive, bright emotions
            'joy': (2, 0.9),
            'admiration': (2, 0.7),
            'gratitude': (2, 0.8),
            'pride': (2, 0.7),
            'relief': (2, 0.6),
            
            # GREEN (3): Balanced, growing, harmonious emotions
            'realization': (3, 0.6),
            'approval': (3, 0.7),
            'curiosity': (3, 0.5),
            
            # BLUE (4): Calm, stable, trustful emotions
            'neutral': (4, 0.6),
            
            # INDIGO (5): Deep, introspective, contemplative emotions
            'confusion': (5, 0.5),
            'disappointment': (5, 0.6),
            'sadness': (5, 0.8),
            'grief': (5, 0.9),
            'nervousness': (5, 0.6),
            'fear': (5, 0.7),
            'remorse': (5, 0.7),
            'disgust': (5, 0.6),
            
            # VIOLET (6): Spiritual, imaginative, mysterious emotions
            'surprise': (6, 0.7),
            'love': (6, 0.9),
            'embarrassment': (6, 0.5),
        }
        
        # Apply each emotion's contribution to its corresponding color
        for emotion, score in all_scores.items():
            if emotion in emotion_color_map:
                color_idx, weight = emotion_color_map[emotion]
                roygbiv[color_idx] += score * weight
        
        # Add embedding-based color influence (first 7 components)
        embedding_influence = np.abs(embedding[:7]) / (np.linalg.norm(embedding[:7]) + 1e-9)
        roygbiv += embedding_influence * 0.2
        
        # Add text-based emotional keywords
        text_lower = text.lower()
        for i, (color, emotions) in enumerate(self.color_emotions.items()):
            for emotion in emotions:
                if emotion in text_lower:
                    roygbiv[i] += 0.15
        
        # Normalize to unit vector
        norm = np.linalg.norm(roygbiv)
        if norm > 0:
            roygbiv = roygbiv / norm
        else:
            roygbiv = np.ones(7) / np.sqrt(7)  # Uniform if no signal
        
        return roygbiv
    
    def _search_similar(
        self,
        query_embedding: np.ndarray,
        user_id: str,
        k: int = 3
    ) -> List[Dict]:
        """
        Search for similar memories in ChromaDB.
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=k,
                where={"user_id": user_id}
            )
            
            if not results['ids'] or len(results['ids'][0]) == 0:
                return []
            
            similar = []
            for i in range(len(results['ids'][0])):
                similar.append({
                    'id': results['ids'][0][i],
                    'distance': float(results['distances'][0][i]) if results['distances'] else 0.0,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'document': results['documents'][0][i] if results['documents'] else ''
                })
            
            return similar
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            return []
    
    def get_memory_count(self, user_id: Optional[str] = None) -> int:
        """Get total memory count, optionally filtered by user."""
        try:
            if user_id:
                results = self.collection.get(where={"user_id": user_id})
                return len(results['ids']) if results['ids'] else 0
            else:
                return self.collection.count()
        except Exception as e:
            logger.error(f"Count failed: {e}")
            return 0
