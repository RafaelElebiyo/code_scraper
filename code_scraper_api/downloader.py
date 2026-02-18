# code_scraper/downloader.py

import os
import git
from pathlib import Path
from utils import get_all_files, format_timestamp
import settings


def clone_or_update_repo():
    repo_path = Path(settings.LOCAL_REPO_PATH)
    if repo_path.exists():
        print(f"Updating existing repo at {repo_path}...")
        repo = git.Repo(repo_path)
        repo.remotes.origin.pull()
    else:
        print(f"Cloning repo {settings.REPO_URL} into {repo_path}...")
        repo = git.Repo.clone_from(settings.REPO_URL, repo_path)
    return repo_path


def list_frontend_files(repo_path):
    files = get_all_files(repo_path, settings.FRONTEND_EXTENSIONS)
    file_metadata = []

    for f in files:
        p = Path(f)
        stats = p.stat()
        metadata = {
            "file_path": str(p),
            "file_name": p.name,
            "extension": p.suffix,
            "created_at": format_timestamp(stats.st_ctime),
            "last_modified": format_timestamp(stats.st_mtime)
        }
        file_metadata.append(metadata)
    return file_metadata


if __name__ == "__main__":
    repo_path = clone_or_update_repo()
    files_meta = list_frontend_files(repo_path)
    print(f"Found {len(files_meta)} frontend files")

    # Save file list for analyzer.py
    import json

    os.makedirs("data", exist_ok=True)
    with open("data/files_list.json", "w", encoding="utf-8") as f:
        json.dump(files_meta, f, indent=2)
