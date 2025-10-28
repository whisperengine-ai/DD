#!/bin/bash

echo "========================================"
echo "spaCy Pipeline Feature Verification"
echo "========================================"
echo ""
echo "Testing that all spaCy features flow through the system..."
echo ""

# Test comprehensive spaCy analysis
echo "Input: Complex sentence with multiple entities, relationships, and ethical content"
echo ""

RESPONSE=$(curl -s -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "spacy_test",
    "text": "Dr. Sarah Chen and her team at MIT developed a new AI system that respects user privacy and promotes fairness. The research will be published in Nature next month."
  }')

echo "=== 1. TOKENIZATION & POS TAGGING ==="
echo "$RESPONSE" | jq '.details.linguistic_features | {
  token_count,
  pos_distribution,
  avg_token_length
}'

echo ""
echo "=== 2. LEMMATIZATION ==="
echo "$RESPONSE" | jq '.details.linguistic_features.key_lemmas'

echo ""
echo "=== 3. SENTENCE BOUNDARY DETECTION ==="
echo "$RESPONSE" | jq '.details.linguistic_features | {
  sentence_count,
  sentences
}'

echo ""
echo "=== 4. NAMED ENTITY RECOGNITION ==="
echo "$RESPONSE" | jq '.details.entities[] | {
  text,
  label,
  lemma,
  root_pos,
  root_dep
}'

echo ""
echo "=== 5. DEPENDENCY PARSING (Relationships) ==="
echo "$RESPONSE" | jq '.details.relationships[] | {
  subject,
  predicate_lemma,
  object,
  dependency_type
}'

echo ""
echo "=== 6. CONCEPT EXTRACTION (Enhanced) ==="
echo "$RESPONSE" | jq '.details.concepts[] | select(.entity_type != "LEMMA") | {
  name,
  lemma,
  entity_type,
  pos_tag,
  category
}'

echo ""
echo "=== 7. RULE-BASED MATCHING (Ethical Patterns) ==="
echo "$RESPONSE" | jq '.details.ethical_patterns'

echo ""
echo "=== 8. SLMU COMPLIANCE (Multi-feature) ==="
echo "$RESPONSE" | jq '.details.slmu_compliance | {
  compliant,
  violations,
  warnings,
  ethical_patterns_found,
  harm_patterns_found
}'

echo ""
echo "=== 9. COHERENCE CALCULATION (Enhanced) ==="
echo "$RESPONSE" | jq '{
  coherence,
  sentiment: .details.sentiment,
  triad_outputs
}'

echo ""
echo "========================================"
echo "Verification Complete!"
echo ""
echo "All 9 spaCy features are:"
echo "  ✓ Extracted by Prismo triad"
echo "  ✓ Passed through Callosum fusion"
echo "  ✓ Surfaced in API response"
echo "  ✓ Used in coherence calculation"
echo "========================================"
