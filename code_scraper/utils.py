# code_scraper/utils.py

import os
from pathlib import Path
import datetime

def get_all_files(base_path, extensions):
    """
    Returns all files inside base_path that match given extensions.
    """
    files = []
    for root, _, filenames in os.walk(base_path):
        for f in filenames:
            if any(f.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, f))
    return files

def read_file_lines(filepath):
    """Reads a file and returns its lines as a list"""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().splitlines()

def format_timestamp(ts):
    """Converts timestamp to ISO 8601"""
    return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")
