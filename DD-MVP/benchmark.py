#!/usr/bin/env python3
"""
Performance Benchmark for Digital Daemon MVP
Tests throughput, latency, and resource usage
"""
import requests
import time
import statistics
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

BASE_URL = "http://localhost:8000"

# Test messages of varying complexity
TEST_MESSAGES = [
    "I practice wisdom daily",  # Simple
    "The wise teacher carefully explained complex philosophical concepts to eager students",  # Medium
    "Dr. Sarah Chen at MIT developed a groundbreaking AI system that respects privacy, promotes fairness, and demonstrates remarkable capabilities across multiple domains",  # Complex
    "Hello",  # Minimal
    "I seek to understand the nature of wisdom, virtue, and ethical behavior in the context of modern artificial intelligence systems 🤖",  # With emoji
]


def make_request(text: str, user_id: str) -> Dict:
    """Make a single API request and return timing + response info."""
    start = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/process",
            json={"user_id": user_id, "text": text},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        elapsed = time.time() - start
        
        return {
            "success": response.status_code == 200,
            "elapsed": elapsed,
            "status_code": response.status_code,
            "text_length": len(text),
            "response_size": len(response.content)
        }
    except Exception as e:
        elapsed = time.time() - start
        return {
            "success": False,
            "elapsed": elapsed,
            "error": str(e),
            "text_length": len(text)
        }


def test_sequential_latency(iterations: int = 20):
    """Test sequential request latency."""
    print(f"\n📊 Sequential Latency Test ({iterations} requests)")
    print("=" * 60)
    
    latencies = []
    
    for i in range(iterations):
        result = make_request(
            TEST_MESSAGES[i % len(TEST_MESSAGES)],
            f"latency_test_{i}"
        )
        latencies.append(result["elapsed"] * 1000)  # Convert to ms
        print(f"  Request {i+1:2d}: {result['elapsed']*1000:6.1f}ms", end="")
        if not result["success"]:
            print(f" ❌ FAILED")
        else:
            print()
    
    print(f"\n  Mean:   {statistics.mean(latencies):6.1f}ms")
    print(f"  Median: {statistics.median(latencies):6.1f}ms")
    print(f"  P95:    {statistics.quantiles(latencies, n=20)[18]:6.1f}ms")
    print(f"  P99:    {statistics.quantiles(latencies, n=100)[98]:6.1f}ms")
    print(f"  Min:    {min(latencies):6.1f}ms")
    print(f"  Max:    {max(latencies):6.1f}ms")


def test_concurrent_throughput(concurrent: int = 5, requests_per_thread: int = 10):
    """Test concurrent request throughput."""
    print(f"\n🚀 Concurrent Throughput Test")
    print(f"   {concurrent} concurrent threads × {requests_per_thread} requests = {concurrent * requests_per_thread} total")
    print("=" * 60)
    
    start_time = time.time()
    successful = 0
    failed = 0
    latencies = []
    
    with ThreadPoolExecutor(max_workers=concurrent) as executor:
        futures = []
        
        for thread_id in range(concurrent):
            for req_id in range(requests_per_thread):
                message = TEST_MESSAGES[(thread_id * requests_per_thread + req_id) % len(TEST_MESSAGES)]
                future = executor.submit(
                    make_request,
                    message,
                    f"thread{thread_id}_req{req_id}"
                )
                futures.append(future)
        
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            if result["success"]:
                successful += 1
                latencies.append(result["elapsed"] * 1000)
            else:
                failed += 1
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"  Completed: {i+1}/{len(futures)}")
    
    total_time = time.time() - start_time
    throughput = successful / total_time
    
    print(f"\n  Total time:     {total_time:.2f}s")
    print(f"  Successful:     {successful}")
    print(f"  Failed:         {failed}")
    print(f"  Throughput:     {throughput:.1f} req/s")
    
    if latencies:
        print(f"  Mean latency:   {statistics.mean(latencies):.1f}ms")
        print(f"  Median latency: {statistics.median(latencies):.1f}ms")
        print(f"  P95 latency:    {statistics.quantiles(latencies, n=20)[18]:.1f}ms")


