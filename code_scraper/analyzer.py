import os
import json
import shutil
import re
from pathlib import Path
from tqdm import tqdm
import ollama

import settings
from utils import read_file_lines


MODEL_NAME = "deepseek-coder:1.3b"


# ==========================================================
# ROBUST UTILITIES
# ==========================================================

def extract_json_from_text(text: str):
    """
    Extracts the first valid JSON block found inside a text.
    Tolerates ```json blocks and extra text before/after.
    """

    if not text:
        return None

    try:
        # Remove markdown blocks
        text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
        text = re.sub(r"```", "", text)

        # Search for first {...} block
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            candidate = match.group()
            return json.loads(candidate)

    except Exception:
        return None

    return None


# ==========================================================
# AI ANALYSIS
# ==========================================================

def detect_framework_and_dependencies(code_lines, file_name):
    """
    Detects framework and dependencies using Ollama.
    Never breaks the pipeline.
    """

    prompt_text = f"""
Analyze the following code and determine:

1. Framework used (React, Angular, Vue, None)
2. External libraries used

Respond ONLY with valid JSON using this structure:

{{
  "framework": "...",
  "dependencies": []
}}

Code:
{chr(10).join(code_lines)}
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format="json",
            messages=[{"role": "user", "content": prompt_text}]
        )

        content = response.get("message", {}).get("content", "").strip()

        # Direct parse attempt
        try:
            return json.loads(content)
        except Exception:
            pass

        # Robust extraction attempt
        parsed = extract_json_from_text(content)

        if parsed:
            return parsed

        raise ValueError("Could not extract valid JSON")

    except Exception as e:
        print(f"⚠ AI Error in {file_name}: {e}")
        return {
            "framework": None,
            "dependencies": []
        }


# ==========================================================
# MAIN PROCESSING
# ==========================================================

def process_files():
    """
    Processes files listed in data/files_list.json,
    analyzes them with AI, and saves JSON replicating structure.
    """

    files_list_path = Path("data/files_list.json")

    if not files_list_path.exists():
        print("❌ data/files_list.json does not exist")
        return

    with open(files_list_path, "r", encoding="utf-8") as f:
        files_meta = json.load(f)

    repos_root = Path(settings.REPOS_PATH)
    data_root = Path(settings.DATA_PATH)

    print(f"📁 Repos root: {repos_root}")
    print(f"📦 Data root: {data_root}")

    for fmeta in tqdm(files_meta, desc="Processing AI files"):

        file_path = Path(fmeta["file_path"])

        if not file_path.exists():
            continue

        try:
            relative_path = file_path.relative_to(repos_root)
        except ValueError:
            continue

        code_lines = read_file_lines(file_path)

        ai_result = detect_framework_and_dependencies(
            code_lines,
            fmeta["file_name"]
        )

        # Build destination path replicating original structure
        output_path = data_root / relative_path
        output_path = output_path.with_suffix(output_path.suffix + ".json")

        # Create necessary folders
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_json = {
            "file_name": fmeta["file_name"],
            "original_path": str(file_path),
            "extension": fmeta["extension"],
            "framework": ai_result.get("framework"),
            "dependencies": ai_result.get("dependencies"),
            "code": code_lines
        }

        try:
            with open(output_path, "w", encoding="utf-8") as jf:
                json.dump(
                    output_json,
                    jf,
                    indent=2,
                    ensure_ascii=False  # 🔥 critical for CSS and special characters
                )
        except Exception as e:
            print(f"❌ Error saving {output_path}: {e}")

    print("✔ JSON files generated respecting repository structure")


# ==========================================================
# ENTERPRISE CLEANUP
# ==========================================================

def cleanup_repos():
    """
    Completely deletes the repositories folder
    after processing.
    """

    repos_path = Path(settings.REPOS_PATH)

    if repos_path.exists() and repos_path.is_dir():
        print(f"🧹 Deleting repositories in {repos_path}...")
        try:
            shutil.rmtree(repos_path)
            print("✔ Repositories deleted successfully")
        except Exception as e:
            print(f"❌ Error deleting repositories: {e}")
    else:
        print("No repositories to delete")


# ==========================================================
# ENTRYPOINT
# ==========================================================

if __name__ == "__main__":
    print("🚀 Starting enterprise analysis...")
    process_files()
    cleanup_repos()
    print("✅ Pipeline completed successfully")
