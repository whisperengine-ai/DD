"""
SLMU (Sanctifying Learning & Moral Understanding) policy engine.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


def load_slmu_rules(path: str) -> Dict:
    """Load SLMU rules from JSON config."""
    try:
        with open(path, 'r') as f:
            rules = json.load(f)
            logger.info(f"Loaded SLMU rules from {path}")
            return rules
    except FileNotFoundError:
        logger.warning(f"SLMU rules file not found: {path}. Using defaults.")
        return get_default_rules()
    except Exception as e:
        logger.error(f"Error loading SLMU rules: {e}")
        return get_default_rules()


def get_default_rules() -> Dict:
    """Return default SLMU rules."""
    return {
        "version": "1.0",
        "description": "Default SLMU rules",
        "prohibited_concepts": [
            "violence",
            "harm",
            "deception",
            "theft",
            "abuse"
        ],
        "required_virtues": [
            "temperance",
            "prudence",
            "justice",
            "fortitude"
        ],
        "ethical_weights": {
            "truthfulness": 1.0,
            "compassion": 0.9,
            "wisdom": 0.8
        }
    }


def check_compliance(text: str, concepts: List[str], rules: Dict) -> tuple[bool, str]:
    """
    Check if text and concepts comply with SLMU rules.
    Returns (is_compliant, reason)
    """
    prohibited = rules.get('prohibited_concepts', [])
    text_lower = text.lower()
    
    # Check for prohibited concepts in text
    for concept in prohibited:
        if concept.lower() in text_lower:
            return False, f"Contains prohibited concept: {concept}"
    
    # Check extracted concepts
    for concept in concepts:
        if concept.lower() in [p.lower() for p in prohibited]:
            return False, f"Extracted prohibited concept: {concept}"
    
    return True, "Compliant"
