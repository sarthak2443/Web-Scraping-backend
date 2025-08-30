#!/bin/bash
# Setup script for Stock Market Sentiment Analysis Pipeline
# Works on Unix/Linux/MacOS systems

echo "🚀 Setting up Stock Market Sentiment Analysis Pipeline..."
echo "=" * 60

# Check Python version
python_version=$(python3 --version 2>&1)
if [ $? -eq 0 ]; then
    echo "✅ Python found: $python_version"
else
    echo "❌ Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Create necessary directories
echo "📁 Creating data directory..."
mkdir -p data

# Run a quick test
echo "🧪 Running pipeline test..."
python -m src.orchestrator

echo ""
echo "=" * 60
echo "✅ Setup complete!"
echo ""
echo "🎯 Quick start:"
echo "   source .venv/bin/activate    # Activate environment"
echo "   python -m src.orchestrator   # Run pipeline"
echo "   python analyze_output.py     # Analyze results"
echo ""
echo "📊 Generated files:"
echo "   • data/tweets.parquet - Tweet data"
echo "   • data/signals.parquet - Trading signals"
echo ""
echo "📚 Documentation:"
echo "   • README.md - Project overview"
echo "   • docs/design.md - Technical documentation"
