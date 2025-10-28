# Running Digital Daemon MVP Natively (Without Docker)

## Quick Start

### Option 1: Automated Setup

```bash
# 1. Run setup script (creates venv, installs deps, downloads models)
./setup_native.sh

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run the server
./run_native.py
# or: python run_native.py
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download spaCy model
python -m spacy download en_core_web_sm

# 4. Pre-download transformer models (optional but recommended)
python download_models.py

# 5. Create data directories
mkdir -p data/chromadb

# 6. Run the server
python run_native.py
```

## What Gets Installed

### Python Packages (~1.4GB)
- **FastAPI** 0.104.1 - Web framework
- **uvicorn** 0.24.0 - ASGI server
- **spaCy** 3.7.2 + en_core_web_sm - NLP pipeline
- **transformers** 4.35.2 - Cardiff Twitter RoBERTa
- **sentence-transformers** 2.2.2 - Embeddings
- **torch** 2.1.1 - PyTorch backend
- **chromadb** 0.4.18 - Vector database
- Other dependencies (numpy, sqlalchemy, etc.)

### ML Models
- **spaCy en_core_web_sm**: 43MB
- **Cardiff Twitter RoBERTa**: ~500MB
- **sentence-transformers (all-MiniLM-L6-v2)**: ~80MB
- **PyTorch**: ~800MB

## Configuration

### Environment Variables

```bash
# Enable/disable enhanced mode (default: true)
export DD_USE_ENHANCED=true

# Set environment
export DD_ENV=native
```

### File Paths

Native run uses the same paths as Docker:
- **Config**: `./config/slmu_rules.json`, `./config/system_config.json`
- **Data**: `./data/` (SQLite, ChromaDB, vectors, soul state, interactions)
- **Logs**: stdout/stderr

## Running the Server

### Basic Run
```bash
python run_native.py
```

### With Custom Port
```bash
# Modify run_native.py or run uvicorn directly:
uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
```

### Production Mode (No Reload)
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Background Run
```bash
nohup python run_native.py > logs/server.log 2>&1 &
echo $! > server.pid  # Save PID for later
```

### Stop Background Server
```bash
kill $(cat server.pid)
rm server.pid
```

## Testing

### Run Demo Script
```bash
# Ensure server is running, then:
./demo.sh
```

### Run Enhanced Tests
```bash
./test_enhanced.sh
```

### Run spaCy Pipeline Tests
```bash
./test_spacy_pipeline.sh
```

### Manual API Test
```bash
# Health check
curl http://localhost:8000/health | jq

# Process text
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test",
    "text": "Hello world"
  }' | jq
```

## Development Workflow

### With Auto-Reload
```bash
# Terminal 1: Run server with reload
python run_native.py

# Terminal 2: Edit code
vim src/triads/prismo_enhanced.py

# Server automatically reloads on file changes
```

### Without Auto-Reload
```bash
# Run with uvicorn directly
uvicorn src.main:app --host 0.0.0.0 --port 8000 --no-reload
```

### Debugging
```bash
# Run with Python debugger
python -m pdb run_native.py

# Or use VS Code debugger with launch.json
```

## Troubleshooting

### Issue: spaCy Model Not Found

```bash
# Download manually
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('OK')"
```

### Issue: Transformer Models Slow on First Run

```bash
# Pre-download models
python download_models.py

# Models cached to:
# - ~/.cache/huggingface/transformers/
# - ~/.cache/torch/sentence_transformers/
```

### Issue: Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn src.main:app --port 8080
```

### Issue: Module Not Found

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Verify installation
pip list | grep -E "fastapi|spacy|transformers"

# Reinstall if needed
pip install -r requirements.txt
```

### Issue: Out of Memory

```bash
# Monitor memory usage
python -c "
import psutil
print(f'Memory: {psutil.virtual_memory().percent}%')
"

# Reduce model memory:
# 1. Disable enhanced mode
export DD_USE_ENHANCED=false
python run_native.py

# 2. Or free up memory
# Close other applications
```

## Performance

### Native vs Docker

