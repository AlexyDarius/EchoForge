#!/bin/bash

# EchoForge Repo Manager Setup Script

echo "🚀 Setting up EchoForge Repo Manager..."
echo "========================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"

# Test the application
echo "🧪 Testing application..."
python test_app.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "To run the application:"
    echo "1. Activate virtual environment: source venv/bin/activate"
    echo "2. Run the app: python run.py"
    echo ""
    echo "Or use the quick start command:"
    echo "source venv/bin/activate && python run.py"
else
    echo "⚠️  Setup completed with warnings. Check the output above."
fi 