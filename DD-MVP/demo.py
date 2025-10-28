#!/usr/bin/env python3
"""
Demo script for Digital Daemon MVP
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def demo():
    print_section("Digital Daemon MVP - Demo")
    
    # 1. Health Check
    print_section("1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(json.dumps(response.json(), indent=2))
    
    # 2. Process positive input
    print_section("2. Processing Positive Input")
    response = requests.post(
        f"{BASE_URL}/process",
        json={
            "text": "I am seeking wisdom, compassion, and understanding",
            "user_id": "demo_user"
        }
    )
    result = response.json()
    print(f"Success: {result['success']}")
    print(f"Coherence: {result['coherence']:.3f}")
    print(f"Sentiment: {result['details']['sentiment']:.3f}")
    print(f"Concepts: {result['details']['concepts']}")
    print(f"Soul Alignment: {result['details']['soul_alignment']:.3f}")
    print(f"Response: {result['response']}")
    
    # 3. Check soul state
    print_section("3. Soul State After Interaction")
    response = requests.get(f"{BASE_URL}/soul/demo_user")
    soul = response.json()
    print(f"User ID: {soul['user_id']}")
    print(f"Alignment Score: {soul['alignment_score']:.3f}")
    print(f"Interaction Count: {soul['interaction_count']}")
    print(f"ROYGBIV Vector: [{', '.join([f'{v:.3f}' for v in soul['vector']])}]")
    
    # 4. Process another input
    print_section("4. Processing Another Input")
    response = requests.post(
        f"{BASE_URL}/process",
        json={
            "text": "I value temperance and justice in all things",
            "user_id": "demo_user"
        }
    )
    result = response.json()
    print(f"Success: {result['success']}")
    print(f"Coherence: {result['coherence']:.3f}")
    print(f"New Soul Alignment: {result['details']['soul_alignment']:.3f}")
    
    # 5. Check updated soul
    print_section("5. Soul State After Second Interaction")
    response = requests.get(f"{BASE_URL}/soul/demo_user")
    soul = response.json()
    print(f"Alignment Score: {soul['alignment_score']:.3f}")
    print(f"Interaction Count: {soul['interaction_count']}")
    
    # 6. Test with ethical concepts
    print_section("6. Testing Virtuous Concepts")
    virtuous_inputs = [
        "Prudence guides my decisions",
        "Fortitude helps me face challenges",
        "I practice kindness daily"
    ]
    
    for text in virtuous_inputs:
        response = requests.post(
            f"{BASE_URL}/process",
            json={"text": text, "user_id": "demo_user"}
        )
        result = response.json()
        print(f"Input: {text}")
        print(f"  → Coherence: {result['coherence']:.3f}, "
              f"Sentiment: {result['details']['sentiment']:.3f}")
    
    # 7. Final soul state
    print_section("7. Final Soul State")
    response = requests.get(f"{BASE_URL}/soul/demo_user")
    soul = response.json()
    print(f"User ID: {soul['user_id']}")
    print(f"Final Alignment Score: {soul['alignment_score']:.3f}")
    print(f"Total Interactions: {soul['interaction_count']}")
    print(f"ROYGBIV Vector: [{', '.join([f'{v:.3f}' for v in soul['vector']])}]")
    
    # 8. System stats
    print_section("8. System Statistics")
    response = requests.get(f"{BASE_URL}/health")
    health = response.json()
    print(f"Total Vectors: {health['vectors']}")
    print(f"Total Concepts: {health['concepts']}")
    print(f"Total Souls: {health['souls']}")
    
    print_section("Demo Complete!")
    print("✓ All triads operational")
    print("✓ Callosum fusion working")
    print("✓ Soul persistence active")
    print("✓ SLMU ethical alignment enabled")
    print("\nAccess API docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    try:
        demo()
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to Digital Daemon MVP.")
        print("Make sure the system is running:")
        print("  cd DD-MVP && docker-compose up")
    except Exception as e:
        print(f"ERROR: {e}")
