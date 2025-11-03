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

# Initialize community database tables
echo "Initializing community database tables..."
python init_community_db.py

echo "Build completed successfully!"

