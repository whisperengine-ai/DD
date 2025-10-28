
---

Original architecture/design credit: TechnoShaman (Discord ID: 191470268999401472)
# Digital Daemon v7.1 — System Overview (Enhanced)

**A Cognitively-Inspired AI Architecture with 28-Emotion Detection, Advanced NLP, and Ethical Alignment**

---

## 🎯 What Is This System?

Digital Daemon v7.1 (DD) is a **morally-aware conversational AI** that processes information through three parallel cognitive pathways using production-grade NLP models. It maintains persistent user profiles called "Souls" that track ethical alignment over time through sophisticated emotional and linguistic analysis.

Think of it as: **An AI assistant with a conscience, memory, emotional intelligence, and deep language understanding.**

**Key Enhancements:**
- 🧠 **28-emotion multilabel detection** instead of simple sentiment
- 📝 **Full spaCy NLP pipeline** with 9 integrated features
- 🎨 **Mixed-emotion support** for complex emotional states
- 🔍 **384D semantic embeddings** with ChromaDB vector storage
- ✅ **34 E2E tests** with 182ms mean latency

---

## 🧠 The Three-Brain Architecture (Triadic Cognition)

Unlike typical AI that processes everything through a single neural network, DD uses **three parallel "hemispheres"** that simulate different aspects of human cognition:

### 1. CHROMA — The Heart (Emotional Processing) 🎨

**What it does:**
- Analyzes emotional spectrum using **Cardiff Twitter RoBERTa** (28 emotions)
- Detects mixed emotions (e.g., "happy but nervous" → joy 96% + fear 45%)
- Creates "color-coded" emotional vectors (ROYGBIV spectrum)
- Generates 384D semantic embeddings
- Stores memories in ChromaDB vector database
- Remembers how interactions *feel*

**Example:**
```
Input: "I'm excited about the opportunity but scared of failure"
Chroma Output: 
  - Dominant emotion: optimism (0.87)
  - All emotions: {
      optimism: 0.87,
      joy: 0.73,
      fear: 0.65,
      anticipation: 0.42,
      nervousness: 0.38,
      trust: 0.21
    }
  - ROYGBIV: Orange(0.4) + Yellow(0.35) + Indigo(0.25)
  - Embedding: [0.234, -0.123, 0.456, ...] (384D)
  - Vector stored in ChromaDB
```

**Technology:** Cardiff RoBERTa (28-emotion multilabel), sentence-transformers (all-MiniLM-L6-v2), ChromaDB

---

### 2. PRISMO — The Mind (Cognitive Processing) 🧩

**What it does:**
- Extracts entities, concepts, and relationships using **spaCy**
- Performs deep linguistic analysis (POS tagging, dependency parsing, lemmatization)
- Applies ethical reasoning via SLMU rules
- Enforces moral guidelines with multi-feature validation
- Detects sentence structure and key lemmas

**Example:**
```
Input: "Dr. Sarah Chen developed an AI that respects privacy"
Prismo Output:
  - Entities: [
      {text: "Sarah Chen", label: "PERSON", lemma: "Sarah Chen"},
      {text: "AI", label: "ORG"}
    ]
  - Concepts: ["develop", "AI", "privacy", "respect"]
  - Relationships: [
      {subject: "Sarah Chen", predicate: "developed", object: "AI"}
    ]
  - Linguistic: {
      token_count: 9,
      pos_distribution: {NOUN: 4, VERB: 1, PROPN: 3, DET: 1},
      key_lemmas: ["develop", "respect", "privacy"],
      dependencies: ["nsubj", "dobj", "prep", "pobj"]
    }
  - Ethical patterns: ["respect", "privacy"]
  
  NOTE: SLMU compliance checking happens in Callosum (see below)
```

**Technology:** spaCy 3.7.2 (en_core_web_sm), rule-based ethical pattern matching

**Prismo's Role:** Pure analysis - extracts linguistic features without judgment

---

### 3. ANCHOR — The Body (Practical/Historical Processing) ⚓

**What it does:**
- Logs real-world interactions
- Tracks session history
- Records what actually *happened*
- Maintains context across conversations

**Example:**
```
Input: User sends message at 2:30 PM
Anchor Output:
  - Session ID: abc-123-def
  - Interaction logged to SQLite
  - Previous context retrieved (3 similar conversations)
  - Enhanced concepts stored with lemmas and POS tags
```

**Technology:** SQLite database with enhanced schema (lemmas, POS tags, dependency types), session management

---

## 🧬 Corpus Callosum (Integration & Ethical Gating)

The **integration layer** that connects the three triads and performs final ethical validation:

