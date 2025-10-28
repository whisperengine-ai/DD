"""
Tests for Prismo Triad
"""
import pytest
import sys
from pathlib import Path
import tempfile
import sqlite3

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from triads.prismo import PrismoTriad
from slmu import get_default_rules


@pytest.fixture
def prismo():
    """Create Prismo triad instance with temporary database."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        rules = get_default_rules()
        p = PrismoTriad(f.name, rules)
        yield p
        # Cleanup
        p.db.close()
        Path(f.name).unlink(missing_ok=True)


def test_prismo_extracts_concepts(prismo):
    """Test concept extraction."""
    result = prismo.process("Wisdom and Knowledge are important virtues", "test_user")
    assert 'concepts' in result
    assert len(result['concepts']) > 0


def test_prismo_compliant_text(prismo):
    """Test that compliant text passes."""
    result = prismo.process("I seek wisdom, truth, and compassion", "test_user")
    assert result['compliant'] is True


def test_prismo_non_compliant_text(prismo):
    """Test that non-compliant text is rejected."""
    result = prismo.process("I will use violence and deception", "test_user")
    assert result['compliant'] is False


def test_prismo_stores_concepts(prismo):
    """Test that concepts are stored in database."""
    initial_count = prismo.get_concept_count()
    prismo.process("Wisdom is a virtue", "test_user")
    assert prismo.get_concept_count() > initial_count


def test_prismo_finds_related_concepts(prismo):
    """Test that related concepts are found."""
    prismo.process("Wisdom is important", "test_user")
    prismo.process("Wise people are virtuous", "test_user")
    
    result = prismo.process("Wisdom guides us", "test_user")
    assert 'related' in result
