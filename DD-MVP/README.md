# Digital Daemon v7.1 — MVP

A simplified, local implementation of the Digital Daemon triadic cognitive architecture with ethical alignment.

## 🎯 Overview

This MVP runs entirely on your local machine using Docker Compose. It implements the complete triadic cognitive model (Chroma, Prismo, Anchor) with Corpus Callosum fusion, Soul persistence, and Sleep Phase consolidation.

**What You Get:**
- ✅ Three cognitive triads working in coordination
- ✅ Ethical alignment via SLMU rules
- ✅ Persistent user "souls" tracking alignment over time
- ✅ Automated sleep phase for system maintenance
- ✅ REST API with comprehensive endpoints
- ✅ Complete logging and monitoring

**Cost:** $0 (runs locally)  
**Timeline:** 6-8 weeks to build from scratch  
**Hardware:** 16GB RAM, 4+ cores, 50GB disk

## 🚀 Quick Start

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
  "coherence": 0.834,
  "response": "Seeking wisdom is virtuous. Reflecting on: I am seeking wisdom and understanding...",
  "details": {
    "sentiment": 0.75,
    "concepts": ["wisdom", "understanding"],
    "soul_alignment": 0.812,
    "session_id": "abc-123-def",
    "similar_memories": 3,
    "triad_outputs": {
      "chroma_vector_id": "chroma_john_doe_123456",
      "prismo_concept_count": 2,
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

## 🏗️ Architecture

```
                    FastAPI App
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    CHROMA           PRISMO           ANCHOR
  (Perceptive)     (Cognitive)      (Embodied)
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
                  CORPUS CALLOSUM
                  (Fusion + Ethics)
                         │
                         ▼
                      SOUL
               (User Alignment)
                         │
                         ▼
                   SLEEP PHASE
               (Scheduled Maintenance)
```

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
│       ├── chroma.py       # Chroma triad
│       ├── prismo.py       # Prismo triad
│       └── anchor.py       # Anchor triad
│
└── tests/                  # Test suite
    └── test_*.py
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

Run tests with pytest:

```bash
# In Docker
docker-compose exec dd-mvp pytest

# Locally
pytest tests/
```

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
