
---

Original architecture/design credit: TechnoShaman (Discord ID: 191470268999401472)
# Digital Daemon v7.1 — Enhanced MVP

A production-grade implementation of the Digital Daemon triadic cognitive architecture with 28-emotion NLP, comprehensive spaCy pipeline, and ethical alignment.

## 🎯 Overview

This MVP runs entirely on your local machine using Docker Compose. It implements the complete triadic cognitive model (Chroma, Prismo, Anchor) with Corpus Callosum fusion, Soul persistence, and advanced NLP processing.

**What You Get:**
- ✅ Three cognitive triads working in coordination
- ✅ **28-emotion multilabel detection** (Cardiff RoBERTa) - joy, fear, anger, optimism, sadness, love, and 22+ more
- ✅ **Full spaCy NLP pipeline** - NER, POS tagging, dependency parsing, lemmatization, sentence boundary detection
- ✅ **Mixed-emotion support** - Handles complex emotional states (e.g., "happy but nervous")
- ✅ **384D semantic embeddings** with ChromaDB vector storage
- ✅ Ethical alignment via SLMU rules with multi-feature validation
- ✅ Persistent user "souls" tracking alignment over time
- ✅ Automated sleep phase for system maintenance
- ✅ REST API with comprehensive endpoints
- ✅ Complete logging and monitoring
- ✅ **34 E2E tests (100% passing)** with performance benchmarking

**Cost:** $0 (runs locally)  
**Performance:** 182ms mean latency, 6 req/s concurrent throughput  
**Hardware:** 16GB RAM recommended, 4+ cores, 50GB disk (includes 1.4GB ML models)

## � Document guide (Table of contents)

A friendly map of every guide in this folder (DD-MVP). Each link explains what it is and why you might care.

- [README.md](./README.md) — The main guide. Value: start here for what the system does, how to run it, and how to use the API.
- [QUICKSTART.md](./QUICKSTART.md) — Step‑by‑step setup. Value: quickest path to a working system (Docker or native).
- [QUICKREF.md](./QUICKREF.md) — Cheat sheet. Value: handy list of commands, endpoints, and tips at a glance.
- [SYSTEM_OVERVIEW.md](./SYSTEM_OVERVIEW.md) — Big‑picture tour. Value: understand the moving parts in plain language.
- [DEMO_REPORT.md](./DEMO_REPORT.md) — What the demo shows. Value: see example runs and what to expect.
- [TEST_REPORT.md](./TEST_REPORT.md) — Test outcomes. Value: confidence the system works as intended.
- [TESTING.md](./TESTING.md) — How to run tests. Value: reproduce results and check your setup.
- [MVP_POC_ANALYSIS.md](./MVP_POC_ANALYSIS.md) — How close this MVP is to the full vision. Value: evaluate scope, features, and real‑world readiness.
- [IMPLEMENTATION.md](./IMPLEMENTATION.md) — What we built and how. Value: peek under the hood without deep code diving.
- [IMPLEMENTATION_COMPLETE.md](./IMPLEMENTATION_COMPLETE.md) — Delivery summary. Value: quick status of what’s done.
- [DOCUMENTATION_UPDATE_COMPLETE.md](./DOCUMENTATION_UPDATE_COMPLETE.md) — Docs status. Value: what changed in the docs and when.
- [ENHANCEMENT_GUIDE.md](./ENHANCEMENT_GUIDE.md) — Turn on advanced features. Value: enable “enhanced” modes safely.
- [NLP_UPGRADE_SUMMARY.md](./NLP_UPGRADE_SUMMARY.md) — What got better in language understanding. Value: why the new NLP matters.
- [CHROMADB_7D_GUIDE.md](./CHROMADB_7D_GUIDE.md) — How memory and emotions work together. Value: an easy explanation of vector memory and the 7‑color (ROYGBIV) emotion map.
- [SLMU_GUIDE.md](./SLMU_GUIDE.md) — The ethics layer explained. Value: how the system keeps responses safe and aligned.
- [SOUL_LOGGING_SLEEP_GUIDE.md](./SOUL_LOGGING_SLEEP_GUIDE.md) — Persistence & maintenance. Value: how your “soul” (long‑term profile), logs, and nightly clean‑up work.
- [SQLITE_USAGE_GUIDE.md](./SQLITE_USAGE_GUIDE.md) — Where data lives. Value: simple instructions to inspect stored knowledge.
- [NATIVE_RUN.md](./NATIVE_RUN.md) — Run without Docker. Value: useful for laptops and dev boxes.

