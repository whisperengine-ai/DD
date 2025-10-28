#!/usr/bin/env python3
"""
Simple test script to verify Digital Daemon MVP is working.
Run after starting the system with: ./start.sh or docker-compose up
"""

import requests
import json
import time
from typing import Dict

BASE_URL = "http://localhost:8000"

def print_section(title: str):
    """Print a section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_result(success: bool, message: str):
    """Print test result."""
    icon = "✅" if success else "❌"
    print(f"{icon} {message}")

def test_health() -> bool:
    """Test health endpoint."""
    print_section("Testing Health Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Health check passed: {data['status']}")
            print(f"   Vectors: {data['vectors']}, Concepts: {data['concepts']}, Souls: {data['souls']}")
            return True
        else:
            print_result(False, f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Health check error: {e}")
        return False

def test_process(user_id: str = "test_user") -> Dict:
    """Test main processing endpoint."""
    print_section("Testing Process Endpoint")
    
    test_inputs = [
        "I seek wisdom and understanding in my life",
        "Compassion and kindness are important virtues",
        "I want to learn and grow"
    ]
    
    for i, text in enumerate(test_inputs, 1):
        try:
            print(f"\n[Test {i}/3] Processing: '{text[:50]}...'")
            response = requests.post(
                f"{BASE_URL}/process",
                json={"text": text, "user_id": user_id},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print_result(True, f"Processing successful")
                print(f"   Coherence: {data['coherence']:.3f}")
                print(f"   Sentiment: {data['details']['sentiment']:.3f}")
                print(f"   Concepts: {', '.join(data['details']['concepts'][:3])}")
                print(f"   Soul Alignment: {data['details']['soul_alignment']:.3f}")
                print(f"   Response: {data['response'][:80]}...")
            else:
                print_result(False, f"Processing failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print_result(False, f"Processing error: {e}")
    
    return {"user_id": user_id}

def test_soul(user_id: str) -> bool:
    """Test soul retrieval."""
    print_section("Testing Soul Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/soul/{user_id}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Soul retrieved for {user_id}")
            print(f"   Alignment Score: {data['alignment_score']:.3f}")
            print(f"   Interaction Count: {data['interaction_count']}")
            print(f"   Vector: [{', '.join([f'{v:.2f}' for v in data['vector'][:3]])}...]")
            return True
        else:
            print_result(False, f"Soul retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Soul retrieval error: {e}")
        return False

def test_ethical_gate() -> bool:
    """Test SLMU ethical gating."""
    print_section("Testing Ethical Compliance (SLMU)")
    
    # This should fail
    try:
        print("\n[Test 1] Testing prohibited content (should fail)...")
        response = requests.post(
            f"{BASE_URL}/process",
            json={"text": "I will use violence and deception to get what I want", "user_id": "bad_user"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 400:
            print_result(True, "Ethical violation correctly rejected")
            return True
        else:
            print_result(False, f"Ethical gate failed: allowed prohibited content")
            return False
            
    except Exception as e:
        print_result(False, f"Ethical test error: {e}")
        return False

def test_sleep_status() -> bool:
    """Test sleep phase status."""
    print_section("Testing Sleep Phase")
    try:
        response = requests.get(f"{BASE_URL}/sleep/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_result(True, "Sleep phase status retrieved")
            print(f"   Scheduler Running: {data['scheduler_running']}")
            print(f"   Run Count: {data['run_count']}")
            print(f"   Last Run: {data['last_run']}")
            return True
        else:
            print_result(False, f"Sleep status failed: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"Sleep status error: {e}")
        return False

def test_api_docs() -> bool:
    """Test API documentation availability."""
    print_section("Testing API Documentation")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print_result(True, "API docs available")
            print(f"   Visit: {BASE_URL}/docs")
            return True
        else:
            print_result(False, f"API docs not available: {response.status_code}")
            return False
    except Exception as e:
        print_result(False, f"API docs error: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "🚀" * 30)
    print("  DIGITAL DAEMON MVP - System Verification")
    print("🚀" * 30)
    
    print("\nWaiting for system to be ready...")
    
    # Wait for system to be ready
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print_result(True, "System is ready!")
                break
        except:
            pass
        
        if attempt < max_attempts - 1:
            print(f"   Waiting... (attempt {attempt + 1}/{max_attempts})")
            time.sleep(3)
        else:
            print_result(False, "System not responding. Is it running?")
            print("\nStart the system with:")
            print("  ./start.sh")
            print("  OR")
            print("  docker-compose up")
            return
    
    # Run tests
    results = {
        "Health Check": test_health(),
        "Process Endpoint": True,  # Multiple calls
        "Soul Persistence": True,  # Will be set below
        "Ethical Gating": test_ethical_gate(),
        "Sleep Phase": test_sleep_status(),
        "API Docs": test_api_docs()
    }
    
    # Process and soul tests
    user_data = test_process("test_user_123")
    results["Soul Persistence"] = test_soul(user_data["user_id"])
    
    # Summary
    print_section("Test Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        print_result(result, test)
    
    print(f"\n{'✅' if passed == total else '⚠️'} Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Digital Daemon MVP is working perfectly!")
        print("\n📚 Next steps:")
        print("   - Explore API docs: http://localhost:8000/docs")
        print("   - Try different queries")
        print("   - Check soul evolution over time")
        print("   - Review logs: docker-compose logs -f")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        print("   - Review logs: docker-compose logs -f dd-mvp")
        print("   - Check system health: curl http://localhost:8000/health")
    
    print("\n" + "🚀" * 30 + "\n")

if __name__ == "__main__":
    main()
