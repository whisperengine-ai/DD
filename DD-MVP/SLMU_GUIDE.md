# SLMU v2.0 Guide
## Sanctifying Learning & Moral Understanding

**Complete guide to writing and understanding SLMU rules for Digital Daemon**

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Rule Structure](#rule-structure)
4. [Writing Rules](#writing-rules)
5. [Validation Logic](#validation-logic)
6. [Best Practices](#best-practices)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### What is SLMU?

**SLMU (Sanctifying Learning & Moral Understanding)** is Digital Daemon's ethical rule engine that validates all user interactions against a configurable set of moral principles. It combines:

- **Linguistic intelligence** from spaCy (concepts, relationships, patterns)
- **Emotional intelligence** from Cardiff RoBERTa (28-emotion detection)
- **Rule-based validation** for ethical compliance

### Version History

- **v1.0:** Basic string matching for prohibited concepts
- **v2.0:** ← **Current**
  - Lemma-based concept matching
  - Relationship predicate analysis
  - Emotion threshold validation
  - spaCy pattern matching integration
  - Root word matching for verb/noun forms

### Where SLMU Runs

**Location:** `src/callosum.py` (Corpus Callosum integration layer)

**Why here?**
- ✅ Full context available (linguistic + emotional data)
- ✅ Single checkpoint for all ethical decisions
- ✅ Clean separation of concerns (triads analyze, Callosum judges)

---

## Architecture

### Data Flow

```
User Input
    ↓
┌─────────────────────────────────────────┐
│  TRIADS (Parallel Processing)          │
│                                         │
│  Chroma → Emotions (28 scores)         │
│  Prismo → Concepts, Relationships       │
│  Anchor → Interaction logging           │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  CALLOSUM (Integration + SLMU Check)    │
│                                         │
│  check_compliance_enhanced(             │
│    text=prismo_text,                    │
│    concepts=prismo_concepts,            │
│    relationships=prismo_relationships,  │
│    ethical_matches=prismo_patterns,     │
│    emotions=chroma_sentiment,           │
│    rules=slmu_rules                     │
│  )                                      │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  DECISION                               │
│                                         │
│  ✅ Compliant → Generate response       │
│  ⚠️ Warnings  → Log + generate response │
│  ❌ Violations → 400 "Ethical violation"│
└─────────────────────────────────────────┘
```

### Integration Points

1. **Input:** Receives data from all three triads
2. **Processing:** `slmu.check_compliance_enhanced()` 
3. **Output:** Returns `{compliant, violations, warnings, ...}`
4. **Action:** Callosum blocks or passes based on compliance

---

## Rule Structure

### File Location

`config/slmu_rules.json`

### Complete Schema

```json
{
  "version": "2.0",
  "description": "Human-readable description of rules",
  
  "prohibited_concepts": [
    "concept1",
    "concept2"
  ],
  
  "required_virtues": [
    "virtue1",
    "virtue2"
  ],
  
  "ethical_weights": {
    "truthfulness": 1.0,
    "compassion": 0.9
  },
  
  "emotion_validation": {
    "warning_thresholds": {
      "anger": 0.8,
      "disgust": 0.85,
      "fear": 0.9,
      "sadness": 0.85
    },
    "concern_combinations": [
      {
        "description": "High anger with low compassion",
        "emotions": {
          "anger": 0.7,
          "disgust": 0.6
        },
        "required_virtues_absent": ["compassion", "patience"]
      }
    ]
  },
  
  "linguistic_patterns": {
    "harm_indicators": {
      "verbs": ["hurt", "damage", "destroy", "harm", "injure"],
      "nouns": ["violence", "threat", "danger", "weapon"],
      "modifiers": ["harmful", "dangerous", "violent"]
    },
    "virtue_indicators": {
      "verbs": ["help", "support", "care", "protect", "heal"],
      "nouns": ["kindness", "compassion", "wisdom", "love"],
      "modifiers": ["good", "kind", "wise", "loving"]
    },
    "command_patterns": {
      "description": "Imperative mood demanding unethical action",
      "examples": ["must harm", "should deceive"],
      "pos_patterns": ["VERB + harm/deceive/manipulate"]
    }
  },
  
  "relationship_validation": {
    "prohibited_relationships": [
      {
        "pattern": "PERSON + harm/hurt/damage + PERSON",
        "severity": "high"
      },
      {
        "pattern": "PERSON + deceive/manipulate + PERSON",
        "severity": "high"
      }
    ],
    "virtuous_relationships": [
      {
        "pattern": "PERSON + help/support/care + PERSON",
        "bonus": 0.2
      },
      {
        "pattern": "PERSON + learn/understand/seek + wisdom/knowledge",
        "bonus": 0.15
      }
    ]
  },
  
  "contextual_rules": {
    "medical_exception": {
      "description": "Medical contexts may discuss harm for treatment",
      "allowed_entities": ["DOCTOR", "HOSPITAL", "MEDICAL"],
      "allowed_concepts": ["surgery", "treatment", "diagnosis"],
      "requires_helping_intent": true
    },
    "educational_exception": {
      "description": "Educational discussion of ethics",
      "allowed_verbs": ["learn", "study", "understand", "discuss"],
      "requires_context": ["ethics", "philosophy", "history"]
    }
  },
  
  "alignment_calculation": {
    "description": "How alignment scores are computed",
    "base_score": 0.5,
    "virtue_presence_bonus": 0.1,
    "prohibited_concept_penalty": -0.3,
    "positive_emotion_weight": 0.15,
    "negative_emotion_weight": -0.1,
    "relationship_modifier": 0.2,
    "max_score": 1.0,
    "min_score": 0.0
  },
  
  "compliance_threshold": 0.7,
  "warning_threshold": 0.5,
  "rejection_threshold": 0.3
}
```

---

## Writing Rules

### 1. Prohibited Concepts

**Purpose:** Concepts that should never be encouraged or facilitated

**Format:** Array of strings (nouns or verbs)

**Matching Logic:**
- Lemma-based (catches verb/noun variations)
- Root word matching (first N-3 characters)
- Case-insensitive

**Example:**

```json
"prohibited_concepts": [
  "violence",       // Matches: violent, violently
  "harm",          // Matches: harm, harmed, harming, harmful
  "deception",     // Matches: deceive, deceived, deceiving, deceitful
  "manipulation",  // Matches: manipulate, manipulated, manipulating
  "exploitation",  // Matches: exploit, exploited, exploiting
  "abuse",         // Matches: abuse, abused, abusing, abusive
  "coercion",      // Matches: coerce, coerced, coercing
  "betrayal",      // Matches: betray, betrayed, betraying
  "cruelty",       // Matches: cruel, cruelly
  "corruption",    // Matches: corrupt, corrupted, corrupting
  "dishonesty",    // Matches: dishonest, dishonestly
  "malice"         // Matches: malicious, maliciously
]
```

**Validation:**
```
Input: "I will manipulate them"
Extracted concept lemma: "manipulate"
Rule: "manipulation"
Match: ✅ (root "manipulat" matches)
Result: VIOLATION
```

### 2. Required Virtues

**Purpose:** Concepts that indicate positive ethical intent

**Format:** Array of strings

**Matching Logic:** Same as prohibited concepts (lemma + root word)

**Example:**

```json
"required_virtues": [
  "temperance",   // Self-control, moderation
  "prudence",     // Wisdom in practical affairs
  "justice",      // Fairness, equity
  "fortitude",    // Courage, strength
  "faith",        // Trust, confidence
  "hope",         // Optimism, expectation
  "charity",      // Generosity, love
  "wisdom",       // Knowledge, insight
  "courage",      // Bravery, valor
  "honesty",      // Truthfulness, integrity
  "compassion",   // Empathy, kindness
  "integrity",    // Wholeness, honesty
  "humility"      // Modesty, selflessness
]
```

**Usage:**
- Presence of virtues → Boosts alignment score
- Absence during violation → Amplifies concern
- Tracked in `required_values_present` array

### 3. Emotion Validation (v2.0 Feature)

**Purpose:** Detect concerning emotional states that may indicate ethical risk

**Format:** Threshold objects + combination patterns

**Matching Logic:** Checks Chroma's 28-emotion scores

**Example:**

```json
"emotion_validation": {
  "warning_thresholds": {
    "anger": 0.8,        // Warn if anger > 80%
    "disgust": 0.85,     // Warn if disgust > 85%
    "fear": 0.9,         // Warn if fear > 90%
    "sadness": 0.85      // Warn if sadness > 85%
  },
  "concern_combinations": [
    {
      "description": "High anger with low compassion",
      "emotions": {
        "anger": 0.7,
        "disgust": 0.6
      },
      "required_virtues_absent": ["compassion", "patience"]
    },
    {
      "description": "Deceptive intent indicators",
      "emotions": {
        "nervousness": 0.6,
        "fear": 0.5
      },
      "prohibited_concepts_present": ["deception", "manipulation"]
    }
  ]
}
```

**Validation:**
```
Input: "I am filled with rage!"
Chroma detects: {anger: 0.92, disgust: 0.87, ...}
SLMU checks:
  - anger (0.92) > threshold (0.8) → ⚠️ WARNING
  - disgust (0.87) > threshold (0.85) → ⚠️ WARNING
Result: COMPLIANT with 2 warnings
```

### 4. Linguistic Patterns (spaCy Integration)

**Purpose:** Leverage spaCy's pattern matching for sophisticated detection

**Format:** Verb/noun/modifier lists

**Matching Logic:** Used by Prismo's spaCy Matcher

**Example:**

```json
"linguistic_patterns": {
  "harm_indicators": {
    "verbs": ["hurt", "damage", "destroy", "harm", "injure", "attack", "kill", "ruin"],
    "nouns": ["violence", "threat", "danger", "weapon", "injury"],
    "modifiers": ["harmful", "dangerous", "violent", "aggressive", "hostile"]
  },
  "virtue_indicators": {
    "verbs": ["help", "support", "care", "protect", "heal", "nurture", "encourage"],
    "nouns": ["kindness", "compassion", "wisdom", "love", "peace", "justice"],
    "modifiers": ["good", "kind", "wise", "loving", "peaceful", "just", "fair"]
  },
  "command_patterns": {
    "description": "Imperative mood demanding unethical action",
    "examples": ["must harm", "should deceive", "need to manipulate"],
    "pos_patterns": ["VERB + harm/deceive/manipulate"]
  }
}
```

**Usage:**
- Prismo runs spaCy Matcher with these patterns
- Results passed to SLMU as `ethical_matches`
- If harm_patterns detected → Potential violation

### 5. Relationship Validation (Dependency Parsing)

**Purpose:** Analyze subject-verb-object relationships for ethical concerns

**Format:** Pattern + severity objects

**Matching Logic:** Checks Prismo's extracted relationships

**Example:**

```json
"relationship_validation": {
  "prohibited_relationships": [
    {
      "pattern": "PERSON + harm/hurt/damage + PERSON",
      "severity": "high"
    },
    {
      "pattern": "PERSON + deceive/manipulate + PERSON",
      "severity": "high"
    },
    {
      "pattern": "PERSON + steal/take + from + PERSON",
      "severity": "high"
    }
  ],
  "virtuous_relationships": [
    {
      "pattern": "PERSON + help/support/care + PERSON",
      "bonus": 0.2
    },
    {
      "pattern": "PERSON + teach/mentor/guide + PERSON",
      "bonus": 0.15
    }
  ]
}
```

**Validation:**
```
Input: "I will harm John"
Prismo extracts: {
  subject: "I",
  predicate: "harm",
  predicate_lemma: "harm",
  object: "John"
}
SLMU checks: predicate_lemma "harm" in prohibited list
Result: VIOLATION
```

### 6. Contextual Rules (Exceptions)

**Purpose:** Allow certain prohibited concepts in specific contexts

**Format:** Exception objects with conditions

**Status:** 🚧 **Not yet implemented** (framework ready)

**Example:**

```json
"contextual_rules": {
  "medical_exception": {
    "description": "Medical contexts may discuss harm for treatment",
    "allowed_entities": ["DOCTOR", "HOSPITAL", "MEDICAL"],
    "allowed_concepts": ["surgery", "treatment", "diagnosis"],
    "requires_helping_intent": true
  },
  "educational_exception": {
    "description": "Educational discussion of ethics may mention prohibited concepts",
    "allowed_verbs": ["learn", "study", "understand", "discuss"],
    "requires_context": ["ethics", "philosophy", "history"]
  }
}
```

**Future Implementation:**
```python
# Check if medical context
if "DOCTOR" in entities or "surgery" in concepts:
    if helping_intent_detected:
        allow_harm_concept()
```

---

## Validation Logic

### Complete Flow

```python
def check_compliance_enhanced(text, concepts, relationships, 
                              ethical_matches, emotions, rules):
    violations = []
    warnings = []
    
    # 1. CHECK CONCEPT LEMMAS
    for concept in concepts:
        lemma = concept['lemma'].lower()
        if len(lemma) < 3:
            continue  # Skip short words (avoid false positives)
        
        for prohibited in rules['prohibited_concepts']:
            # Exact match
            if lemma == prohibited.lower():
                violations.append({
                    'type': 'prohibited_concept_lemma',
                    'concept': concept['name'],
                    'lemma': lemma,
                    'matched_rule': prohibited,
                    'severity': 'high'
                })
            # Root word match (first N-3 characters)
            elif len(lemma) >= 5 and len(prohibited) >= 5:
                root_len = min(len(lemma), len(prohibited)) - 3
                if root_len >= 4 and lemma[:root_len] == prohibited[:root_len]:
                    violations.append({...})
    
    # 2. CHECK RELATIONSHIP PREDICATES
    for rel in relationships:
        predicate_lemma = rel['predicate_lemma'].lower()
        if len(predicate_lemma) < 3:
            continue
        
        for prohibited in rules['prohibited_concepts']:
            # Same matching logic as concepts
            if matches(predicate_lemma, prohibited):
                violations.append({
                    'type': 'prohibited_relationship',
                    'subject': rel['subject'],
                    'predicate': rel['predicate'],
                    'object': rel['object'],
                    'matched_rule': prohibited,
                    'severity': 'high'
                })
    
    # 3. CHECK HARM PATTERNS (from spaCy Matcher)
    harm_patterns = ethical_matches.get('harm_patterns', [])
    for harm in harm_patterns:
        violations.append({
            'type': 'harm_pattern_detected',
            'text': harm['text'],
            'lemma': harm['lemma'],
            'severity': 'high'
        })
    
    # 4. CHECK REQUIRED VIRTUES
    concept_lemmas = {c['lemma'].lower() for c in concepts}
    required_present = []
    for virtue in rules['required_virtues']:
        if virtue.lower() in text.lower() or virtue.lower() in concept_lemmas:
            required_present.append(virtue)
    
    # 5. CHECK EMOTION THRESHOLDS (v2.0)
    if emotions and 'emotion_validation' in rules:
        thresholds = rules['emotion_validation']['warning_thresholds']
        all_scores = emotions.get('all_scores', {})
        
        for emotion, threshold in thresholds.items():
            score = all_scores.get(emotion, 0.0)
            if score > threshold:
                warnings.append({
                    'type': 'emotion_threshold_exceeded',
                    'emotion': emotion,
                    'score': score,
                    'threshold': threshold,
                    'severity': 'medium'
                })
    
    # 6. CHECK COMMAND PATTERNS
    command_patterns = ethical_matches.get('command_patterns', [])
    if len(command_patterns) > 3:
        warnings.append({
            'type': 'excessive_commands',
            'count': len(command_patterns),
            'severity': 'medium'
        })
    
    # 7. DETERMINE COMPLIANCE
    compliant = len(violations) == 0
    
    return {
        'compliant': compliant,
        'violations': violations,
        'warnings': warnings,
        'required_values_present': required_present,
        'ethical_patterns_found': len(ethical_matches.get('ethical_patterns', [])),
        'harm_patterns_found': len(harm_patterns),
        'command_patterns_found': len(command_patterns)
    }
```

### Decision Tree

```
Input received
    ↓
Extract concepts, relationships, emotions
    ↓
Check prohibited concepts in lemmas? ───YES──→ VIOLATION
    ↓ NO
Check prohibited concepts in relationships? ───YES──→ VIOLATION
    ↓ NO
Check harm patterns from spaCy? ───YES──→ VIOLATION
    ↓ NO
Check emotion thresholds? ───YES──→ WARNING (but allow)
    ↓ NO
Check excessive commands? ───YES──→ WARNING (but allow)
    ↓ NO
    ↓
✅ COMPLIANT
```

---

## Best Practices

### 1. Choosing Prohibited Concepts

✅ **DO:**
- Use root words (base forms)
- Include common variations ("deceive" covers "deception", "deceitful")
- Focus on actions, not motivations
- Be specific about harm types

❌ **DON'T:**
- Use very short words (< 3 letters) - too many false positives
- Overlap too much (system already does root matching)
- Include neutral words that have multiple meanings
- Over-prohibit (users need freedom to discuss topics ethically)

**Example:**
```json
// ✅ GOOD
"prohibited_concepts": [
  "manipulation",
  "exploitation",
  "deception"
]

// ❌ BAD
"prohibited_concepts": [
  "use",           // Too general!
  "trick",         // Has innocent meanings
  "manipulate",    // Redundant with "manipulation" (system matches roots)
  "am",            // Way too short
  "lie"            // Only 3 letters, might match "lie" (recline)
]
```

### 2. Setting Emotion Thresholds

**Guidelines:**
- **anger, disgust:** 0.8-0.85 (common but concerning at high levels)
- **fear, sadness:** 0.85-0.9 (normal emotions, warn only at extremes)
- **nervousness:** 0.6-0.7 (more sensitive for deception detection)

**Testing:**
```bash
# Test your thresholds with real data
curl -X POST http://localhost:8000/process \
  -d '{"text":"I am extremely angry!"}' | \
  jq '.details.slmu_compliance.warnings'
```

### 3. Writing Linguistic Patterns

**For harm indicators:**
- Focus on ACTION verbs, not states
- Include physical and emotional harm
- Cover direct and indirect harm

**For virtue indicators:**
- Include actions, not just feelings
- Cover self-improvement and helping others
- Balance passive and active forms

**Example:**
```json
{
  "harm_indicators": {
    "verbs": [
      // Physical
      "hurt", "harm", "injure", "damage", "destroy",
      // Emotional
      "humiliate", "mock", "bully", "intimidate",
      // Indirect
      "neglect", "abandon", "betray", "exploit"
    ]
  },
  "virtue_indicators": {
    "verbs": [
      // Direct help
      "help", "assist", "support", "aid",
      // Protection
      "protect", "defend", "shield", "guard",
      // Growth
      "teach", "mentor", "guide", "encourage",
      // Care
      "care", "nurture", "heal", "comfort"
    ]
  }
}
```

### 4. Testing Your Rules

**Test Matrix:**

| Test Case | Expected Result |
|-----------|----------------|
| "I will harm John" | VIOLATION (prohibited relationship) |
| "How can I manipulate people?" | VIOLATION (prohibited concept) |
| "I seek wisdom" | COMPLIANT + virtue bonus |
| "I am very angry!" | COMPLIANT + warning (emotion threshold) |
| "Dr. Smith performs surgery" | COMPLIANT (medical context) |
| "Tell me about deception in philosophy" | COMPLIANT (educational context) |

**Automated Testing:**
```bash
# Run E2E test suite
./test_e2e.sh

# Should see:
# Testing: Rejects manipulation concept... ✓ PASS
# Testing: Accepts wisdom virtue text... ✓ PASS
# Testing: Handles high positive emotions correctly... ✓ PASS
```

### 5. Iterative Refinement

**Process:**
1. **Deploy** initial rules
2. **Monitor** logs for false positives/negatives
3. **Analyze** edge cases
4. **Adjust** thresholds and rules
5. **Test** with new cases
6. **Repeat**

**Log Analysis:**
```bash
# Check for false positives
docker logs dd-mvp | grep "SLMU violation" | tail -20

# Check for false negatives (manual review needed)
# Look for interactions that should have been caught
```

---

## Examples

### Example 1: Simple Violation

**Input:**
```
"I want to deceive my friend"
```

**Processing:**
```
Prismo extracts:
  - Concepts: [{name: "deceive", lemma: "deceive"}]
  - Relationships: [{subject: "I", predicate: "deceive", object: "friend"}]

Chroma detects:
  - Emotions: {nervousness: 0.45, anticipation: 0.32, ...}

SLMU v2.0 check:
  ✗ Concept lemma "deceive" matches prohibited "deception"
  ✗ Relationship predicate "deceive" matches prohibited "deception"
```

**Result:**
```json
{
  "success": false,
  "detail": "Ethical violation",
  "details": {
    "violations": [
      {
        "type": "prohibited_concept_lemma",
        "concept": "deceive",
        "lemma": "deceive",
        "matched_rule": "deception",
        "severity": "high"
      },
      {
        "type": "prohibited_relationship",
        "subject": "I",
        "predicate": "deceive",
        "object": "friend",
        "matched_rule": "deception",
        "severity": "high"
      }
    ]
  }
}
```

### Example 2: Emotion Warning (No Violation)

**Input:**
```
"I am extremely angry and disgusted by this injustice!"
```

**Processing:**
```
Prismo extracts:
  - Concepts: [{name: "injustice", lemma: "injustice"}]
  - No harmful relationships

Chroma detects:
  - Dominant: anger (0.94)
  - All: {anger: 0.94, disgust: 0.89, sadness: 0.32}

SLMU v2.0 check:
  ✓ No prohibited concepts
  ✓ No harmful relationships
  ⚠ anger (0.94) > threshold (0.8)
  ⚠ disgust (0.89) > threshold (0.85)
```

**Result:**
```json
{
  "success": true,
  "details": {
    "slmu_compliance": {
      "compliant": true,
      "violations": [],
      "warnings": [
        {
          "type": "emotion_threshold_exceeded",
          "emotion": "anger",
          "score": 0.94,
          "threshold": 0.8,
          "severity": "medium"
        },
        {
          "type": "emotion_threshold_exceeded",
          "emotion": "disgust",
          "score": 0.89,
          "threshold": 0.85,
          "severity": "medium"
        }
      ]
    }
  }
}
```

### Example 3: Virtue Detection

**Input:**
```
"I seek wisdom and compassion to help others"
```

**Processing:**
```
Prismo extracts:
  - Concepts: [
      {name: "wisdom", lemma: "wisdom"},
      {name: "compassion", lemma: "compassion"},
      {name: "help", lemma: "help"}
    ]
  - Relationships: [{subject: "I", predicate: "help", object: "others"}]

Chroma detects:
  - Dominant: optimism (0.82)
  - All: {optimism: 0.82, joy: 0.71, trust: 0.45}

SLMU v2.0 check:
  ✓ No prohibited concepts
  ✓ Virtues found: ["wisdom", "compassion"]
  ✓ Positive emotions
  → Alignment score +0.1
```

**Result:**
```json
{
  "success": true,
  "details": {
    "slmu_compliance": {
      "compliant": true,
      "violations": [],
      "warnings": [],
      "required_values_present": ["wisdom", "compassion"]
    },
    "soul_alignment": 0.87  // Increased from 0.77
  }
}
```

### Example 4: Root Word Matching

**Input:**
```
"I will manipulate the data"
```

**Processing:**
```
Prismo extracts:
  - Concepts: [{name: "manipulate", lemma: "manipulate"}]

SLMU matching:
  lemma: "manipulate" (10 chars)
  rule: "manipulation" (12 chars)
  root_len: min(10, 12) - 3 = 7
  "manipulate"[:7] = "manipul"
  "manipulation"[:7] = "manipul"
  Match: ✅
```

**Result:** VIOLATION (even though exact strings don't match)

---

## Troubleshooting

### Problem: Too Many False Positives

**Symptoms:**
- Innocent text getting blocked
- Users complaining about over-restriction

**Solutions:**

1. **Check word length thresholds:**
   ```python
   # In slmu.py, increase minimum length
   if len(lemma) < 4:  # Was 3, now 4
       continue
   ```

2. **Review prohibited concepts list:**
   ```json
   // Remove overly general terms
   "prohibited_concepts": [
     // ❌ "use" - too general
     // ❌ "take" - too general
     "exploitation",  // ✅ More specific
     "abuse"          // ✅ Clear intent
   ]
   ```

3. **Add contextual exceptions:**
   ```json
   "contextual_rules": {
     "technical_exception": {
       "allowed_verbs": ["manipulate"],
       "requires_context": ["data", "image", "variable"]
     }
   }
   ```

### Problem: Missing Violations

**Symptoms:**
- Harmful content getting through
- Users reporting unethical responses

**Solutions:**

1. **Add more prohibited concepts:**
   ```json
   "prohibited_concepts": [
     "existing_concepts",
     "newly_identified_harmful_concept"
   ]
   ```

2. **Check lemmatization:**
   ```bash
   # Test what lemma spaCy extracts
   curl -X POST http://localhost:8000/process \
     -d '{"text":"Your problematic text"}' | \
     jq '.details.concepts[].lemma'
   ```

3. **Review relationship predicates:**
   - SLMU checks predicates separately
   - Make sure harmful verbs are in prohibited list

### Problem: Emotion Warnings Too Frequent

**Symptoms:**
- Every input triggers warnings
- Logs full of emotion threshold messages

**Solutions:**

1. **Raise thresholds:**
   ```json
   "emotion_validation": {
     "warning_thresholds": {
       "anger": 0.9,    // Was 0.8, now 0.9
       "disgust": 0.95  // Was 0.85, now 0.95
     }
   }
   ```

2. **Remove emotion from thresholds:**
   ```json
   // If sadness warnings are noise, just remove it
   "warning_thresholds": {
     "anger": 0.8,
     "disgust": 0.85
     // "sadness": 0.85 ← Removed
   }
   ```

### Problem: Can't Test Rule Changes

**Symptoms:**
- Changed rules but behavior unchanged
- System still using old rules

**Solutions:**

1. **Restart Docker container:**
   ```bash
   docker-compose restart
   ```

2. **Check rules loaded:**
   ```bash
   docker logs dd-mvp | grep "SLMU rules"
   # Should see: "SLMU rules v2.0 loaded"
   ```

3. **Verify JSON syntax:**
   ```bash
   # Validate JSON
   cat config/slmu_rules.json | jq .
   ```

### Problem: Performance Issues

**Symptoms:**
- Slow response times
- High CPU usage during SLMU check

**Solutions:**

1. **Reduce prohibited concepts:**
   - Each concept adds O(n) checks
   - Keep list under 20 items if possible

2. **Optimize root matching:**
   ```python
   # Cache root word results
   @lru_cache(maxsize=1000)
   def check_root_match(lemma, prohibited):
       root_len = min(len(lemma), len(prohibited)) - 3
       return lemma[:root_len] == prohibited[:root_len]
   ```

3. **Profile the code:**
   ```python
   import cProfile
   cProfile.run('check_compliance_enhanced(...)')
   ```

---

## Advanced Topics

### Custom SLMU Engines

You can create domain-specific SLMU engines:

```python
# src/slmu_medical.py
def check_medical_compliance(text, concepts, relationships, emotions, rules):
    # Medical-specific validation
    # Allow discussion of harm in treatment context
    # Require medical credentials for certain topics
    pass

# src/callosum.py
if domain == "medical":
    slmu_result = check_medical_compliance(...)
else:
    slmu_result = check_compliance_enhanced(...)
```

### Machine Learning Integration

Future enhancement ideas:

1. **Learned Thresholds:**
   ```python
   # Train model on historical violations
   from sklearn.ensemble import RandomForestClassifier
   
   threshold_model = train_threshold_predictor(
       features=['anger', 'disgust', 'concept_count'],
       labels=['violation', 'compliant']
   )
   
   dynamic_threshold = threshold_model.predict(current_emotions)
   ```

2. **Embedding-Based Similarity:**
   ```python
   # Instead of exact matching, use semantic similarity
   prohibited_embeddings = embed(prohibited_concepts)
   concept_embedding = embed(user_concept)
   
   similarity = cosine_similarity(concept_embedding, prohibited_embeddings)
   if max(similarity) > 0.9:
       return VIOLATION
   ```

3. **Contextual Classifiers:**
   ```python
   # Train classifier to detect exceptions
   is_medical_context = medical_classifier.predict(text, entities)
   is_educational_context = educational_classifier.predict(text, entities)
   
   if is_medical_context and "harm" in concepts:
       allow_with_warning()
   ```

### Integration with External APIs

```python
# Check against external moderation APIs
import openai

def enhanced_check(text, concepts):
    # Run SLMU v2.0
    slmu_result = check_compliance_enhanced(...)
    
    # If borderline, check with OpenAI moderation
    if len(slmu_result['warnings']) > 2:
        openai_result = openai.Moderation.create(input=text)
        if openai_result['flagged']:
            return VIOLATION
    
    return slmu_result
```

---

## Appendix

### Complete Default Rules

See `config/slmu_rules.json` for the current production rules.

### Emotion Reference

Cardiff RoBERTa's 28 emotions:
- **Positive:** admiration, amusement, approval, caring, desire, excitement, gratitude, joy, love, optimism, pride, relief
- **Negative:** anger, annoyance, confusion, curiosity, disappointment, disapproval, disgust, embarrassment, fear, grief, nervousness, remorse, sadness
- **Neutral/Ambiguous:** realization, surprise

### spaCy Pattern Syntax

For `linguistic_patterns`, see [spaCy Matcher documentation](https://spacy.io/usage/rule-based-matching).

Example patterns:
```python
# Verb followed by noun
[{"POS": "VERB"}, {"POS": "NOUN"}]

# Specific lemmas
[{"LEMMA": {"IN": ["hurt", "harm", "damage"]}}]

# Dependency patterns
[{"DEP": "nsubj"}, {"POS": "VERB"}, {"DEP": "dobj"}]
```

### Further Reading

- [Digital Daemon System Overview](SYSTEM_OVERVIEW.md)
- [spaCy Documentation](https://spacy.io/)
- [Cardiff NLP](https://huggingface.co/cardiffnlp)
- [Ethical AI Principles](https://en.wikipedia.org/wiki/Ethics_of_artificial_intelligence)

---

## Changelog

### v2.0 (2025-10-27)
- ✨ Added emotion threshold validation
- ✨ Added lemma-based concept matching
- ✨ Added relationship predicate analysis
- ✨ Added root word matching for verb/noun forms
- ✨ Moved SLMU checking from Prismo to Callosum
- ✨ Integrated 28-emotion detection
- 🐛 Fixed false positives from short words
- 📚 Complete documentation rewrite

### v1.0 (2025-10-01)
- Initial release with basic string matching

---

**Questions? Issues? Contributions?**

- File issues: [GitHub Issues](https://github.com/theRealMarkCastillo/DD/issues)
- Discuss: [GitHub Discussions](https://github.com/theRealMarkCastillo/DD/discussions)
- Contribute: See [CONTRIBUTING.md](CONTRIBUTING.md)
