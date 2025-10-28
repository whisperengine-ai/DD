# Testing & Demo Guide

Comprehensive testing and demonstration scripts for the Digital Daemon MVP.

## 📋 Quick Reference

| Script | Purpose | Duration | Use Case |
|--------|---------|----------|----------|
| `./demo.sh` | Basic demo | ~30s | First-time users |
| `./demo_interactive.sh` | Full feature showcase | ~2min | Comprehensive overview |
| `./test_spacy_pipeline.sh` | spaCy feature verification | ~10s | Verify NLP integration |
| `./test_enhanced.sh` | Enhanced NLP tests | ~20s | Test sentiment, entities, similarity |
| `./test_e2e.sh` | End-to-end test suite | ~1min | CI/CD validation |
| `python benchmark.py` | Performance benchmarks | ~3min | Performance analysis |
| `pytest tests/` | Unit tests | ~5s | Development TDD |

---

## 🎯 Demo Scripts

### 1. Basic Demo (`demo.sh`)
Simple walkthrough of core functionality.

```bash
./demo.sh
```

**Shows:**
- Health check
- Basic text processing
- Soul evolution
- Concept extraction

---

### 2. Interactive Demo (`demo_interactive.sh`) ⭐ **RECOMMENDED**
Comprehensive showcase of all system capabilities with color-coded output.

```bash
./demo_interactive.sh
```

**Demonstrates:**
1. System health monitoring
2. Virtuous text processing
3. Named entity recognition & relationships
4. Deep linguistic analysis (POS, lemmas, dependencies)
5. Unicode & emoji support
6. Sentiment analysis spectrum (positive/neutral/negative)
7. Semantic memory & vector similarity
8. Soul state evolution
9. Triadic architecture outputs
10. SLMU ethical compliance

**Output:** Rich, color-coded JSON with explanatory sections.

---

## 🧪 Test Scripts

### 3. spaCy Pipeline Test (`test_spacy_pipeline.sh`)
Verifies all 9 spaCy features flow through the system.

```bash
./test_spacy_pipeline.sh
```

**Validates:**
- ✅ Tokenization & POS tagging
- ✅ Lemmatization
- ✅ Sentence boundary detection
- ✅ Named entity recognition
- ✅ Dependency parsing
- ✅ Concept extraction (enhanced)
- ✅ Rule-based matching
- ✅ SLMU compliance
- ✅ Serialization (database storage)

---

### 4. Enhanced NLP Test (`test_enhanced.sh`)
Tests production-grade NLP features.

```bash
./test_enhanced.sh
```

**Tests:**
- Cardiff RoBERTa sentiment analysis
- Complex entity extraction (people, orgs, locations, dates, money)
- sentence-transformers embeddings
- ChromaDB vector similarity
- Multi-language support

---

### 5. End-to-End Test Suite (`test_e2e.sh`) ⭐ **CI/CD**
Comprehensive automated test suite with pass/fail reporting.

```bash
./test_e2e.sh
```

**Test Categories:**
- **Core System** (2 tests): Health, vector count
- **Basic Processing** (3 tests): Success, coherence, sentiment
- **NLP Features** (6 tests): Entities, concepts, lemmas, POS, relationships, linguistics
- **SLMU Compliance** (4 tests): Accepts virtuous, reports compliance, rejects harmful, ethical patterns
- **Soul System** (5 tests): Creation, vector, alignment, interactions
- **Vector Similarity** (2 tests): Memory retrieval, metadata
- **ChromaDB** (2 tests): Embedding dimensions, vector IDs
- **Edge Cases** (5 tests): Empty input, short text, punctuation, unicode, long text
- **Triad Outputs** (4 tests): Chroma, Prismo, Anchor execution + session IDs
- **Performance** (1 test): 5 requests under 10s

**Total:** 34 automated tests

**Exit codes:**
- `0` = All tests passed ✅
- `1` = Some tests failed ❌

---

## 📊 Performance Benchmarking

### 6. Performance Benchmark (`benchmark.py`)
Comprehensive performance analysis with statistics.

```bash
python benchmark.py
```

**Benchmark Suites:**

1. **Health Endpoint Performance** (100 requests)
   - Mean/median/P95 latency
   - Availability check

2. **Sequential Latency** (20 requests)
   - Mean, median, P95, P99, min, max
   - Per-request timing

3. **Concurrent Throughput** (5 threads × 10 requests)
   - Requests per second
   - Concurrent behavior
   - Success rate

4. **Text Complexity Scaling** (5 complexity levels)
   - Minimal (1 word)
   - Short (3 words)
   - Medium (10 words)
   - Long (25 words)
   - Very Long (50 words)

5. **Memory Accumulation** (50 sequential requests)
   - Latency degradation over time
   - Same-user memory growth

6. **Error Recovery**
   - Invalid request handling
   - System resilience

**Example Output:**
```
Sequential Latency Test (20 requests)
  Mean:    156.3ms
  Median:  148.2ms
  P95:     201.5ms
  P99:     215.8ms

Concurrent Throughput Test
  Throughput:     32.4 req/s
  Mean latency:   154.1ms
  P95 latency:    198.3ms
```