Tip: There are also deeper technical notes in `docs/` (e.g., [SPACY_PIPELINE_FEATURES.md](./docs/SPACY_PIPELINE_FEATURES.md), [SYSTEM_INTEGRATION.md](./docs/SYSTEM_INTEGRATION.md)). If you’re non‑technical, you can skip these.

## �🚀 Quick Start

### Prerequisites

- Docker Desktop (or Docker + Docker Compose)
- 16GB RAM recommended (8GB minimum)
- 50GB free disk space

### Installation

1. **Clone or extract the project:**
```bash
cd DD-MVP
```

2. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

3. **Wait for startup (about 30 seconds):**
```
Digital Daemon MVP Ready!
```

4. **Test it:**
```bash
curl http://localhost:8000/health
```

### Without Docker (Local Python)

1. **Create virtual environment:**
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
cd src
python main.py
```

## 📖 Usage Examples

### Process Input (Core Function)

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I am seeking wisdom and understanding in my life",
    "user_id": "john_doe"
  }'
```

**Response:**
```json
{
  "success": true,
  "coherence": 0.917,
  "response": "Seeking wisdom is virtuous. Reflecting on: I am seeking wisdom and understanding...",
  "details": {
    "sentiment": {
      "label": "optimism",
      "score": 0.892,
      "all_scores": {
        "optimism": 0.892,
        "joy": 0.761,
        "trust": 0.342,
        "love": 0.189,
        "anticipation": 0.087,
        "sadness": 0.043,
        "fear": 0.021
      }
    },
    "concepts": [
      {
        "name": "wisdom",
        "lemma": "wisdom",
        "entity_type": "LEMMA",
        "pos_tag": "NOUN",
        "category": "virtue"
      },
      {
        "name": "understanding",
        "lemma": "understanding",
        "entity_type": "LEMMA",
        "pos_tag": "NOUN",
        "category": "concept"
      }
    ],
    "entities": [],
    "relationships": [],
    "linguistic_features": {
      "token_count": 9,
      "pos_distribution": {
        "NOUN": 3,
        "VERB": 2,
        "PRON": 1,
        "ADP": 1,
        "CCONJ": 1,
        "DET": 1
      },
      "key_lemmas": ["seek", "wisdom", "understanding", "life"],
      "sentence_count": 1,
      "dependency_types": ["nsubj", "ROOT", "dobj", "prep", "pobj"],
      "avg_token_length": 5.2
    },
    "slmu_compliance": {
      "compliant": true,
      "violations": [],
      "warnings": [],
      "ethical_patterns_found": 2,
      "harm_patterns_found": 0
    },
    "soul_alignment": 0.812,
    "session_id": "abc-123-def",
    "similar_memories": [
      {
        "id": "chroma_john_doe_98765",
        "distance": 0.23,
        "text_snippet": "I want to learn and grow in wisdom..."
      }
    ],
    "triad_outputs": {
      "chroma_vector_id": "chroma_john_doe_123456",
      "chroma_embedding_dim": 384,
      "chroma_similar_count": 3,
      "prismo_concept_count": 2,
      "prismo_entity_count": 0,
      "prismo_sentence_count": 1,
      "anchor_interaction_count": 1
    }
  }
}
```

### Get User's Soul

```bash
curl http://localhost:8000/soul/john_doe
```

**Response:**
```json
{
  "user_id": "john_doe",
  "vector": [0.21, 0.34, 0.18, 0.42, 0.31, 0.28, 0.19],
  "alignment_score": 0.812,
  "interaction_count": 47,
  "preferences": {},
  "created_at": "2025-10-27T10:30:00.000Z",
  "last_updated": "2025-10-27T14:15:00.000Z"
}
```

### Check System Health

```bash
curl http://localhost:8000/health
```

### Trigger Sleep Phase Manually

```bash
curl -X POST http://localhost:8000/sleep/trigger
```

### Get Session History

```bash
curl http://localhost:8000/session/{session_id}/history
```

### Get User History

```bash
curl http://localhost:8000/user/{user_id}/history?limit=10
```

## 🧠 Enhanced NLP Features

### 28-Emotion Detection
Uses Cardiff Twitter RoBERTa multilabel model to detect:
- **Positive:** joy, optimism, love, admiration, gratitude, pride, relief, caring, trust
- **Negative:** anger, sadness, fear, disgust, disappointment, grief, nervousness, annoyance
- **Mixed:** surprise, confusion, embarrassment, realization, curiosity, anticipation
- Returns ALL emotion scores, enabling mixed-emotion analysis

