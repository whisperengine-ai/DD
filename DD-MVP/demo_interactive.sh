#!/bin/bash
# Enhanced Interactive Demo - Shows all system capabilities

BASE_URL="http://localhost:8000"
DEMO_USER="interactive_demo_$(date +%s)"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "========================================================================"
echo "  🧠 Digital Daemon MVP - Interactive Demo"
echo "========================================================================"
echo ""
echo "Demo User: $DEMO_USER"
echo ""

# Function to show section
show_section() {
    echo ""
    echo -e "${CYAN}========================================================================"
    echo -e "  $1"
    echo -e "========================================================================${NC}"
    echo ""
}

# Function to show input
show_input() {
    echo -e "${YELLOW}📝 Input:${NC} $1"
    echo ""
}

# Function to highlight key output
show_output() {
    echo -e "${GREEN}✓ $1${NC}"
}

# 1. System Health
show_section "1️⃣  System Health Check"
curl -s $BASE_URL/health | jq '{
    status,
    vectors,
    concepts,
    souls
}'

# 2. Basic Virtuous Interaction
show_section "2️⃣  Basic Virtuous Interaction"
show_input "I practice temperance and wisdom daily"
RESPONSE=$(curl -s -X POST $BASE_URL/process \
    -H "Content-Type: application/json" \
    -d '{"user_id":"'$DEMO_USER'","text":"I practice temperance and wisdom daily"}')

echo "$RESPONSE" | jq '{
    success,
    coherence,
    response,
    sentiment: .details.sentiment.label,
    concepts: [.details.concepts[].name]
}'

# 3. Complex Entity Extraction
show_section "3️⃣  Named Entity Recognition & Relationships"
show_input "Dr. Sarah Chen at MIT developed an AI system that respects privacy and promotes fairness"

RESPONSE=$(curl -s -X POST $BASE_URL/process \
    -H "Content-Type: application/json" \
    -d '{"user_id":"'$DEMO_USER'","text":"Dr. Sarah Chen at MIT developed an AI system that respects privacy and promotes fairness"}')

echo "$RESPONSE" | jq '{
    entities: .details.entities,
    relationships: .details.relationships,
    ethical_patterns: .details.ethical_patterns
}'

# 4. Linguistic Analysis
show_section "4️⃣  Deep Linguistic Analysis"
show_input "The wise teacher carefully explained complex philosophical concepts"

RESPONSE=$(curl -s -X POST $BASE_URL/process \
    -H "Content-Type: application/json" \
    -d '{"user_id":"'$DEMO_USER'","text":"The wise teacher carefully explained complex philosophical concepts"}')

echo "$RESPONSE" | jq '.details.linguistic_features | {
    token_count,
    pos_distribution,
    key_lemmas,
    sentence_count,
    dependency_types,
    avg_token_length
}'

# 5. Multi-language/Emoji Support
show_section "5️⃣  Unicode & Emoji Processing"
show_input "I love learning about AI and ethics! 🤖💚 Building with wisdom 🧠"

RESPONSE=$(curl -s -X POST $BASE_URL/process \
    -H "Content-Type: application/json" \
    -d '{"user_id":"'$DEMO_USER'","text":"I love learning about AI and ethics! 🤖💚 Building with wisdom 🧠"}')

echo "$RESPONSE" | jq '{
    success,
    sentiment: .details.sentiment,
    concepts: [.details.concepts[].name]
}'

# 6. Sentiment Analysis Spectrum
show_section "6️⃣  Sentiment Analysis (Positive/Neutral/Negative)"

echo -e "${BLUE}Positive:${NC}"
show_input "This is absolutely wonderful and I'm grateful for it!"
curl -s -X POST $BASE_URL/process \
    -H "Content-Type: application/json" \
    -d '{"user_id":"'$DEMO_USER'","text":"This is absolutely wonderful and I'"'"'m grateful for it!"}' \
    | jq '.details.sentiment'

echo ""
echo -e "${BLUE}Neutral:${NC}"
show_input "The meeting is scheduled for 3 PM today"
curl -s -X POST $BASE_URL/process \
    -H "Content-Type: application/json" \
    -d '{"user_id":"'$DEMO_USER'","text":"The meeting is scheduled for 3 PM today"}' \
    | jq '.details.sentiment'

echo ""
echo -e "${BLUE}Negative (will be rejected by SLMU):${NC}"
show_input "I hate this and want to harm others"
curl -s -X POST $BASE_URL/process \
    -H "Content-Type: application/json" \
    -d '{"user_id":"'$DEMO_USER'","text":"I hate this and want to harm others"}' \
    | jq '{success, reason: .reason}'