---

## 🧬 Unit Tests

### 7. Python Unit Tests (`pytest`)
Test individual components in isolation.

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_callosum.py

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run with verbose output
pytest tests/ -v
```

**Test Files:**
- `tests/test_prismo.py` - Prismo triad (basic)
- `tests/test_chroma.py` - Chroma triad (basic)
- `tests/test_integration.py` - System integration
- `tests/test_callosum.py` - Corpus Callosum fusion ⭐ **NEW**
- `tests/test_soul.py` - Soul system ⭐ **NEW**

**New Test Coverage:**
- ✅ Callosum weight initialization
- ✅ SLMU compliance gating (basic + enhanced)
- ✅ Coherence calculation
- ✅ Triad output preservation
- ✅ Soul creation & updates
- ✅ Soul persistence
- ✅ Alignment score calculation
- ✅ Vector blending over time

---

## 🎬 Usage Examples

### Quick Validation
```bash
# Health check
curl http://localhost:8000/health

# Run quick tests
./test_spacy_pipeline.sh
```

### Full Demo for Stakeholders
```bash
# Interactive demo with explanations
./demo_interactive.sh

# Follow up with performance stats
python benchmark.py
```

### CI/CD Pipeline
```bash
# Automated test suite
./test_e2e.sh
if [ $? -eq 0 ]; then
    echo "✓ All tests passed"
else
    echo "✗ Tests failed"
    exit 1
fi
```

### Development Workflow
```bash
# Unit tests during development
pytest tests/ -v

# Integration test after changes
./test_e2e.sh

# Performance check
python benchmark.py
```

---

## 📈 Expected Results

### Performance Targets (Docker on Apple Silicon M1/M2)
- **Latency:** < 200ms (p95)
- **Throughput:** > 30 req/s
- **Health endpoint:** < 10ms
- **Concurrent:** 5+ threads without degradation

### Test Pass Rates
- **Unit tests:** 100% (15+ tests)
- **E2E tests:** 100% (34 tests)
- **Integration:** All triads operational

### NLP Quality
- **Entity extraction:** 90%+ accuracy
- **Sentiment:** Cardiff RoBERTa (SOTA)
- **Embeddings:** 384D sentence-transformers
- **Concepts:** spaCy lemmatization + POS

---

## 🐛 Troubleshooting

### Tests Fail: "Connection refused"
```bash
# Check container is running
docker ps | grep dd-mvp

# Start if needed
docker-compose up -d

# Wait for startup
sleep 5
```

### Tests Fail: "Ethical violation"
This is expected for harmful inputs. Check test expectations.

### Benchmark Shows Slow Performance
```bash
# Check system resources
docker stats dd-mvp

# Check if models are pre-cached
docker logs dd-mvp | grep "downloaded successfully"

# Restart container
docker-compose restart
```

### Unit Tests Import Errors
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Or use venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔄 Adding New Tests

### Add E2E Test
Edit `test_e2e.sh`:
```bash
run_test "Your test name" \
    "curl -s $BASE_URL/your_endpoint" \
    "jq -e '.field == expected_value'"
```

### Add Unit Test
Create `tests/test_yourcomponent.py`:
```python
import pytest
from yourmodule import YourClass

def test_your_feature():
    instance = YourClass()
    assert instance.method() == expected
```

### Add Benchmark
Edit `benchmark.py`:
```python
def test_your_benchmark():
    # Your benchmark code
    print(f"Results: {metric}")
```

---

## 📝 Test Coverage Summary

| Component | Unit Tests | Integration | E2E | Performance |
|-----------|------------|-------------|-----|-------------|
| Chroma Triad | ✅ | ✅ | ✅ | ✅ |
| Prismo Triad | ✅ | ✅ | ✅ | ✅ |
| Anchor Triad | ⚠️ Basic | ✅ | ✅ | ✅ |
| Callosum | ✅ **NEW** | ✅ | ✅ | ✅ |
| Soul System | ✅ **NEW** | ✅ | ✅ | ✅ |
| SLMU | ✅ | ✅ | ✅ | N/A |
| API | ✅ | ✅ | ✅ | ✅ |
| NLP Pipeline | ✅ | ✅ | ✅ | ✅ |

**Legend:** ✅ Complete | ⚠️ Partial | ❌ Missing

---

## 🎯 Next Steps

1. **Run Interactive Demo:**
   ```bash
   ./demo_interactive.sh
   ```

2. **Validate System:**
   ```bash
   ./test_e2e.sh
   ```

3. **Benchmark Performance:**
   ```bash
   python benchmark.py
   ```

4. **Review Results:**
   - Check pass rates
   - Analyze performance metrics
   - Identify bottlenecks

---

**Last Updated:** October 27, 2025  
**Test Scripts:** 7 (demo + test + benchmark)  
**Total Test Coverage:** 50+ assertions across unit, integration, E2E, and performance tests
