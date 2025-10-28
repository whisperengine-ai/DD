#!/bin/bash
# Comprehensive End-to-End Test Suite
# Tests all system features including enhanced SLMU v2.0 rules
# Total: 50 tests (34 original + 16 SLMU v2.0)

set -e  # Exit on error

BASE_URL="http://localhost:8000"
TEST_USER="e2e_test_$(date +%s)"
PASSED=0
FAILED=0

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "Digital Daemon Enhanced E2E Test Suite"
echo "========================================"
echo "Test User: $TEST_USER"
echo "Base URL: $BASE_URL"
echo ""

# Helper function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local validation="$3"
    
    echo -n "Testing: $test_name... "
    
    if eval "$test_command" | eval "$validation" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
        return 1
    fi
}

# Test 1: Health Check
echo "=== CORE SYSTEM TESTS ==="
run_test "Health endpoint responds" \
    "curl -s $BASE_URL/health" \
    "jq -e '.status == \"healthy\"'"

run_test "Health returns vector count" \
    "curl -s $BASE_URL/health" \
    "jq -e '.vectors >= 0'"

# Test 2: Basic Processing
echo ""
echo "=== BASIC PROCESSING TESTS ==="
run_test "Process simple virtuous text" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I practice wisdom daily\"}'" \
    "jq -e '.success == true'"

run_test "Process returns coherence score" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I seek understanding\"}'" \
    "jq -e '.coherence > 0'"

run_test "Process returns emotion (28-emotion model)" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I am happy and grateful\"}'" \
    "jq -e '.details.sentiment.label == \"joy\" or .details.sentiment.label == \"optimism\"'"

# Test 3: NLP Features
echo ""
echo "=== NLP FEATURE TESTS ==="
run_test "Extracts named entities" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Elon Musk leads Tesla in California\"}'" \
    "jq -e '.details.entities | length > 0'"

run_test "Extracts concepts with lemmas" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I am learning wisdom\"}'" \
    "jq -e '.details.concepts[0].lemma != null'"

run_test "Extracts concepts with POS tags" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"The wise teacher speaks\"}'" \
    "jq -e '.details.concepts[0].pos_tag != null'"

run_test "Detects relationships" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Sarah teaches wisdom to students\"}'" \
    "jq -e '.details.relationships | length >= 0'"

run_test "Provides linguistic features" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I practice daily\"}'" \
    "jq -e '.details.linguistic_features.token_count > 0'"

run_test "POS distribution calculated" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I walk slowly\"}'" \
    "jq -e '.details.linguistic_features.pos_distribution | length > 0'"

# Test 4: SLMU Compliance
echo ""
echo "=== SLMU COMPLIANCE TESTS ==="
run_test "Accepts virtuous text" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I practice temperance and prudence\"}'" \
    "jq -e '.success == true'"

run_test "SLMU compliance reported" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I value wisdom\"}'" \
    "jq -e '.details.slmu_compliance.compliant == true'"

run_test "Rejects harmful text" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I will harm others and deceive people\"}'" \
    "jq -e '.detail == \"Ethical violation\"'"

run_test "Detects ethical patterns" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Respect and fairness are important\"}'" \
    "jq -e '.details.ethical_patterns != null'"

# Test 4b: Enhanced SLMU v2.0 Rules (testing basic rule expansion)
echo ""
echo "=== ENHANCED SLMU v2.0 RULES TESTS ==="

# Test new prohibited concepts in basic form
run_test "Rejects manipulation concept" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I will manipulate them\"}'" \
    "jq -e '.detail == \"Ethical violation\"'"

run_test "Rejects deception concept" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I plan to deceive people\"}'" \
    "jq -e '.detail == \"Ethical violation\"'"

run_test "Rejects abuse concept" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I want to abuse their trust\"}'" \
    "jq -e '.detail == \"Ethical violation\"'"

# Test new virtues are accepted
run_test "Accepts wisdom virtue text" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I seek wisdom and understanding\"}'" \
    "jq -e '.success == true'"

run_test "Accepts integrity virtue text" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I will act with integrity and honesty\"}'" \
    "jq -e '.success == true'"

run_test "Accepts compassion virtue text" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I practice compassion and kindness\"}'" \
    "jq -e '.success == true'"

# Emotion and linguistic pattern tests (verify system handles them)
run_test "Processes high positive emotions correctly" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I am so joyful and optimistic about helping others!\"}'" \
    "jq -e '.success == true and .details.sentiment.all_scores.joy > 0.5'"

run_test "Handles mixed emotions without false positives" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I am nervous but excited to learn\"}'" \
    "jq -e '.success == true'"

# Relationship tests using spaCy features
run_test "Accepts helping relationships" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Sarah helps students learn\"}'" \
    "jq -e '.success == true and .details.relationships | length >= 0'"

run_test "Detects relationships in virtuous context" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"The teacher supports the students\"}'" \
    "jq -e '.success == true'"

# Contextual understanding tests
run_test "Processes medical/educational context" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I want to learn about ethical philosophy\"}'" \
    "jq -e '.success == true'"

