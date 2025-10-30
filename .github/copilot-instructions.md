# Copilot Instructions for this repo (DD v7.1)

Purpose: Give AI coding agents the fastest path to being productive in this codebase.

## Big picture
- Architecture is triadic cognition: three parallel "triads" plus an integration/gating layer and persistent user state.
  - Chroma (emotion): 28‑emotion multilabel via Cardiff RoBERTa; 384D embeddings via sentence‑transformers; vectors in ChromaDB. See `src/triads/chroma*.py` and `src/vector_store.py`.
  - Prismo (cognition): spaCy 3.7 pipeline extracts entities, concepts, relationships, lemmas, POS, deps, sentences, rule‑matches. See `src/triads/prismo*.py`.
  - Anchor (history): logs interactions, sessions, and retrieves past context. See `src/triads/anchor.py`.
  - Corpus Callosum (fusion + ethics): merges triad outputs, calculates coherence, and runs SLMU v2.0 ethical gating using BOTH linguistic and emotional signals. See `src/callosum.py` and `src/slmu.py`.
  - Soul (persistence): per‑user evolving profile, alignment score, and triad weights, persisted under `data/`. See `src/soul.py`.
  - Sleep phase: APScheduler job consolidates vectors, prunes graphs, optimizes DB every ~6h. See `src/sleep.py`.

## Where work happens
- API: FastAPI app in `src/main.py` (POST `/process`, GET `/health`, `/soul/{id}`, etc.). Response model includes `details` with sentiment, concepts, entities, relationships, linguistic_features, ethical_patterns, slmu_compliance, triad_outputs.
- Config: `config/slmu_rules.json` (ethics) and `config/system_config.json` (weights). Adjust and restart.
- Data: `data/` holds SQLite, ChromaDB, vectors, `soul_state.json`, `interactions.jsonl`.
- Docker: `DD-MVP/docker-compose.yml`, `DD-MVP/Dockerfile`. Native run: `run_native.py`.

## Dev workflows (do these)
- Docker run: `docker-compose up --build -d` (service `dd-mvp`), logs with `docker logs -f dd-mvp`.
- Native run: `./setup_native.sh` then `python run_native.py` (env `DD_USE_ENHANCED=true` by default). Model prefetch: `python download_models.py`.
- Demos/tests from `DD-MVP`:
  - `./demo_interactive.sh` (feature tour), `./test_e2e.sh` (34 E2E tests), `./test_spacy_pipeline.sh` (verifies spaCy flow), `python benchmark.py`.
- API quick checks:
  - `GET /health`, `POST /process` with `{text, user_id}`, `GET /soul/{user}`; OpenAPI at `/docs`.

## Patterns and conventions
- Keep triads focused: Chroma = emotion/embeddings, Prismo = linguistic analysis, Anchor = session/history. No ethics in Prismo—SLMU v2.0 runs in Callosum only.
- Pass through data, don’t drop it: Callosum preserves entities, concepts, relationships, linguistic_features, ethical_patterns, slmu results into the API `details` object.
- Coherence scoring uses linguistic richness (token_count, POS diversity) from Prismo; emotions inform compliance/warnings.
- SLMU rules are lemma‑aware and threshold‑based for emotions; update `config/slmu_rules.json`. Integration uses both Prismo and Chroma outputs.
- Souls update after each interaction (alignment, triad_weights). Keep write paths under `data/` consistent.

## Extending the system (examples)
- Add a new field to API `details`: compute it inside a triad or Callosum; thread it through `fuse(...)` in `src/callosum.py`, then include in the Pydantic response in `src/main.py`.
- Add/modify ethics: update `config/slmu_rules.json` and (if needed) logic in `src/slmu.py` and the Callosum SLMU call site.
- New triad or enhancement: implement under `src/triads/`, keep processing contract `process(text, user_id)` returning structured dictionaries; register in `src/main.py` pipeline and fuse in Callosum.
- Storage: use `vector_store.py` for embeddings/ChromaDB; expand SQLite writes in the relevant triad (Prismo examples are in docs).

## Key references in this repo
- Conceptual docs: `DD-MVP/SYSTEM_OVERVIEW.md`, `DD-MVP/docs/SYSTEM_INTEGRATION.md`.
- Runbooks: `DD-MVP/QUICKSTART.md`, `DD-MVP/NATIVE_RUN.md`, `DD-MVP/TESTING.md`.
- Source: `DD-MVP/src/*.py`, triads under `src/triads/`.
- Config/Data: `DD-MVP/config/*.json`, `DD-MVP/data/*` (created at runtime).

Notes
- Project is 100% local—no cloud APIs. Large first‑run downloads (spaCy, RoBERTa, sentence‑transformers, PyTorch). If memory‑constrained, run with `DD_USE_ENHANCED=false`.
- License: MIT (see `LICENSE`).
