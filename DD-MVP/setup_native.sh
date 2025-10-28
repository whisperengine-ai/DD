#!/bin/bash

echo "========================================"
echo "Digital Daemon - Native Python Setup"
echo "========================================"
echo ""
echo "This script sets up a local Python environment"
echo "for running DD-MVP without Docker."
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.11"

if [[ $(echo -e "$PYTHON_VERSION\n$REQUIRED_VERSION" | sort -V | head -n1) != "$REQUIRED_VERSION" ]]; then
    echo "⚠️  Warning: Python 3.11+ recommended, found $PYTHON_VERSION"
    echo "   (May work with 3.9+, but not guaranteed)"
fi

echo "✓ Python version: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "   Recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
    fi
else
    python3 -m venv venv
fi

echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo ""
echo "Installing dependencies..."
echo "(This will download ~1.4GB of ML models)"
echo ""
pip install -r requirements.txt

# Download spaCy model
echo ""
echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm

# Pre-download transformer models
echo ""
echo "Pre-downloading transformer models..."
python download_models.py

# Create data directories
echo ""
echo "Creating data directories..."
mkdir -p data/chromadb
mkdir -p config

echo ""
echo "✓ Setup complete!"
echo ""
echo "========================================"
echo "To run the system:"
echo ""
echo "  1. Activate environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the server:"
echo "     python run_native.py"
echo ""
echo "  3. Access API at:"
echo "     http://localhost:8000"
echo ""
echo "  4. View docs at:"
echo "     http://localhost:8000/docs"
echo ""
echo "To deactivate:"
echo "  deactivate"
echo "========================================"
