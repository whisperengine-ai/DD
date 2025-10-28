#!/bin/bash

echo "========================================"
echo "Digital Daemon NLP Upgrade - Quick Start"
echo "========================================"
echo ""
echo "This script will:"
echo "  1. Stop the current container"
echo "  2. Rebuild with enhanced NLP libraries"
echo "  3. Start the enhanced system"
echo "  4. Run a quick test"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

echo ""
echo "Step 1: Stopping current container..."
docker-compose down

echo ""
echo "Step 2: Building enhanced version..."
echo "(Pre-downloading ML models into container - may take 5-10 minutes)"
echo "  - spaCy model: 43MB"
echo "  - Cardiff RoBERTa: 500MB"
echo "  - sentence-transformers: 80MB"
echo "  - PyTorch + dependencies: 800MB"
echo ""
docker-compose build

echo ""
echo "Step 3: Starting enhanced system..."
echo "(Models are pre-cached, startup should be fast ~5 seconds)"
docker-compose up -d

echo ""
echo "Step 4: Waiting for system to be ready..."
sleep 10

echo ""
echo "Step 5: Checking health..."
curl -s http://localhost:8000/health | jq '.'

echo ""
echo "Step 6: Running enhanced test..."
echo ""
echo "Test Input: 'Elon Musk announced that Tesla will open a factory in Berlin'"
echo ""
curl -s -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test",
    "text": "Elon Musk announced that Tesla will open a factory in Berlin next year"
  }' | jq '{
    success: .success,
    coherence: .coherence,
    sentiment: .details.sentiment,
    concepts: .details.concepts[:3],
    concept_count: (.details.concepts | length)
  }'

echo ""
echo "========================================"
echo "Enhanced Mode Active!"
echo ""
echo "Check logs: docker-compose logs -f"
echo "Run full tests: ./test_enhanced.sh"
echo "Read docs: cat ENHANCEMENT_GUIDE.md"
echo ""
echo "To switch back to basic mode:"
echo "  DD_USE_ENHANCED=false docker-compose up -d"
echo "========================================"
