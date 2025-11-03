#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements-render.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"

# Create necessary directories
mkdir -p logs
mkdir -p instance

# EMERGENCY FIX: Complete database setup
echo "🚀 EMERGENCY DATABASE FIX..."
python fix_database_now.py

echo "Build completed successfully!"

