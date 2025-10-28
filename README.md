
---

Original architecture/design credit: TechnoShaman (Discord ID: 191470268999401472)
# DD — Digital Daemon Repository (v7.1)

A monorepo that currently hosts the Digital Daemon Enhanced MVP (DD‑MVP). It implements a triadic cognitive architecture (Chroma, Prismo, Anchor) with fusion via a Corpus Callosum, persistent "Soul" alignment, ChromaDB vector memory, and a spaCy‑driven SLMU ethics layer.

If you're here to run the software, jump straight to DD‑MVP:

- Project entry: [DD-MVP/](DD-MVP/)
- Main README: [DD-MVP/README.md](DD-MVP/README.md)
- Quickstart: [DD-MVP/QUICKSTART.md](DD-MVP/QUICKSTART.md)

## Repository structure

```
DD/
├─ DD-MVP/                  # Enhanced MVP application (FastAPI, NLP, ChromaDB, SLMU)
│  ├─ README.md             # In-depth usage, API, tests, troubleshooting
│  ├─ docker-compose.yml    # Container orchestration
│  ├─ Dockerfile            # App container image
│  ├─ requirements.txt      # Python dependencies
│  ├─ config/               # SLMU rules, system config
│  ├─ data/                 # Runtime state (created on first run)
│  ├─ src/                  # Source code (triads, callosum, soul, sleep)
│  └─ docs/                 # Additional MVP docs
│
└─ docs/                    # Top-level docs (architecture and development)
   ├─ DD 7.1.txt
   ├─ DD_7.1_Architecture_Implementation_Plan.md
   └─ DD_7.1_MVP_Local_Development.md
```

Additional technical guides inside DD‑MVP:
- ChromaDB + 7D ROYGBIV mapping: [DD-MVP/CHROMADB_7D_GUIDE.md](DD-MVP/CHROMADB_7D_GUIDE.md)
- MVP vs POC analysis: [DD-MVP/MVP_POC_ANALYSIS.md](DD-MVP/MVP_POC_ANALYSIS.md)
- System integration notes: [DD-MVP/docs/SYSTEM_INTEGRATION.md](DD-MVP/docs/SYSTEM_INTEGRATION.md)
- spaCy pipeline features: [DD-MVP/docs/SPACY_PIPELINE_FEATURES.md](DD-MVP/docs/SPACY_PIPELINE_FEATURES.md)

## Quick start

The MVP lives under `DD-MVP/`. Choose Docker or a native Python run.

- Docker (recommended):
  1) `cd DD-MVP`
  2) `docker-compose up --build`
  3) Visit Swagger UI at http://localhost:8000/docs

- Native (Python 3.11+):
  1) `cd DD-MVP`
  2) `python3.11 -m venv venv && source venv/bin/activate`
  3) `pip install -r requirements.txt`
  4) `python src/main.py`

Health check once running:
- `curl http://localhost:8000/health`

See full instructions and troubleshooting in [DD-MVP/README.md](DD-MVP/README.md) and [DD-MVP/QUICKSTART.md](DD-MVP/QUICKSTART.md).

## What’s inside the MVP

- 28‑emotion multilabel detection (CardiffNLP RoBERTa)
- 384‑dim sentence embeddings + ChromaDB similarity search
- spaCy pipeline (NER, POS, dependencies, lemmatization, rule matcher)
- SLMU v2.0 ethical compliance (lemma + dependency + matcher + emotion thresholds)
- Soul persistence with alignment tracking and scheduled "sleep" maintenance
- FastAPI service with `/process`, `/soul/{user}`, `/health`, and more

## Testing and demos

From `DD-MVP/`:
- End‑to‑end tests: `./test_e2e.sh`
- Enhanced feature tests: `./test_enhanced.sh`
- spaCy pipeline tests: `./test_spacy_pipeline.sh`
- Benchmark: `python benchmark.py` (inside container) or `docker exec` from Compose
- Interactive demo: `./demo_interactive.sh`

## Requirements

- Docker Desktop (or Docker + Compose) — or — Python 3.11+
- Recommended: 16GB RAM, 50GB free disk (to cache ML models)

## Documentation

- MVP documentation index: [DD-MVP/README.md](DD-MVP/README.md)
- Architecture plan: [docs/DD_7.1_Architecture_Implementation_Plan.md](docs/DD_7.1_Architecture_Implementation_Plan.md)
- Local development guide: [docs/DD_7.1_MVP_Local_Development.md](docs/DD_7.1_MVP_Local_Development.md)

## Contributing

Pull requests and issues are welcome. See the MVP README for development tips and the testing suite.

## License

TBD — add your preferred license.

## Status

- Version: 7.1 (Enhanced MVP)
- Date: October 28, 2025
- Primary maintained app: [DD-MVP](DD-MVP/)