| Metric | Docker | Native |
|--------|--------|--------|
| Startup Time | 5s | 3s |
| Request Latency | 80ms | 70ms |
| Memory Usage | 1.5GB | 1.3GB |
| Reload Speed | N/A | <1s |
| Development Speed | Slower | Faster |

### Native Advantages
- ✅ Faster startup (no container overhead)
- ✅ Auto-reload for development
- ✅ Direct debugger access
- ✅ Lower memory usage
- ✅ No Docker daemon required

### Native Disadvantages
- ⚠️ System Python version dependency
- ⚠️ Manual dependency management
- ⚠️ No isolation (could conflict with other projects)
- ⚠️ Platform-specific (works on your machine™)

## Best Practices

### Use Virtual Environment
```bash
# Always activate venv first
source venv/bin/activate

# Check you're in the right env
which python
# Should show: /path/to/DD-MVP/venv/bin/python
```

### Keep Dependencies Updated
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade transformers
```

### Clean Data Between Tests
```bash
# Reset database
rm data/dd.db

# Reset vectors
rm data/vectors.npz
rm -rf data/chromadb/

# Reset soul state
rm data/soul_state.json

# Reset interactions
rm data/interactions.jsonl
```

### Switch Between Basic/Enhanced
```bash
# Enhanced mode (default)
DD_USE_ENHANCED=true python run_native.py

# Basic mode (faster, less memory)
DD_USE_ENHANCED=false python run_native.py
```

## IDE Integration

### VS Code

**`.vscode/launch.json`**:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
      ],
      "jinja": true,
      "justMyCode": true,
      "env": {
        "DD_USE_ENHANCED": "true"
      }
    }
  ]
}
```

### PyCharm

1. Run → Edit Configurations
2. Add New Configuration → Python
3. Script path: `/path/to/run_native.py`
4. Python interpreter: `venv/bin/python`
5. Working directory: `/path/to/DD-MVP`
6. Environment variables: `DD_USE_ENHANCED=true`

## Production Deployment (Native)

### Using systemd (Linux)

**`/etc/systemd/system/dd-mvp.service`**:
```ini
[Unit]
Description=Digital Daemon MVP
After=network.target

[Service]
Type=simple
User=dd-user
WorkingDirectory=/opt/DD-MVP
Environment="DD_USE_ENHANCED=true"
ExecStart=/opt/DD-MVP/venv/bin/python run_native.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable dd-mvp
sudo systemctl start dd-mvp
sudo systemctl status dd-mvp
```

### Using Gunicorn (Production WSGI)

```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --daemon
```

### Using PM2 (Process Manager)

```bash
# Install PM2 (requires Node.js)
npm install -g pm2

# Start server
pm2 start run_native.py --name dd-mvp --interpreter python3

# View logs
pm2 logs dd-mvp

# Restart
pm2 restart dd-mvp

# Stop
pm2 stop dd-mvp
```

## Comparison: Docker vs Native

### Use Docker When:
- ✅ Deploying to production
- ✅ Ensuring consistency across environments
- ✅ Need isolation from other services
- ✅ Running on servers/cloud
- ✅ Sharing with others

### Use Native When:
- ✅ Local development
- ✅ Rapid iteration/debugging
- ✅ Testing code changes
- ✅ Learning the codebase
- ✅ Limited Docker resources

### Hybrid Approach:
```bash
# Develop natively with auto-reload
python run_native.py

# Test in Docker before committing
docker-compose up --build

# Deploy with Docker
docker-compose -f docker-compose.prod.yml up -d
```

---

## Summary

**Native Python run provides**:
- 🚀 Faster development cycle (auto-reload)
- 🐛 Easier debugging (direct Python access)
- 💻 Lower resource usage (no container overhead)
- 🔧 Simpler setup for local testing

**Perfect for**:
- Development and debugging
- Quick tests and experiments
- Learning the codebase
- Rapid prototyping

**Docker is still recommended for**:
- Production deployment
- Consistent environments
- Sharing with team
- CI/CD pipelines