### spaCy Pipeline Integration
- **Named Entity Recognition (NER):** Extracts people, organizations, locations, dates
- **Part-of-Speech Tagging:** Identifies nouns, verbs, adjectives, etc.
- **Dependency Parsing:** Analyzes grammatical structure
- **Lemmatization:** Finds root forms (running → run)
- **Sentence Boundary Detection:** Splits text into sentences
- **Rule-based Matching:** Identifies ethical patterns (harm, virtue, commands)
- **Linguistic Features:** Token count, POS distribution, key lemmas, dependencies

### Vector Storage
- **sentence-transformers:** 384-dimensional semantic embeddings (all-MiniLM-L6-v2)
- **ChromaDB:** Persistent vector database with similarity search
- **FAISS:** Fast approximate nearest neighbor search

### Long Text Handling
- Automatic truncation at 512 tokens for RoBERTa
- No token limit errors, graceful degradation

## 🏗️ Architecture

```
                    FastAPI App
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    CHROMA           PRISMO           ANCHOR
  (Perceptive)     (Cognitive)      (Embodied)
  28-emotion       spaCy NLP        Memory
  RoBERTa          9 features       Context
  ChromaDB         Enhanced         Session
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
                  CORPUS CALLOSUM
              (Fusion + SLMU Ethics)
              Multi-feature validation
                         │
                         ▼
                      SOUL
               (User Alignment)
            Vector blending + JSON
                         │
                         ▼
                   SLEEP PHASE
            (Scheduled Maintenance)
```

**Enhanced Components:**
- **Chroma Enhanced:** Cardiff 28-emotion model + 384D embeddings + ChromaDB
- **Prismo Enhanced:** Full spaCy pipeline with 9 features
- **Callosum:** Dual-format SLMU compliance checking
- **Soul:** Vector-based alignment tracking with gradual updates

## 📁 Project Structure

```
DD-MVP/
├── docker-compose.yml       # Docker orchestration
├── Dockerfile               # Container definition
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .gitignore              # Git exclusions
│
├── config/                 # Configuration files
│   ├── slmu_rules.json     # Ethical rules
│   └── system_config.json  # System settings
│
├── data/                   # Persistent storage (created on first run)
│   ├── dd.db               # SQLite database
│   ├── vectors.npz         # NumPy vector store
│   ├── soul_state.json     # Soul persistence
│   └── interactions.jsonl  # Interaction logs
│
├── src/                    # Source code
│   ├── main.py             # FastAPI application
│   ├── callosum.py         # Fusion logic
│   ├── soul.py             # Soul subsystem
│   ├── sleep.py            # Sleep phase scheduler
│   ├── slmu.py             # SLMU policy engine
│   ├── models.py           # Pydantic models
│   ├── vector_store.py     # Vector storage
│   │
│   └── triads/             # Triad implementations
│       ├── __init__.py
│       ├── chroma.py       # Basic Chroma triad
│       ├── chroma_enhanced.py  # Enhanced: 28-emotion + ChromaDB
│       ├── prismo.py       # Basic Prismo triad
│       ├── prismo_enhanced.py  # Enhanced: spaCy + NLP features
│       └── anchor.py       # Anchor triad
│
├── tests/                  # Test suite (deleted - see test_e2e.sh)
├── test_e2e.sh            # 34 comprehensive E2E tests
├── benchmark.py           # Performance benchmarking
├── demo_interactive.sh    # Interactive feature demo
├── download_models.py     # ML model pre-caching
│
└── docs/                   # Additional documentation
    ├── TESTING.md
    ├── NLP_UPGRADE_SUMMARY.md
    ├── ENHANCEMENT_GUIDE.md
    ├── SPACY_PIPELINE_FEATURES.md
    └── SYSTEM_INTEGRATION.md
```

## 🔧 Configuration

### SLMU Rules (`config/slmu_rules.json`)

Edit this file to customize ethical boundaries:

```json
{
  "prohibited_concepts": [
    "violence",
    "harm",
    "deception"
  ],
  "required_virtues": [
    "temperance",
    "prudence",
    "justice"
  ]
}
```

### System Config (`config/system_config.json`)

Adjust system behavior:

```json
{
  "sleep_phase": {
    "interval_hours": 6
  },
  "callosum": {
    "default_weights": {
      "chroma": 0.33,
      "prismo": 0.34,
      "anchor": 0.33
    }
  }
}
```

## 🧪 Testing

Run the comprehensive E2E test suite:

