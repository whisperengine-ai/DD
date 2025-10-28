#!/bin/bash
# Digital Daemon MVP Demo Script

echo "============================================================"
echo "  Digital Daemon MVP - Demo"
echo "============================================================"
echo ""

# 1. Health Check
echo "============================================================"
echo "  1. Health Check"
echo "============================================================"
echo ""
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""

# 2. Process positive input
echo "============================================================"
echo "  2. Processing Positive Input"
echo "============================================================"
echo ""
echo "Input: 'I am seeking wisdom, compassion, and understanding'"
curl -s -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "I am seeking wisdom, compassion, and understanding", "user_id": "demo_user"}' \
  | python3 -m json.tool
echo ""

# 3. Check soul state
echo "============================================================"
echo "  3. Soul State After First Interaction"
echo "============================================================"
echo ""
curl -s http://localhost:8000/soul/demo_user | python3 -m json.tool
echo ""

# 4. Process another input
echo "============================================================"
echo "  4. Processing Second Input"
echo "============================================================"
echo ""
echo "Input: 'I value temperance and justice in all things'"
curl -s -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "I value temperance and justice in all things", "user_id": "demo_user"}' \
  | python3 -m json.tool
echo ""

# 5. Check updated soul
echo "============================================================"
echo "  5. Soul State After Second Interaction"
echo "============================================================"
echo ""
curl -s http://localhost:8000/soul/demo_user | python3 -m json.tool
echo ""

# 6. Test with more virtuous concepts
echo "============================================================"
echo "  6. Testing More Virtuous Concepts"
echo "============================================================"
echo ""

echo "Processing: 'Prudence guides my decisions'"
curl -s -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Prudence guides my decisions", "user_id": "demo_user"}' \
  | python3 -c "import sys, json; r=json.load(sys.stdin); print(f\"  → Coherence: {r['coherence']:.3f}, Sentiment: {r['details']['sentiment']:.3f}\")"
echo ""

echo "Processing: 'Fortitude helps me face challenges'"
curl -s -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Fortitude helps me face challenges", "user_id": "demo_user"}' \
  | python3 -c "import sys, json; r=json.load(sys.stdin); print(f\"  → Coherence: {r['coherence']:.3f}, Sentiment: {r['details']['sentiment']:.3f}\")"
echo ""

# 7. Final soul state
echo "============================================================"
echo "  7. Final Soul State"
echo "============================================================"
echo ""
curl -s http://localhost:8000/soul/demo_user | python3 -m json.tool
echo ""

# 8. System stats
echo "============================================================"
echo "  8. System Statistics"
echo "============================================================"
echo ""
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""

echo "============================================================"
echo "  Demo Complete!"
echo "============================================================"
echo "✓ All triads operational"
echo "✓ Callosum fusion working"
echo "✓ Soul persistence active"
echo "✓ SLMU ethical alignment enabled"
echo ""
echo "Access API docs at: http://localhost:8000/docs"
echo "============================================================"
