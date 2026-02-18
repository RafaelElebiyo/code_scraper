# code_scraper/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# Repo URL desde .env
REPO_URL = os.getenv("REPO_URL")

# ==========================================================
def get_repo_name(repo_url: str) -> str:
    """
    Extracts repository name from a GitHub URL
    """
    if not repo_url:
        raise ValueError("REPO_URL is not set in .env")

    repo_name = Path(urlparse(repo_url).path).stem
    return repo_name


REPO_NAME = get_repo_name(REPO_URL)

REPOS_PATH = "repos"
LOCAL_REPO_PATH = Path(REPOS_PATH) / REPO_NAME  # repos/Xamen_Generator
DATA_PATH = "data"

FILE_EXTENSIONS = [".ts", ".tsx", ".js", ".jsx", ".html", ".css", ".xml", ".java"]

AI_MODEL = "deepseek-coder:1.3b"
AI_BATCH_SIZE = 3
