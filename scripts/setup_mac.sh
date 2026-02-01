#!/bin/bash
# Hey Arnie Wake Word - Mac Setup Script
# Run this on your Mac to set up the training environment

set -e

echo "🏋️ ARNIE WAKE WORD TRAINING SETUP"
echo "=================================="
echo ""

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

# Create project directory
PROJECT_DIR="$HOME/hey-arnie-wakeword"
echo ""
echo "📁 Setting up project at: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Clone microWakeWord
if [ ! -d "microWakeWord" ]; then
    echo "📥 Cloning microWakeWord repository..."
    git clone https://github.com/kahrendt/microWakeWord.git
else
    echo "✅ microWakeWord already cloned"
fi

# Create virtual environment
echo ""
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install tensorflow==2.15.0
pip install numpy scipy librosa soundfile
pip install piper-tts  # For synthetic sample generation

# Create sample directories
mkdir -p samples/{positive,negative}
mkdir -p trained_model

echo ""
echo "✅ SETUP COMPLETE!"
echo ""
echo "Next steps:"
echo "1. Activate the environment: source venv/bin/activate"
echo "2. Generate synthetic samples: python generate_samples.py"
echo "3. Record real samples with your iPhone"
echo "4. Train the model: python train_model.py"
echo ""
echo "💪 LET'S DO THIS!"
