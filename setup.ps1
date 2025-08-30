# Setup script for Stock Market Sentiment Analysis Pipeline
# PowerShell script for Windows systems

Write-Host "🚀 Setting up Stock Market Sentiment Analysis Pipeline..." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Yellow

# Check Python version
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "📦 Creating virtual environment..." -ForegroundColor Blue
python -m venv .venv

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
& .\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Blue
python -m pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
Write-Host "🌐 Installing Playwright browsers..." -ForegroundColor Blue
playwright install chromium

# Create necessary directories
Write-Host "📁 Creating data directory..." -ForegroundColor Blue
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data"
}

# Run a quick test
Write-Host "🧪 Running pipeline test..." -ForegroundColor Blue
python -m src.orchestrator

Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Quick start:" -ForegroundColor Cyan
Write-Host "   .\.venv\Scripts\Activate.ps1    # Activate environment"
Write-Host "   python -m src.orchestrator      # Run pipeline"
Write-Host "   python analyze_output.py        # Analyze results"
Write-Host ""
Write-Host "📊 Generated files:" -ForegroundColor Cyan
Write-Host "   • data/tweets.parquet - Tweet data"
Write-Host "   • data/signals.parquet - Trading signals"
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   • README.md - Project overview"
Write-Host "   • docs/design.md - Technical documentation"
