#!/bin/bash
# Activate virtual environment
source venv/bin/activate

echo "Cloning and listing frontend files..."
python code_scraper/downloader.py

echo "Analyzing files with AI and generating JSON..."
python code_scraper/analyzer.py

echo "Process completed. JSON files are available in the data/ folder"