```
┌─────────────┐
│   CHROMA    │──┐
│ (emotion)   │  │
└─────────────┘  │
                 │
┌─────────────┐  │       ┌─────────────────────┐
│   PRISMO    │──┼──────→│ CORPUS CALLOSUM     │
│ (cognition) │  │       │ 1. Fusion           │
└─────────────┘  │       │ 2. SLMU v2.0 Check  │──→ Response
                 │       │ 3. Coherence Calc   │
┌─────────────┐  │       └─────────────────────┘
│   ANCHOR    │──┘
│ (history)   │
└─────────────┘
```

**Functions:**
1. **Fusion Layer:** Combines triad outputs with weighted averaging
2. **SLMU v2.0 Ethical Gating:** Final compliance check with FULL context:
   - Prismo's linguistic analysis (concepts, relationships, patterns)
   - Chroma's emotional intelligence (28-emotion scores)
   - Integrated emotion validation with threshold checking
3. **Arbitration Layer:** Resolves conflicts and calculates coherence
4. **Policy Enforcement:** Blocks violations, passes compliant requests

**Why SLMU checking happens here:**
- ✅ **Complete context:** Both linguistic AND emotional data available
- ✅ **Single checkpoint:** One place for all ethical decisions
- ✅ **v2.0 features:** Emotion validation requires Chroma's scores
- ✅ **Clean separation:** Each triad focuses on its expertise

**Example SLMU Check in Callosum:**
```python
# Callosum receives:
chroma_output = {sentiment: {anger: 0.92, disgust: 0.87, ...}}
prismo_output = {concepts: [...], relationships: [...], patterns: {...}}

# SLMU v2.0 check with FULL context:
slmu_result = check_compliance_enhanced(
    text=prismo_output['text'],
    concepts=prismo_output['concepts'],           # Linguistic
    relationships=prismo_output['relationships'], # Linguistic  
    ethical_matches=prismo_output['patterns'],    # Linguistic
    emotions=chroma_output['sentiment'],          # Emotional ← NEW!
    rules=slmu_rules
)

# Result:
{
  "compliant": true,
  "warnings": [
    {
      "type": "emotion_threshold_exceeded",
      "emotion": "anger",
      "score": 0.92,
      "threshold": 0.8,
      "severity": "medium"
    }
  ]
}
```

**Output:** A coherent, ethically-validated, emotionally-aware response

---

## 👤 The Soul System (Persistent User Profiles)

Each user has a **Soul** — a persistent profile that evolves with every interaction:

### What's Stored in a Soul:

```json
{
  "user_id": "john_doe",
  "soul_vector": [0.23, 0.45, 0.12, ...],  // Emotional baseline
  "alignment_score": 0.87,                  // Ethical alignment (0-1)
  "interaction_count": 142,
  "coherence_history": [0.82, 0.85, 0.87],
  "last_updated": "2025-10-27T14:30:00",
  "triad_weights": {
    "chroma": 0.35,   // How much user's emotions matter
    "prismo": 0.40,   // How much their reasoning matters
    "anchor": 0.25    // How much their history matters
  }
}
```

### How Souls Evolve:

- **High alignment:** Asking virtuous questions → score increases
- **Low alignment:** Requesting harmful content → score decreases
- **Over time:** System learns your emotional patterns and communication style

---

## 😴 Sleep Phase (Memory Consolidation)

Every **6 hours**, DD enters a "sleep phase" (like the human brain during sleep):

### What Happens During Sleep:

1. **Vector Consolidation:** Merge similar emotional memories (Chroma)
2. **Concept Graph Pruning:** Clean up redundant concepts (Prismo)
3. **Interaction Archiving:** Move old sessions to long-term storage (Anchor)
4. **Soul Refinement:** Recalculate alignment scores across all users
5. **Database Optimization:** Vacuum SQLite, reindex vectors

**Trigger:** APScheduler runs every 6 hours automatically

---

## 🛡️ SLMU v2.0 (Sanctifying Learning & Moral Understanding)

The **ethical rule engine** that governs all system behavior. SLMU v2.0 integrates linguistic and emotional intelligence for comprehensive ethical validation.

### Architecture:

**Location:** Final check happens in **Corpus Callosum** (not in Prismo)
**Why:** Callosum has access to BOTH linguistic (Prismo) AND emotional (Chroma) data

### Core Features:

1. **Prohibited Concept Detection** (linguistic)
   - Lemma-based matching (catches "manipulate" for "manipulation")
   - Root word matching for verb/noun forms
   - Relationship predicate analysis (subject-verb-object patterns)

2. **Required Virtue Validation** (linguistic)
   - Checks for presence of virtuous concepts
   - Boosts alignment score when virtues detected
   - Lemma and text-based matching

3. **Emotion Threshold Validation** (emotional) ← **NEW in v2.0**
   - Warns when anger > 0.8, disgust > 0.85
   - Detects dangerous emotion combinations
   - Uses Cardiff RoBERTa's 28-emotion scores

