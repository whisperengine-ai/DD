"""
Tests for Chroma Triad
"""
import pytest
import numpy as np
import sys
from pathlib import Path
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from triads.chroma import ChromaTriad
from vector_store import SimpleVectorStore


@pytest.fixture
def vector_store():
    """Create temporary vector store for testing."""
    with tempfile.NamedTemporaryFile(suffix='.npz', delete=False) as f:
        vs = SimpleVectorStore(f.name)
        yield vs
        # Cleanup
        Path(f.name).unlink(missing_ok=True)


@pytest.fixture
def chroma(vector_store):
    """Create Chroma triad instance."""
    return ChromaTriad(vector_store)


def test_chroma_sentiment_positive(chroma):
    """Test positive sentiment detection."""
    result = chroma.process("I love this! It's wonderful and great!", "test_user")
    assert result['sentiment'] > 0.5, "Should detect positive sentiment"


def test_chroma_sentiment_negative(chroma):
    """Test negative sentiment detection."""
    result = chroma.process("This is terrible and awful. I hate it.", "test_user")
    assert result['sentiment'] < 0.5, "Should detect negative sentiment"


def test_chroma_sentiment_neutral(chroma):
    """Test neutral sentiment detection."""
    result = chroma.process("The sky is blue and grass is green.", "test_user")
    assert 0.4 <= result['sentiment'] <= 0.6, "Should detect neutral sentiment"


def test_chroma_vector_dimensions(chroma):
    """Test that output vector has correct dimensions (7D ROYGBIV)."""
    result = chroma.process("Test text", "test_user")
    assert 'color_vector' in result
    assert len(result['color_vector']) == 7, "Should be 7-dimensional"


def test_chroma_vector_normalization(chroma):
    """Test that vectors are normalized (unit vectors)."""
    result = chroma.process("Test text", "test_user")
    vector = np.array(result['color_vector'])
    norm = np.linalg.norm(vector)
    assert 0.99 < norm < 1.01, "Vector should be normalized to unit length"


def test_chroma_stores_vectors(chroma, vector_store):
    """Test that Chroma stores vectors in the vector store."""
    initial_count = vector_store.count()
    chroma.process("Test text", "test_user")
    assert vector_store.count() == initial_count + 1


def test_chroma_similar_memories(chroma):
    """Test that similar memories are retrieved."""
    # Store some vectors
    chroma.process("I love happiness", "test_user")
    chroma.process("Joy brings peace", "test_user")
    
    # Query
    result = chroma.process("I am happy and joyful", "test_user")
    assert 'similar_memories' in result
    assert len(result['similar_memories']) <= 3