# 7. Semantic Memory
show_section "7️⃣  Semantic Memory & Vector Similarity"

show_input "Machine learning and artificial intelligence are fascinating"
curl -s -X POST $BASE_URL/process \
    -H "Content-Type: application/json" \
    -d '{"user_id":"'$DEMO_USER'","text":"Machine learning and artificial intelligence are fascinating"}' \
    > /dev/null

echo "✓ First memory stored"
echo ""

show_input "AI and ML are revolutionizing technology (semantically similar)"
RESPONSE=$(curl -s -X POST $BASE_URL/process \
    -H "Content-Type: application/json" \
    -d '{"user_id":"'$DEMO_USER'","text":"AI and ML are revolutionizing technology"}')

echo "$RESPONSE" | jq '{
    similar_memories: [.details.similar_memories[] | {
        text: .document,
        distance
    }]
}'

# 8. Soul Evolution
show_section "8️⃣  Soul State & Evolution"

show_output "Soul after multiple interactions:"
curl -s $BASE_URL/soul/$DEMO_USER | jq '{
    user_id,
    alignment_score,
    interaction_count,
    vector_snapshot: [.vector[0], .vector[1], .vector[2], "..."]
}'

# 9. Triad Architecture Visibility
show_section "9️⃣  Triad Architecture Outputs"

RESPONSE=$(curl -s -X POST $BASE_URL/process \
    -H "Content-Type: application/json" \
    -d '{"user_id":"'$DEMO_USER'","text":"I seek to understand wisdom and virtue"}')

echo "$RESPONSE" | jq '{
    chroma_triad: {
        vector_id: .details.triad_outputs.chroma_vector_id,
        embedding_dim: .details.triad_outputs.chroma_embedding_dim,
        similar_memories: .details.triad_outputs.chroma_similar_count
    },
    prismo_triad: {
        concepts: .details.triad_outputs.prismo_concept_count,
        entities: .details.triad_outputs.prismo_entity_count,
        sentences: .details.triad_outputs.prismo_sentence_count
    },
    anchor_triad: {
        interaction_count: .details.triad_outputs.anchor_interaction_count
    },
    corpus_callosum: {
        coherence: .coherence,
        soul_alignment: .details.soul_alignment
    }
}'

# 10. SLMU Ethical Compliance
show_section "🔟  SLMU Ethical Compliance System"

echo -e "${GREEN}✓ Virtuous text (passes):${NC}"
show_input "I practice respect, compassion, and temperance in my life"
curl -s -X POST $BASE_URL/process \
    -H "Content-Type: application/json" \
    -d '{"user_id":"'$DEMO_USER'","text":"I practice respect, compassion, and temperance in my life"}' \
    | jq '{
        success,
        compliance: .details.slmu_compliance
    }'

echo ""
echo -e "${YELLOW}⚠ Command patterns (passes with warning):${NC}"
show_input "Practice wisdom and seek understanding always"
curl -s -X POST $BASE_URL/process \
    -H "Content-Type: application/json" \
    -d '{"user_id":"'$DEMO_USER'","text":"Practice wisdom and seek understanding always"}' \
    | jq '{
        success,
        command_patterns_found: .details.slmu_compliance.command_patterns_found
    }'

# Summary
show_section "📊 Demo Summary"

echo "Total interactions for this demo: $(curl -s $BASE_URL/soul/$DEMO_USER | jq '.interaction_count')"
echo ""
echo -e "${GREEN}✓ Demo complete!${NC}"
echo ""
echo "Key capabilities demonstrated:"
echo "  ✓ Health monitoring"
echo "  ✓ Natural language processing (spaCy pipeline)"
echo "  ✓ Named entity recognition"
echo "  ✓ Relationship extraction"
echo "  ✓ Sentiment analysis (RoBERTa)"
echo "  ✓ Semantic embeddings (sentence-transformers)"
echo "  ✓ Vector similarity (ChromaDB)"
echo "  ✓ Ethical compliance (SLMU)"
echo "  ✓ Soul evolution tracking"
echo "  ✓ Triadic cognitive architecture"
echo ""
echo "Explore further:"
echo "  • API Docs: http://localhost:8000/docs"
echo "  • Health: http://localhost:8000/health"
echo "  • Your soul: curl http://localhost:8000/soul/$DEMO_USER"
echo ""