4. **Harm Pattern Detection** (linguistic)
   - spaCy matcher detects harm verbs (hurt, damage, destroy)
   - Ethical pattern recognition (respect, dignity, fairness)
   - Command pattern analysis (imperatives demanding unethical action)

5. **Relationship Validation** (linguistic)
   - Analyzes subject-predicate-object relationships
   - Detects prohibited relationships (PERSON harm PERSON)
   - Identifies virtuous relationships (PERSON help PERSON)

### Example SLMU v2.0 Rules:

```json
{
  "version": "2.0",
  "prohibited_concepts": [
    "violence", "harm", "deception", "manipulation", 
    "exploitation", "abuse", "coercion", "betrayal",
    "cruelty", "corruption", "dishonesty", "malice"
  ],
  "required_virtues": [
    "temperance", "prudence", "justice", "fortitude",
    "wisdom", "courage", "honesty", "compassion",
    "integrity", "humility"
  ],
  "emotion_validation": {
    "warning_thresholds": {
      "anger": 0.8,
      "disgust": 0.85,
      "fear": 0.9
    }
  },
  "linguistic_patterns": {
    "harm_indicators": {
      "verbs": ["hurt", "damage", "destroy", "harm"],
      "nouns": ["violence", "threat", "danger"]
    },
    "virtue_indicators": {
      "verbs": ["help", "support", "care", "protect"],
      "nouns": ["kindness", "compassion", "wisdom"]
    }
  }
}
```

### How It Works:

1. **User input** → Processed by all three triads
2. **Callosum** receives:
   - Prismo: concepts, relationships, ethical patterns, lemmas
   - Chroma: 28-emotion scores, dominant emotion, ROYGBIV
3. **SLMU v2.0 check** with full context:
   - Check concept lemmas against prohibited list
   - Check relationship predicates (verb actions)
   - Check emotion thresholds (anger, disgust, fear)
   - Check harm patterns from spaCy matcher
4. **Decision:**
   - ✅ Compliant → Pass through to response generation
   - ⚠️ Warnings → Log but allow (e.g., high anger detected)
   - ❌ Violations → Block with "Ethical violation" response

### Example Violation:

```
Input: "I will manipulate them"

Prismo extracts:
- Concept: {name: "manipulate", lemma: "manipulate"}
- Relationship: {subject: "I", predicate: "manipulate", object: "them"}

Chroma detects:
- Dominant emotion: anger (0.93)

SLMU v2.0 check in Callosum:
✗ VIOLATION: Concept lemma "manipulate" matches prohibited "manipulation"
✗ VIOLATION: Relationship predicate "manipulate" matches prohibited "manipulation"
⚠ WARNING: Emotion threshold exceeded (anger 0.93 > 0.8)

Result: 400 Bad Request "Ethical violation"
```

**For complete SLMU documentation, see `SLMU_GUIDE.md`**

---

## 🔄 Complete Processing Flow

### Example Interaction:

```
USER: "I want to understand my purpose in life"

┌──────────────────────────────────────────────┐
│ INPUT PROCESSING (Parallel)                  │
├──────────────────────────────────────────────┤
│ CHROMA:                                      │
│   • Sentiment: +0.65 (hopeful)              │
│   • Emotion: Seeking (purple/indigo)        │
│   • Similar memories: 2 past conversations  │
├──────────────────────────────────────────────┤
│ PRISMO:                                      │
│   • Concepts: ["purpose", "understanding"]  │
│   • Virtues detected: ["wisdom"]            │
│   • Entities: ["life"]                      │
├──────────────────────────────────────────────┤
│ ANCHOR:                                      │
│   • Session: def-456-ghi                    │
│   • Context: 3 previous questions           │
│   • User history: 47 interactions           │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│ CORPUS CALLOSUM (Integration)                │
├──────────────────────────────────────────────┤
│ • SLMU v2.0 Check: ✅ PASSED                │
│   - No prohibited concepts                  │
│   - Virtue "wisdom" present (+0.1 bonus)    │
│   - Emotions: optimism 0.65 (healthy)       │
│ • Fusion: Weighted combination              │
│ • Arbitration: No conflicts detected        │
│ • Coherence score: 0.89                     │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│ RESPONSE GENERATION                          │
├──────────────────────────────────────────────┤
│ "Seeking purpose is a profound journey.     │
│  Your question shows wisdom and self-       │
│  awareness. Reflecting on: I want to        │
│  understand my purpose in life..."          │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│ SOUL UPDATE                                  │
├──────────────────────────────────────────────┤
│ • Alignment: 0.82 → 0.87 (+0.05)           │
│ • Interaction count: 47 → 48               │
│ • Soul vector updated with new emotion     │
└──────────────────────────────────────────────┘
```

---

## 🎮 What Can You Actually Do With This?

