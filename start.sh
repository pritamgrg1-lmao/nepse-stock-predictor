#!/bin/bash

echo "======================================"
echo "NEPSE Stock Predictor - Quick Start"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Generate sample data
echo ""
echo "Generating sample data files..."
python3 generate_sample_data.py

if [ $? -eq 0 ]; then
    echo "✓ Sample data generated"
else
    echo "⚠ Could not generate sample data (optional)"
fi

# Start the application
echo ""
echo "======================================"
echo "Starting NEPSE Stock Predictor..."
echo "======================================"
echo ""
echo "The application will be available at:"
echo "  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py