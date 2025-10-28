#!/bin/bash

# Digital Daemon MVP - Quick Start Script

echo "=================================="
echo "Digital Daemon MVP - Quick Start"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    echo "   Visit: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is installed and running"
echo ""

# Create .env from example if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🏗️  Building and starting Digital Daemon..."
echo ""

# Build and run
docker-compose up --build -d

echo ""
echo "⏳ Waiting for services to start (30 seconds)..."
sleep 30

# Check health
echo ""
echo "🔍 Checking system health..."
HEALTH=$(curl -s http://localhost:8000/health || echo "failed")

if [[ "$HEALTH" == "failed" ]]; then
    echo "❌ Service is not responding. Checking logs..."
    docker-compose logs --tail=50
    exit 1
fi

echo "✅ System is healthy!"
echo ""
echo "=================================="
echo "🚀 Digital Daemon MVP is running!"
echo "=================================="
echo ""
echo "📍 API Endpoints:"
echo "   - Root:          http://localhost:8000/"
echo "   - Health:        http://localhost:8000/health"
echo "   - API Docs:      http://localhost:8000/docs"
echo "   - ReDoc:         http://localhost:8000/redoc"
echo ""
echo "📖 Try it out:"
echo '   curl -X POST http://localhost:8000/process \\'
echo '     -H "Content-Type: application/json" \\'
echo '     -d '"'"'{"text": "I seek wisdom", "user_id": "demo"}'"'"
echo ""
echo "📋 Useful commands:"
echo "   - View logs:     docker-compose logs -f"
echo "   - Stop:          docker-compose down"
echo "   - Restart:       docker-compose restart"
echo "   - Rebuild:       docker-compose up --build"
echo ""
echo "✨ Happy exploring!"
