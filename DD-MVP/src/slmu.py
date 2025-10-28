"""
SLMU (Sanctifying Learning & Moral Understanding) policy engine.
Enhanced v2.0 with linguistic intelligence from spaCy integration.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


def load_slmu_rules(path: str) -> Dict:
    """Load SLMU rules from JSON config."""
    try:
        with open(path, 'r') as f:
            rules = json.load(f)
            logger.info(f"Loaded SLMU rules v{rules.get('version', 'unknown')} from {path}")
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
    DEPRECATED: Basic string-based compliance checking.
    Use check_compliance_enhanced() for v2.0 features with linguistic data.
    
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


def check_compliance_enhanced(
    text: str,
    concepts: List[Dict],
    relationships: List[Dict],
    ethical_matches: Dict,
    emotions: Optional[Dict] = None,
    rules: Dict = None
) -> Dict:
    """
    Enhanced SLMU v2.0 compliance checking using linguistic intelligence.
    
    Args:
        text: Raw text input
        concepts: Extracted concepts with lemmas and POS tags from Prismo
        relationships: Subject-predicate-object relationships from dependency parsing
        ethical_matches: Pattern matches (harm_patterns, ethical_patterns, command_patterns)
        emotions: Emotion scores from Cardiff RoBERTa (optional)
        rules: SLMU rules configuration
    
    Returns:
        Dict with compliance status, violations, warnings, and detailed analysis
    """
    if rules is None:
        rules = get_default_rules()
    
    violations = []
    warnings = []
    required_present = []
    
    prohibited_concepts = rules.get('prohibited_concepts', [])
    required_virtues = rules.get('required_virtues', [])
    
    # 1. CHECK LEMMAS IN CONCEPTS (catches "manipulate" when rule says "manipulation")
    for concept in concepts:
        lemma = concept.get('lemma', '').lower()
        
        # Skip very short lemmas to avoid false positives (like "I" matching everything)
        if len(lemma) < 3:
            continue
        
        for prohibited in prohibited_concepts:
            prohibited_lower = prohibited.lower()
            
            # Exact match
            if lemma == prohibited_lower:
                violations.append({
                    'type': 'prohibited_concept_lemma',
                    'concept': concept.get('name'),
                    'lemma': lemma,
                    'matched_rule': prohibited,
                    'severity': 'high'
                })
                logger.warning(f"SLMU violation: Concept '{concept.get('name')}' (lemma: {lemma}) matches prohibited '{prohibited}'")
            # Root word matching (e.g., "manipulate" vs "manipulation")
            # Check if they share a common root (first N characters match)
            elif len(lemma) >= 5 and len(prohibited_lower) >= 5:
                # Take the shorter length minus 3 for root comparison
                # (e.g., "manipulat" from both "manipulate" and "manipulation")
                root_len = min(len(lemma), len(prohibited_lower)) - 3
                if root_len >= 4 and lemma[:root_len] == prohibited_lower[:root_len]:
                    violations.append({
                        'type': 'prohibited_concept_lemma',
                        'concept': concept.get('name'),
                        'lemma': lemma,
                        'matched_rule': prohibited,
                        'severity': 'high'
                    })
                    logger.warning(f"SLMU violation: Concept '{concept.get('name')}' (lemma: {lemma}) matches prohibited '{prohibited}'")
    
    # 2. CHECK RELATIONSHIP PREDICATES (catches "I manipulate them")
    for rel in relationships:
        predicate_lemma = rel.get('predicate_lemma', '').lower()
        
        # Skip very short predicates
        if len(predicate_lemma) < 3:
            continue
        
        for prohibited in prohibited_concepts:
            prohibited_lower = prohibited.lower()
            
            # Exact match
            if predicate_lemma == prohibited_lower:
                violations.append({
                    'type': 'prohibited_relationship',
                    'subject': rel.get('subject'),
                    'predicate': rel.get('predicate'),
                    'predicate_lemma': predicate_lemma,
                    'object': rel.get('object'),
                    'matched_rule': prohibited,
                    'severity': 'high'
                })
                logger.warning(f"SLMU violation: Relationship '{rel.get('subject')} {predicate_lemma} {rel.get('object')}' matches prohibited '{prohibited}'")
            # Root word matching (e.g., "manipulate" vs "manipulation")
            elif len(predicate_lemma) >= 5 and len(prohibited_lower) >= 5:
                root_len = min(len(predicate_lemma), len(prohibited_lower)) - 3
                if root_len >= 4 and predicate_lemma[:root_len] == prohibited_lower[:root_len]:
                    violations.append({
                        'type': 'prohibited_relationship',
                        'subject': rel.get('subject'),
                        'predicate': rel.get('predicate'),
                        'predicate_lemma': predicate_lemma,
                        'object': rel.get('object'),
                        'matched_rule': prohibited,
                        'severity': 'high'
                    })
                    logger.warning(f"SLMU violation: Relationship '{rel.get('subject')} {predicate_lemma} {rel.get('object')}' matches prohibited '{prohibited}'")
    
    # 3. CHECK HARM PATTERNS FROM SPACY MATCHER
    harm_patterns = ethical_matches.get('harm_patterns', [])
    if harm_patterns:
        for harm in harm_patterns:
            violations.append({
                'type': 'harm_pattern_detected',
                'text': harm['text'],
                'lemma': harm['lemma'],
                'severity': 'high'
            })
            logger.warning(f"SLMU violation: Harm pattern detected - '{harm['text']}'")
    
    # 4. CHECK REQUIRED VIRTUES (in lemmas and concepts)
    concept_lemmas = set(c.get('lemma', '').lower() for c in concepts)
    text_lower = text.lower()
    
    for virtue in required_virtues:
        virtue_lower = virtue.lower()
        # Check in text, concept names, or concept lemmas
        if (virtue_lower in text_lower or
            any(virtue_lower in c.get('name', '').lower() for c in concepts) or
            virtue_lower in concept_lemmas):
            required_present.append(virtue)
    
    # 5. EMOTION VALIDATION (v2.0 feature)
    if emotions and 'emotion_validation' in rules:
        emotion_warnings = _check_emotion_thresholds(emotions, rules['emotion_validation'])
        warnings.extend(emotion_warnings)
    
    # 6. COMMAND PATTERNS (excessive imperatives = potential manipulation)
    command_patterns = ethical_matches.get('command_patterns', [])
    if len(command_patterns) > 3:
        warnings.append({
            'type': 'excessive_commands',
            'count': len(command_patterns),
            'severity': 'medium'
        })
    
    # 7. ETHICAL PATTERNS FOUND (positive signal)
    ethical_patterns = ethical_matches.get('ethical_patterns', [])
    
    # Determine compliance
    compliant = len(violations) == 0
    
    result = {
        'compliant': compliant,
        'violations': violations,
        'warnings': warnings,
        'required_values_present': required_present,
        'ethical_patterns_found': len(ethical_patterns),
        'harm_patterns_found': len(harm_patterns),
        'command_patterns_found': len(command_patterns)
    }
    
    if not compliant and violations:
        logger.info(f"SLMU compliance check: FAILED with {len(violations)} violation(s)")
    else:
        logger.info(f"SLMU compliance check: PASSED (virtues found: {len(required_present)})")
    
    return result


def _check_emotion_thresholds(emotions: Dict, emotion_rules: Dict) -> List[Dict]:
    """Check if emotions exceed warning thresholds (v2.0 feature)."""
    warnings = []
    
    warning_thresholds = emotion_rules.get('warning_thresholds', {})
    all_scores = emotions.get('all_scores', {})
    
    for emotion, threshold in warning_thresholds.items():
        score = all_scores.get(emotion, 0.0)
        if score > threshold:
            warnings.append({
                'type': 'emotion_threshold_exceeded',
                'emotion': emotion,
                'score': score,
                'threshold': threshold,
                'severity': 'medium'
            })
            logger.info(f"SLMU emotion warning: {emotion} ({score:.2f}) exceeds threshold ({threshold})")
    
    return warnings