def test_text_complexity_scaling():
    """Test how latency scales with text complexity."""
    print(f"\n📏 Text Complexity Scaling Test")
    print("=" * 60)
    
    test_cases = [
        ("Minimal (1 word)", "Hello", 5),
        ("Short (3 words)", "I practice wisdom", 5),
        ("Medium (10 words)", "The wise teacher explained complex concepts to eager students yesterday", 5),
        ("Long (25 words)", "Dr. Sarah Chen and her dedicated research team at MIT developed an innovative AI system that carefully respects user privacy while promoting fairness and demonstrating remarkable capabilities", 5),
        ("Very Long (50 words)", " ".join(["wisdom"] * 50), 3),
    ]
    
    for label, text, iterations in test_cases:
        latencies = []
        for i in range(iterations):
            result = make_request(text, f"complexity_{label}_{i}")
            if result["success"]:
                latencies.append(result["elapsed"] * 1000)
        
        if latencies:
            avg = statistics.mean(latencies)
            print(f"  {label:20s} ({len(text):3d} chars): {avg:6.1f}ms avg")


def test_memory_accumulation(requests: int = 50):
    """Test system behavior with memory accumulation."""
    print(f"\n💾 Memory Accumulation Test ({requests} sequential requests)")
    print("=" * 60)
    
    user_id = "memory_test"
    latencies = []
    
    for i in range(requests):
        result = make_request(
            f"Iteration {i}: I practice wisdom and virtue",
            user_id
        )
        if result["success"]:
            latencies.append(result["elapsed"] * 1000)
        
        if (i + 1) % 10 == 0:
            print(f"  Completed {i+1}/{requests}: {latencies[-1]:.1f}ms")
    
    # Check if latency degrades over time
    first_10 = statistics.mean(latencies[:10])
    last_10 = statistics.mean(latencies[-10:])
    
    print(f"\n  First 10 requests avg: {first_10:.1f}ms")
    print(f"  Last 10 requests avg:  {last_10:.1f}ms")
    print(f"  Degradation:           {((last_10 - first_10) / first_10 * 100):+.1f}%")


def test_endpoint_health():
    """Test health endpoint performance."""
    print(f"\n❤️  Health Endpoint Performance")
    print("=" * 60)
    
    latencies = []
    for _ in range(100):
        start = time.time()
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        elapsed = (time.time() - start) * 1000
        if response.status_code == 200:
            latencies.append(elapsed)
    
    print(f"  Requests:   100")
    print(f"  Success:    {len(latencies)}")
    print(f"  Mean:       {statistics.mean(latencies):.2f}ms")
    print(f"  Median:     {statistics.median(latencies):.2f}ms")
    print(f"  P95:        {statistics.quantiles(latencies, n=20)[18]:.2f}ms")


def test_error_recovery():
    """Test system recovery from error conditions."""
    print(f"\n🔧 Error Recovery Test")
    print("=" * 60)
    
    # Send invalid request
    print("  Sending invalid request...")
    start = time.time()
    try:
        response = requests.post(
            f"{BASE_URL}/process",
            json={"invalid": "data"},
            timeout=5
        )
        print(f"    Response: {response.status_code} in {(time.time() - start)*1000:.1f}ms")
    except Exception as e:
        print(f"    Error: {e}")
    
    # Send valid request immediately after
    print("  Sending valid request after error...")
    result = make_request("I practice wisdom", "recovery_test")
    if result["success"]:
        print(f"    ✓ System recovered: {result['elapsed']*1000:.1f}ms")
    else:
        print(f"    ✗ System still failing")


def main():
    """Run all benchmark tests."""
    print("\n" + "=" * 60)
    print("  🧠 DIGITAL DAEMON MVP - PERFORMANCE BENCHMARK")
    print("=" * 60)
    
    # Check system is up
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"\n❌ System not healthy: {response.status_code}")
            return
    except Exception as e:
        print(f"\n❌ Cannot connect to {BASE_URL}: {e}")
        return
    
    print(f"\n✓ System is UP at {BASE_URL}")
    
    # Run tests
    test_endpoint_health()
    test_sequential_latency(20)
    test_concurrent_throughput(5, 10)
    test_text_complexity_scaling()
    test_memory_accumulation(50)
    test_error_recovery()
    
    print("\n" + "=" * 60)
    print("  ✓ BENCHMARK COMPLETE")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
