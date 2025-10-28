"""
Integration tests for FastAPI application
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert 'name' in data
    assert 'version' in data


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert 'status' in data
    assert data['status'] == 'healthy'


def test_process_endpoint():
    """Test main processing endpoint."""
    response = client.post("/process", json={
        "text": "I am seeking wisdom and understanding",
        "user_id": "test_123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    assert 0 <= data['coherence'] <= 1
    assert 'response' in data
    assert 'details' in data


def test_process_endpoint_with_session():
    """Test processing with session ID."""
    session_id = "test_session_456"
    response = client.post("/process", json={
        "text": "Hello world",
        "user_id": "test_user",
        "session_id": session_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data['details']['session_id'] == session_id


def test_soul_persistence():
    """Test that soul is created and persists."""
    user_id = "soul_test_user"
    
    # First request
    response1 = client.post("/process", json={
        "text": "I seek compassion and kindness",
        "user_id": user_id
    })
    assert response1.status_code == 200
    
    # Get soul
    response2 = client.get(f"/soul/{user_id}")
    assert response2.status_code == 200
    soul1 = response2.json()
    assert soul1['user_id'] == user_id
    assert 'alignment_score' in soul1
    
    # Second request
    response3 = client.post("/process", json={
        "text": "Wisdom and understanding are virtues",
        "user_id": user_id
    })
    assert response3.status_code == 200
    
    # Get updated soul
    response4 = client.get(f"/soul/{user_id}")
    soul2 = response4.json()
    
    # Check that interaction count increased
    assert soul2['interaction_count'] == soul1['interaction_count'] + 2


def test_non_compliant_input():
    """Test that non-compliant input is rejected."""
    response = client.post("/process", json={
        "text": "I will use violence and harm to achieve my goals",
        "user_id": "test_bad_user"
    })
    assert response.status_code == 400  # Bad request due to ethical violation


def test_soul_stats_endpoint():
    """Test soul stats endpoint."""
    user_id = "stats_test_user"
    
    # Create some activity
    client.post("/process", json={
        "text": "Test input",
        "user_id": user_id
    })
    
    # Get stats
    response = client.get(f"/soul/{user_id}/stats")
    assert response.status_code == 200
    data = response.json()
    assert 'alignment_score' in data
    assert 'interaction_count' in data


def test_all_souls_stats():
    """Test aggregate soul statistics."""
    response = client.get("/souls/stats")
    assert response.status_code == 200
    data = response.json()
    assert 'system_stats' in data
    assert 'total_users' in data


def test_invalid_input():
    """Test that invalid input is rejected."""
    response = client.post("/process", json={
        "text": "",  # Empty text
        "user_id": "test_user"
    })
    assert response.status_code == 422  # Validation error


def test_missing_user_id():
    """Test that missing user_id is rejected."""
    response = client.post("/process", json={
        "text": "Test text"
        # Missing user_id
    })
    assert response.status_code == 422  # Validation error
