"""
Corpus Callosum: Fusion and arbitration layer.
Combines outputs from all three triads with ethical gating.
Performs final SLMU v2.0 compliance check with full context (linguistic + emotional data).
"""
import numpy as np
import sys
from pathlib import Path
from typing import Dict
import logging

# Import SLMU v2.0
sys.path.insert(0, str(Path(__file__).parent))
from slmu import check_compliance_enhanced, load_slmu_rules

logger = logging.getLogger(__name__)


class CorpusCallosum:
    """Simplified fusion and arbitration with SLMU v2.0 gating."""
    
    def __init__(self, weights: Dict[str, float] = None, slmu_rules_path: str = "config/slmu_rules.json"):
        self.weights = weights or {
            'chroma': 0.33,
            'prismo': 0.34,
            'anchor': 0.33
        }
        
        # Load SLMU rules for ethical gating
        self.slmu_rules = load_slmu_rules(slmu_rules_path)
        
        logger.info(f"Callosum initialized with weights: {self.weights}")
        logger.info(f"SLMU rules v{self.slmu_rules.get('version', 'unknown')} loaded for ethical gating")
    
    def fuse(
        self,
        chroma_output: Dict,
        prismo_output: Dict,
        anchor_output: Dict
    ) -> Dict:
        """
        Enhanced fusion with integrated SLMU v2.0 ethical gating.
        
        Performs final compliance check using:
        - Prismo's linguistic analysis (concepts, relationships, patterns)
        - Chroma's emotional intelligence (28-emotion scores)
        - Combined context for v2.0 emotion validation
        """
        logger.debug("Starting fusion process with SLMU v2.0 gating")
        
        # SLMU v2.0: Final ethical check with full context
        slmu_result = check_compliance_enhanced(
            text=prismo_output.get('text', ''),
            concepts=prismo_output.get('concepts', []),
            relationships=prismo_output.get('relationships', []),
            ethical_matches=prismo_output.get('ethical_patterns', {}),
            emotions=chroma_output.get('sentiment', None),  # 28-emotion scores from Chroma
            rules=self.slmu_rules
        )
        
        # Ethical gate: Reject if violations found
        if not slmu_result.get('compliant', False):
            violations = slmu_result.get('violations', [])
            logger.warning(f"SLMU v2.0 violation detected during fusion: {len(violations)} violation(s)")
            return {
                'success': False,
                'reason': 'Ethical violation',
                'details': {
                    'violations': violations,
                    'warnings': slmu_result.get('warnings', [])
                },
                'coherence': 0.0
            }
        
        # Calculate coherence using all triad outputs
        coherence = self._calculate_coherence(
            chroma_output, prismo_output, anchor_output
        )
        
        # Simple fusion: combine sentiment + compliance + action
        fused_response = {
            'success': True,
            'coherence': coherence,
            'sentiment': chroma_output.get('sentiment', 0.5),
            'concepts': prismo_output.get('concepts', []),
            'entities': prismo_output.get('entities', []),
            'relationships': prismo_output.get('relationships', []),
            'linguistic_features': prismo_output.get('linguistic_features', {}),
            'ethical_patterns': prismo_output.get('ethical_patterns', {}),
            'slmu_compliance': slmu_result,  # Full SLMU v2.0 result with emotion validation
            'response': anchor_output.get('response', ''),
            'weights_used': self.weights,
            'triad_outputs': {
                'chroma_vector_id': chroma_output.get('vector_id'),
                'chroma_embedding_dim': chroma_output.get('embedding_dim', 0),
                'chroma_similar_count': len(chroma_output.get('similar_memories', [])),
                'prismo_concept_count': prismo_output.get('concept_count', 0),
                'prismo_entity_count': prismo_output.get('entity_count', 0),
                'prismo_sentence_count': prismo_output.get('sentence_count', 0),
                'anchor_interaction_count': anchor_output.get('interaction_count', 0)
            }
        }
        
        logger.info(f"Fusion complete. Coherence: {coherence:.3f}")
        return fused_response
    
    def _calculate_coherence(
        self,
        chroma: Dict,
        prismo: Dict,
        anchor: Dict
    ) -> float:
        """
        Enhanced coherence calculation using spaCy features:
        - Sentiment quality (from RoBERTa)
        - Linguistic richness (token count, POS diversity)
        - Concept extraction success
        
        NOTE: SLMU compliance is checked in fuse() before this is called,
        so by the time we calculate coherence, we know input is ethically compliant.
        """
        scores = []
        
        # Chroma score: sentiment confidence + embedding quality
        sentiment = chroma.get('sentiment', {})
        if isinstance(sentiment, dict):
            # Enhanced mode with confidence scores
            sentiment_score = sentiment.get('score', 0.5)
        else:
            # Basic mode fallback
            sentiment_score = 0.5
        
        chroma_score = sentiment_score
        scores.append(chroma_score * self.weights['chroma'])
        
        # Prismo score: linguistic richness + concept extraction
        # (compliance already verified in fuse())
        linguistic = prismo.get('linguistic_features', {})
        if linguistic:
            token_count = linguistic.get('token_count', 0)
            pos_diversity = len(linguistic.get('pos_distribution', {}))
            
            # Reward richer text (more tokens, more POS types)
            richness_score = min(1.0, (token_count / 20.0) * (pos_diversity / 5.0))
        else:
            richness_score = 0.5
        
        # Concept extraction success
        concept_count = prismo.get('concept_count', 0)
        entity_count = prismo.get('entity_count', 0)
        concept_score = min(1.0, (concept_count + entity_count) / 10.0)
        
        # Combine richness and concepts (compliance already guaranteed)
        prismo_score = richness_score * 0.5 + concept_score * 0.5
        scores.append(prismo_score * self.weights['prismo'])
        
        # Anchor score: based on successful logging
        anchor_score = 1.0 if anchor.get('interaction_logged', False) else 0.5
        scores.append(anchor_score * self.weights['anchor'])
        
        # Normalize to 0-1 range
        total_weight = sum(self.weights.values())
        coherence = sum(scores) / total_weight
        
        return float(np.clip(coherence, 0.0, 1.0))
    
    def update_weights(self, performance_feedback: Dict):
        """
        Update fusion weights based on performance feedback.
        For MVP: simple adjustment.
        """
        learning_rate = 0.05
        
        for triad in ['chroma', 'prismo', 'anchor']:
            if triad in performance_feedback:
                adjustment = performance_feedback[triad] * learning_rate
                self.weights[triad] = np.clip(
                    self.weights[triad] + adjustment,
                    0.1, 0.6
                )
        
        # Renormalize
        total = sum(self.weights.values())
        self.weights = {k: v/total for k, v in self.weights.items()}
        
        logger.info(f"Weights updated: {self.weights}")
