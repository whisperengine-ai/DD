"""
Corpus Callosum: Fusion and arbitration layer.
Combines outputs from all three triads with ethical gating.
"""
import numpy as np
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class CorpusCallosum:
    """Simplified fusion and arbitration."""
    
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            'chroma': 0.33,
            'prismo': 0.34,
            'anchor': 0.33
        }
        logger.info(f"Callosum initialized with weights: {self.weights}")
    
    def fuse(
        self,
        chroma_output: Dict,
        prismo_output: Dict,
        anchor_output: Dict
    ) -> Dict:
        """
        Simple fusion: weighted combination of outputs.
        """
        logger.debug("Starting fusion process")
        
        # Calculate coherence (simplified)
        coherence = self._calculate_coherence(
            chroma_output, prismo_output, anchor_output
        )
        
        # Check ethical gate (Prismo compliance)
        if not prismo_output.get('compliant', False):
            logger.warning("SLMU violation detected during fusion")
            return {
                'success': False,
                'reason': 'Ethical violation',
                'details': prismo_output.get('reason', 'Unknown violation'),
                'coherence': 0.0
            }
        
        # Simple fusion: combine sentiment + compliance + action
        fused_response = {
            'success': True,
            'coherence': coherence,
            'sentiment': chroma_output.get('sentiment', 0.5),
            'concepts': prismo_output.get('concepts', []),
            'response': anchor_output.get('response', ''),
            'weights_used': self.weights,
            'triad_outputs': {
                'chroma_vector_id': chroma_output.get('vector_id'),
                'prismo_concept_count': prismo_output.get('concept_count', 0),
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
        Simplified coherence: weighted average of component scores.
        """
        scores = []
        
        # Chroma score: based on sentiment (0.4-1.0 range mapped to 0-1)
        sentiment = chroma.get('sentiment', 0.5)
        chroma_score = max(0.0, (sentiment - 0.4) / 0.6)
        scores.append(chroma_score * self.weights['chroma'])
        
        # Prismo score: compliance is binary but we can add concept richness
        prismo_compliant = 1.0 if prismo.get('compliant', False) else 0.0
        concept_count = len(prismo.get('concepts', []))
        prismo_score = prismo_compliant * min(1.0, concept_count / 5.0)
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
