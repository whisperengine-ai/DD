# Digital Daemon MVP - Quick Reference

## 🚀 Getting Started

### Start the system:
```bash
./start.sh
# OR
docker-compose up --build
```

### Stop the system:
```bash
docker-compose down
```

### View logs:
```bash
docker-compose logs -f dd-mvp
```

## 📡 API Endpoints

### Core Operations

**Process Input** (Main endpoint)
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "I seek wisdom and understanding", "user_id": "john"}'
```

**Get Soul State**
```bash
curl http://localhost:8000/soul/john
```

**Health Check**
```bash
curl http://localhost:8000/health
```

### System Management

**Sleep Phase Status**
```bash
curl http://localhost:8000/sleep/status
```

**Trigger Sleep Phase**
```bash
curl -X POST http://localhost:8000/sleep/trigger
```

**All Souls Statistics**
```bash
curl http://localhost:8000/souls/stats
```

### History

**Session History**
```bash
curl http://localhost:8000/session/{session_id}/history
```

**User History**
```bash
curl http://localhost:8000/user/{user_id}/history?limit=10
```

## 📊 Response Examples

### Process Response
```json
{
  "success": true,
  "coherence": 0.834,
  "response": "Seeking wisdom is virtuous...",
  "details": {
    "sentiment": 0.75,
    "concepts": ["wisdom", "understanding"],
    "soul_alignment": 0.812,
    "session_id": "abc-123",
    "similar_memories": 3
  }
}
```

### Soul Response
```json
{
  "user_id": "john",
  "vector": [0.21, 0.34, 0.18, 0.42, 0.31, 0.28, 0.19],
  "alignment_score": 0.812,
  "interaction_count": 47,
  "preferences": {},
  "created_at": "2025-10-27T10:30:00Z",
  "last_updated": "2025-10-27T14:15:00Z"
}
```

## 🔧 Configuration

### SLMU Rules (`config/slmu_rules.json`)
```json
{
  "prohibited_concepts": ["violence", "harm", "deception"],
  "required_virtues": ["temperance", "prudence", "justice"],
  "ethical_weights": {
    "truthfulness": 1.0,
    "compassion": 0.9,
    "wisdom": 0.8
  }
}
```

### System Config (`config/system_config.json`)
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

## 🐛 Troubleshooting

### Container won't start
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Check logs
```bash
docker-compose logs --tail=100 dd-mvp
```

### Permission errors
```bash
chmod -R 755 data/
```

### Port in use
Edit `docker-compose.yml` and change:
```yaml
ports:
  - "8080:8000"  # Changed port
```

### Reset everything
```bash
docker-compose down -v
rm -rf data/*
docker-compose up --build
```

## 📈 Monitoring

### Check system health
```bash
curl http://localhost:8000/health | jq
```

### View all active souls
```bash
curl http://localhost:8000/souls/stats | jq
```

### Monitor sleep phase
```bash
curl http://localhost:8000/sleep/status | jq
```

## 🧪 Testing

### Run all tests
```bash
docker-compose exec dd-mvp pytest -v
```

### Run specific test file
```bash
docker-compose exec dd-mvp pytest tests/test_chroma.py -v
```

### Run with coverage
```bash
docker-compose exec dd-mvp pytest --cov=src tests/
```

## 📁 File Locations

### Data Files (persisted)
- `data/dd.db` - SQLite database (concepts)
- `data/vectors.npz` - Vector store (memories)
- `data/soul_state.json` - Soul states
- `data/interactions.jsonl` - Interaction logs

### Config Files
- `config/slmu_rules.json` - Ethical rules
- `config/system_config.json` - System settings

### Source Code
- `src/main.py` - FastAPI application
- `src/triads/` - Triad implementations
- `src/callosum.py` - Fusion logic
- `src/soul.py` - Soul subsystem
- `src/sleep.py` - Sleep phase

## 🎯 Key Concepts

### Coherence (0-1)
How well the three triads agree on the output.
- **< 0.5**: Low agreement, conflicting signals
- **0.5-0.7**: Moderate agreement
- **> 0.7**: High agreement, strong coherence

### Alignment Score (0-1)
User's ethical alignment based on interaction history.
- **< 0.5**: Concerning patterns
- **0.5-0.7**: Average alignment
- **> 0.7**: Strong ethical alignment

### ROYGBIV Vector (7D)
Emotional/perceptive representation:
- [0]: Red (passion, energy)
- [1]: Orange (creativity)
- [2]: Yellow (joy, optimism)
- [3]: Green (balance, growth)
- [4]: Blue (calm, truth)
- [5]: Indigo (intuition)
- [6]: Violet (wisdom, spirituality)

## 💡 Tips

1. **Start with simple queries** to understand the system
2. **Check soul alignment** after each interaction
3. **Monitor coherence** to ensure triads are working well
4. **Review SLMU rules** before deploying to production
5. **Back up data/** directory regularly
6. **Check logs** if something seems wrong
7. **Trigger sleep phase manually** for testing
8. **Use session IDs** to track conversation threads

## 🔗 Links

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Root Info**: http://localhost:8000/

## ⚡ Quick Commands

```bash
# Start
./start.sh

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Test API
curl http://localhost:8000/health

# Process text
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text":"test","user_id":"demo"}'

# Get soul
curl http://localhost:8000/soul/demo

# Rebuild
docker-compose up --build --force-recreate
```

## 🆘 Support

If stuck:
1. Check README.md
2. Review logs: `docker-compose logs`
3. Test health: `curl http://localhost:8000/health`
4. Check disk space: `df -h`
5. Verify Docker: `docker info`

---

**Version:** 7.1-mvp  
**Updated:** October 27, 2025
