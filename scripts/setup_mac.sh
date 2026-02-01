#!/bin/bash
# Hey Arnie Wake Word - Mac Setup Script
# Run this FROM the cloned repo folder!
#
# Usage:
#   cd ~/Dev/hey-arnie-wakeword
#   chmod +x scripts/setup_mac.sh
#   ./scripts/setup_mac.sh

set -e

echo "🏋️ ARNIE WAKE WORD TRAINING SETUP"
echo "=================================="
echo ""

# Get the directory where the repo is (parent of scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "📁 Project directory: $PROJECT_DIR"
cd "$PROJECT_DIR"

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew found"
fi

# Check for Python 3.9+
if ! command -v python3 &> /dev/null; then
    echo "📦 Installing Python 3..."
    brew install python@3.11
else
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    echo "✅ Python $PYTHON_VERSION found"
fi

# Install system dependencies
echo ""
echo "📦 Installing system dependencies..."
brew install ffmpeg sox

# Create virtual environment IN the project directory
echo ""
echo "🐍 Creating Python virtual environment..."
python3 -m venv "$PROJECT_DIR/venv"
source "$PROJECT_DIR/venv/bin/activate"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install tensorflow==2.15.0
pip install numpy scipy librosa soundfile
pip install sounddevice  # For Mac microphone recording
pip install piper-tts  # For synthetic sample generation

# Create sample directories (if not exist)
mkdir -p "$PROJECT_DIR/samples/positive"
mkdir -p "$PROJECT_DIR/samples/negative"
mkdir -p "$PROJECT_DIR/trained_model"

echo ""
echo "✅ SETUP COMPLETE!"
echo ""
echo "Your project is at: $PROJECT_DIR"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_DIR"
echo "  source venv/bin/activate"
echo "  python scripts/generate_samples.py"
echo ""
echo "💪 LET'S DO THIS!"