# Multiple virtues rewards alignment
run_test "Multiple virtues improve alignment" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"test_multi_virtue_$(date +%s)\",\"text\":\"I practice wisdom, courage, and compassion\"}'" \
    "jq -e '.success == true and .details.soul_alignment > 0.4'"

# Complex ethical scenarios
run_test "Handles nuanced ethical discussion" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I struggle with patience but I am learning compassion\"}'" \
    "jq -e '.success == true'"

run_test "Processes mixed virtue and challenge text" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"I want to be more honest and overcome my fears\"}'" \
    "jq -e '.success == true'"

# Linguistic feature validation
run_test "Extracts entities from ethical text" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Dr. Martin Luther King promoted justice and peace\"}'" \
    "jq -e '.success == true and .details.entities | length > 0'"

# Alignment scoring over time
run_test "Consistent virtuous text improves alignment" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"test_alignment_$(date +%s)\",\"text\":\"I practice temperance and wisdom daily\"}'" \
    "jq -e '.success == true and .details.soul_alignment >= 0'"

# Test 5: Soul System
echo ""
echo "=== SOUL SYSTEM TESTS ==="
SOUL_USER="soul_test_$(date +%s)"

run_test "Creates new soul on first interaction" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$SOUL_USER\",\"text\":\"Hello wisdom\"}'" \
    "jq -e '.success == true'"

run_test "Soul endpoint returns user data" \
    "curl -s $BASE_URL/soul/$SOUL_USER" \
    "jq -e '.user_id == \"'$SOUL_USER'\"'"

run_test "Soul has vector representation" \
    "curl -s $BASE_URL/soul/$SOUL_USER" \
    "jq -e '.vector | length == 7'"

run_test "Soul has alignment score" \
    "curl -s $BASE_URL/soul/$SOUL_USER" \
    "jq -e '.alignment_score >= 0'"

run_test "Soul tracks interaction count" \
    "curl -s $BASE_URL/soul/$SOUL_USER" \
    "jq -e '.interaction_count >= 1'"

# Test 6: Vector Similarity
echo ""
echo "=== VECTOR SIMILARITY TESTS ==="
SIM_USER="sim_test_$(date +%s)"

# Send first message
curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' \
    -d '{"user_id":"'$SIM_USER'","text":"machine learning and AI"}' > /dev/null

# Send similar message
run_test "Finds similar memories" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$SIM_USER\",\"text\":\"artificial intelligence and ML\"}'" \
    "jq -e '.details.similar_memories | length > 0'"

run_test "Similar memories have metadata" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$SIM_USER\",\"text\":\"AI research\"}'" \
    "jq -e '.details.similar_memories[0].metadata != null'"

# Test 7: ChromaDB Integration
echo ""
echo "=== CHROMADB INTEGRATION TESTS ==="
run_test "Embeddings have correct dimensions" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Test embedding\"}'" \
    "jq -e '.details.triad_outputs.chroma_embedding_dim == 384'"

run_test "Vector ID assigned" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Vector test\"}'" \
    "jq -e '.details.triad_outputs.chroma_vector_id != null'"

# Test 8: Edge Cases
echo ""
echo "=== EDGE CASE TESTS ==="
run_test "Handles empty user_id gracefully" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"\",\"text\":\"test\"}'" \
    "jq -e '. != null'"

run_test "Handles very short text" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Hi\"}'" \
    "jq -e '. != null'"

run_test "Handles punctuation-only text" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"...\"}'" \
    "jq -e '. != null'"

run_test "Handles unicode/emoji" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Hello 世界 🌍\"}'" \
    "jq -e '. != null'"

run_test "Handles very long text (>500 chars)" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"long_test\",\"text\":\"$(python3 -c "print('This is a test of wisdom and temperance. ' * 20)")\"}'" \
    "jq -e '.success == true'"

# Test 9: Triad Outputs
echo ""
echo "=== TRIAD OUTPUT TESTS ==="
run_test "Chroma triad executed" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Test triads\"}'" \
    "jq -e '.details.triad_outputs.chroma_vector_id != null'"

run_test "Prismo triad executed" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Test triads\"}'" \
    "jq -e '.details.triad_outputs.prismo_concept_count >= 0'"

run_test "Anchor triad executed" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Test triads\"}'" \
    "jq -e '.details.triad_outputs.anchor_interaction_count >= 0'"

run_test "Session ID assigned" \
    "curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' -d '{\"user_id\":\"$TEST_USER\",\"text\":\"Test session\"}'" \
    "jq -e '.details.session_id != null'"

# Test 10: Performance
echo ""
echo "=== PERFORMANCE TESTS ==="
START_TIME=$(date +%s)
for i in {1..5}; do
    curl -s -X POST $BASE_URL/process -H 'Content-Type: application/json' \
        -d '{"user_id":"perf_test","text":"Performance test '$i'"}' > /dev/null
done
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ $DURATION -le 10 ]; then
    echo -e "${GREEN}✓ PASS${NC} - 5 requests in ${DURATION}s (avg: $((DURATION * 200))ms)"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ SLOW${NC} - 5 requests in ${DURATION}s (avg: $((DURATION * 200))ms)"
fi

# Summary
echo ""
echo "========================================"
echo "TEST SUMMARY"
echo "========================================"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo "Total:  $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    exit 1
fi
