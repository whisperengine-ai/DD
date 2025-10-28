#!/usr/bin/env python3
"""
Run Digital Daemon MVP natively (without Docker).

This script starts the FastAPI server with proper configuration
for local development.
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Set environment variables for native run
os.environ.setdefault("DD_USE_ENHANCED", "true")
os.environ.setdefault("DD_ENV", "native")

def main():
    """Run the FastAPI server."""
    import uvicorn
    
    print("="*60)
    print("Digital Daemon MVP - Native Python Run")
    print("="*60)
    print("")
    print("Environment: Native Python (not Docker)")
    print("Enhanced Mode:", os.environ.get("DD_USE_ENHANCED"))
    print("")
    print("Starting server...")
    print("API: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("")
    print("Press Ctrl+C to stop")
    print("="*60)
    print("")
    
    # Run uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        sys.exit(0)