```bash
# Run all 34 E2E tests
./test_e2e.sh

# Run performance benchmark
docker exec dd-mvp python benchmark.py

# Run interactive demo
./demo_interactive.sh

# Run enhanced feature tests
./test_enhanced.sh

# Test spaCy pipeline specifically
./test_spacy_pipeline.sh
```

**Test Coverage:**
- Core System (2 tests)
- Basic Processing (3 tests)
- NLP Features (6 tests) - entities, concepts, POS tags, relationships
- SLMU Compliance (4 tests) - ethical validation
- Soul System (5 tests) - persistence, alignment
- Vector Similarity (2 tests)
- ChromaDB Integration (2 tests)
- Edge Cases (5 tests) - unicode, emoji, long text
- Triad Outputs (4 tests)
- Performance (1 test)

**Total: 34/34 passing (100%)**

## 📊 API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔍 Monitoring

### Logs

**Docker:**
```bash
docker-compose logs -f dd-mvp
```

**Local:**
Logs print to console automatically.

### Sleep Phase Status

```bash
curl http://localhost:8000/sleep/status
```

**Response:**
```json
{
  "scheduler_running": true,
  "last_run": "2025-10-27T12:00:00",
  "run_count": 4,
  "next_run": "2025-10-27T18:00:00"
}
```

## 🛠️ Development

### Adding New Endpoints

Edit `src/main.py`:

```python
@app.get("/my-endpoint", tags=["Custom"])
async def my_endpoint():
    return {"message": "Hello!"}
```

### Modifying Triads

Each triad is in `src/triads/`:
- `chroma.py` - Emotional/perceptive processing
- `prismo.py` - Cognitive/moral reasoning
- `anchor.py` - Embodiment/feedback

### Adjusting Fusion Logic

Edit `src/callosum.py` to change how triads are combined.

## 🐛 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs dd-mvp

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Permission errors

```bash
chmod -R 755 data/
```

### Port already in use

Change port in `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Changed from 8000:8000
```

### Out of memory

Reduce Docker memory limit or increase system RAM allocation:
```yaml
services:
  dd-mvp:
    mem_limit: 2g
```

### Slow responses

1. Check if sleep phase is running (high CPU)
2. Reduce vector dimensions in `chroma.py`
3. Limit history queries

## 📈 Performance

**Typical Response Times:**
- `/process`: 50-200ms
- `/soul/{user_id}`: <10ms
- `/health`: <5ms
- Sleep phase: 5-30 seconds

**Resource Usage:**
- RAM: 200-500MB (normal), 1-2GB (peak)
- CPU: 10-30% (idle), 50-100% (active)
- Disk: 50MB-1GB (depends on usage)

## 🔐 Security Notes

⚠️ **This is a development MVP!**

For production:
1. Add authentication (JWT)
2. Enable HTTPS/TLS
3. Rate limiting
4. Input validation
5. Secrets management
6. Network isolation

## 📚 Next Steps

### Immediate Improvements
1. Add sentence-transformers for better embeddings
2. Implement spaCy for concept extraction
3. Create simple web UI
4. Add more comprehensive SLMU rules

### Medium-term
1. Replace SimpleVectorStore with Faiss
2. Add user authentication
3. Implement feedback loops
4. Create analytics dashboard

### Long-term (Scale to Production)
1. Migrate to PostgreSQL
2. Add async processing
3. Implement Redis caching
4. Deploy to cloud

See `docs/DD_7.1_Architecture_Implementation_Plan.md` for full production architecture.

## 🤝 Contributing

This is a proof of concept. Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests
- Extend functionality

## 📄 License

[Your chosen license]

## 📞 Support

For questions or issues:
1. Check logs: `docker-compose logs -f`
2. Review documentation in `/docs`
3. Test with `/health` endpoint
4. Check sleep phase status

## 🎓 Learning Resources

### Understanding the Architecture
- **Triads:** Three parallel cognitive processors
- **Callosum:** Fusion and arbitration layer
- **Soul:** Persistent user alignment tracking
- **SLMU:** Ethical compliance system
- **Sleep Phase:** Maintenance and consolidation

### Key Concepts
- **Coherence:** How well triads agree (0-1)
- **Alignment:** User's ethical score (0-1)
- **ROYGBIV Vector:** 7D emotional representation
- **Concept Graph:** Knowledge structure in SQLite

---

**Built with:** Python 3.11, FastAPI, NumPy, SQLite, APScheduler  
**Version:** 7.1-mvp  
**Date:** October 27, 2025

🚀 **Ready to explore sanctified artificial cognition!**
