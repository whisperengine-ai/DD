#!/bin/bash

echo "========================================"
echo "Digital Daemon Enhanced NLP Test"
echo "========================================"
echo ""

# Test 1: Rich sentiment with emojis and slang
echo "Test 1: Enhanced Sentiment Analysis"
echo "Input: 'This is absolutely terrible and I hate it! 😡'"
curl -s -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_sentiment",
    "text": "This is absolutely terrible and I hate it! 😡"
  }' | jq '.details.sentiment'

echo ""
echo "----------------------------------------"
echo ""

# Test 2: Complex entity extraction
echo "Test 2: Enhanced Entity Extraction"
echo "Input: 'Elon Musk announced that Tesla will open a factory in Berlin next year for €500 million'"
curl -s -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_entities",
    "text": "Elon Musk announced that Tesla will open a factory in Berlin next year for €500 million"
  }' | jq '{
    entities: .details.entities,
    concepts: .details.concepts[:5],
    relationships: .details.relationships,
    linguistic: .details.linguistic_features
  }'

echo ""
echo "----------------------------------------"
echo ""

# Test 3: Semantic similarity
echo "Test 3: Vector Similarity (send 2 related messages)"
echo "Message 1: 'I love machine learning and artificial intelligence'"
curl -s -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_similarity",
    "text": "I love machine learning and artificial intelligence"
  }' > /dev/null

echo "Message 2: 'Neural networks and deep learning are fascinating'"
RESULT=$(curl -s -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_similarity",
    "text": "Neural networks and deep learning are fascinating"
  }')

echo "$RESULT" | jq '.details.similar_memories'

echo ""
echo "----------------------------------------"
echo ""

# Test 4: System health
echo "Test 4: System Health Check"
curl -s http://localhost:8000/health | jq '.'

echo ""
echo "========================================"
echo "Tests Complete!"
echo ""
echo "Enhanced features to look for:"
echo "  ✓ Sentiment with all_scores (negative/neutral/positive)"
echo "  ✓ Entities with lemma, pos_tag, and root_dep"
echo "  ✓ Concepts with entity_type, lemma, category"
echo "  ✓ Relationships with predicate_lemma and dependency_type"
echo "  ✓ Linguistic features (token_count, pos_distribution, key_lemmas)"
echo "  ✓ Ethical patterns (harm/ethical/command detection)"
echo "  ✓ SLMU compliance with multi-feature analysis"
echo "  ✓ Similar memories with actual semantic matches"
echo "  ✓ Higher coherence scores based on linguistic richness"
echo "========================================"
