# code_scraper_api/utils.py

import os
from pathlib import Path
import datetime

def get_all_files(base_path, extensions):
    """
    Retorna todos los archivos dentro de base_path que tengan extensiones dadas.
    """
    files = []
    for root, _, filenames in os.walk(base_path):
        for f in filenames:
            if any(f.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, f))
    return files

def read_file_lines(filepath):
    """Lee un archivo y devuelve sus líneas como lista"""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().splitlines()

def format_timestamp(ts):
    """Convierte timestamp a ISO 8601"""
    return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")