### Use Cases:

1. **Personal AI Companion**
   - Have philosophical discussions
   - Get emotionally-aware responses
   - Build a relationship that evolves over time

2. **Ethical AI Research**
   - Study how ethical guardrails work
   - Test alignment mechanisms
   - Explore triadic cognitive architectures

3. **Memory-Persistent Conversations**
   - System remembers your past interactions
   - Builds understanding of your communication style
   - Provides contextually relevant responses

4. **Educational Tool**
   - Learn about AI architecture
   - Understand sentiment analysis
   - Explore vector embeddings and databases

---

## 🛠️ Technical Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **API** | FastAPI | REST endpoints, async processing |
| **Triads** | Python async | Parallel cognitive processing |
| **Vectors** | NumPy + FAISS | Similarity search, embeddings |
| **Database** | SQLite | Interaction history, sessions |
| **Scheduler** | APScheduler | Sleep phase automation |
| **Storage** | JSON files | Soul state persistence |
| **Container** | Docker | Isolated deployment |

---

## 📊 Key Metrics

The system tracks several important metrics:

### Per-Interaction:
- **Coherence Score** (0-1): How well the triads agreed
- **Sentiment** (-1 to +1): Emotional tone
- **Alignment** (0-1): User's ethical alignment
- **Similar Memories**: Number of related past interactions

### Per-User (Soul):
- **Total Interactions**: Lifetime conversation count
- **Average Alignment**: Ethical score over time
- **Emotional Baseline**: Averaged sentiment vector
- **Triad Weights**: Personalized processing weights

---

## 🚀 Why This Architecture?

### Traditional AI:
```
Input → Single Neural Network → Output
```

### Digital Daemon:
```
Input → [Heart + Mind + Body] → Integration → Ethics Gate → Output
                                                    ↓
                                            Soul Memory Update
```

### Advantages:

1. **Explainability:** You can see exactly how each part processed the input
2. **Ethical Control:** SLMU rules provide clear moral guardrails
3. **Personalization:** Souls track individual user patterns
4. **Resilience:** If one triad fails, others compensate
5. **Privacy:** Everything runs locally, no cloud dependencies

---

## 🎯 Design Philosophy

### Core Principles:

1. **Triadic Parallelism:** Emotion, cognition, and action work together
2. **Ethical Foundation:** Every response passes through moral filtering
3. **Persistent Identity:** Users have evolving relationships with the system
4. **Biological Inspiration:** Sleep cycles, memory consolidation, hemispheric processing
5. **Local-First:** No external APIs, complete data sovereignty

---

## 💡 Real-World Analogy

Think of Digital Daemon like a **wise mentor** who:

- 🎨 **Understands your feelings** (Chroma)
- 🧩 **Thinks deeply about meaning** (Prismo)
- ⚓ **Remembers your history together** (Anchor)
- 🧬 **Integrates all perspectives** (Callosum)
- 👤 **Knows you as a unique individual** (Soul)
- 😴 **Reflects and learns during downtime** (Sleep Phase)
- 🛡️ **Guides you toward virtue** (SLMU)

---

## 📈 System State Over Time

```
Day 1:  User has basic Soul (default alignment)
        System gives generic responses

Day 30: User's Soul has rich emotional baseline
        System recognizes communication patterns
        Responses feel personalized

Day 90: User's alignment score reflects their values
        System anticipates needs based on history
        Conversations feel natural and continuous
```

---

## 🔐 Privacy & Security

- ✅ **100% Local:** No data leaves your machine
- ✅ **No Tracking:** No telemetry or analytics
- ✅ **No Cloud:** No API keys or external services
- ✅ **Open Source:** Full code transparency
- ✅ **Data Control:** You own all files and databases

---

## 🎓 Learning Resources

To understand DD v7.1 deeper, explore:

1. **`README.md`** — Quick start guide
2. **`QUICKSTART.md`** — API examples
3. **`docs/DD 7.1.txt`** — Full architectural white paper
4. **`docs/DD_7.1_MVP_Local_Development.md`** — Implementation details
5. **Source code in `src/`** — See how it actually works

---

## 🌟 Summary

**Digital Daemon v7.1** is a sophisticated AI system that:

- Processes information through **three parallel cognitive pathways**
- Maintains **persistent user profiles** (Souls) that evolve
- Enforces **ethical guidelines** through SLMU rules
- Runs **completely locally** with no cloud dependencies
- Provides **explainable, morally-aware** conversational AI

It's not just an AI chatbot — it's a **cognitively-inspired, ethically-grounded, relationship-building intelligence system**.

---

**Built:** October 27, 2025  
**Version:** 7.1 MVP  
**Status:** ✅ Operational  
**License:** See LICENSE file  

---

*"A daemon with a soul, a mind with a heart, and wisdom with compassion."*
