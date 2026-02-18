# 🧠 Code Scraper AI

An enterprise-ready pipeline that **clones a repository, extracts frontend source files, analyzes them using a local AI model (Ollama), generates structured JSON files replicating the original folder structure, and removes the temporary repository automatically.**

The result is a clean, structured dataset of analyzed source code — ready for indexing, search, embeddings, or further AI processing.

---

# 🚀 Project Overview

Code Scraper AI performs the following pipeline:

1. Clone a target repository  
2. Detect and list frontend source files  
3. Analyze each file using a local AI model (Ollama)  
4. Generate structured JSON files  
5. Replicate the original folder structure  
6. Delete the cloned repository  
7. Keep only the processed JSON dataset  

The system is designed to be:

- Stable  
- CPU-compatible  
- Structure-preserving  
- Fault-tolerant  
- AI-response-safe  
- Enterprise-ready  

---

# 🏗 Project Architecture

```bash
code_scraper/
│
├── analyzer.py        # AI analysis + JSON generation + cleanup
├── settings.py        # Project configuration
├── utils.py           # Helper functions
├── run.sh             # Full pipeline runner
│
├── repos/             # Temporary cloned repositories
└── data/              # Final structured JSON output
```

After execution:

```bash
data/
└── <repository_name>/
    └── src/
        └── components/
            └── Button.jsx.json
```

The `repos/` folder is automatically deleted after processing.

---

# 🧩 Requirements

## System Requirements

- Python 3.10+
- Git
- Ollama installed locally
- Linux/macOS (Windows works with minor adjustments)

---

# 🤖 Install Ollama (Critical Step)

Install Ollama from:

https://ollama.com

After installing, pull the required model:

```bash
ollama pull deepseek-coder:1.3b
```

Verify it works:

```bash
ollama run deepseek-coder:1.3b
```

If this does not work, the project will not function.

---

# 🐍 Python Installation (Clean Setup — Avoid Past Issues)

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Upgrade pip:

```bash
pip install --upgrade pip
```

Install required packages:

```bash
pip install ollama==0.6.1
pip install tqdm
```

⚠️ Do NOT install:

- ollama-python  
- unofficial ollama clients  
- incompatible langchain versions  

The project uses the official `ollama` package only.

Verify installation:

```bash
python -c "import ollama; print(dir(ollama))"
```

You should see:

```
chat
generate
Client
...
```

---

# ⚙️ Configuration

Open `settings.py`.

You will see something like:

```python
REPOS_PATH = "repos"
DATA_PATH = "data"
TARGET_REPO = "https://github.com/your-user/your-repo.git"
```

To scrape a different repository, simply change:

```python
TARGET_REPO = "https://github.com/any-user/any-repo.git"
```

That’s it.

No other modification required.

---

# ▶️ Running the Project

Run:

```bash
./run.sh
```

Pipeline execution:

```text
Cloning repository...
Extracting frontend files...
Analyzing files with AI...
Generating structured JSON...
Deleting temporary repository...
Done.
```

---

# 📦 Output Structure

The output folder (`data/`) replicates the original repository structure.

Each source file becomes:

```
<Component>.tsx.json
```

Example JSON structure:

```json
{
  "file_name": "Button.tsx",
  "original_path": "repos/MyRepo/src/components/Button.tsx",
  "extension": ".tsx",
  "framework": "React",
  "dependencies": ["styled-components"],
  "code": []
}
```

This makes the dataset ideal for:

- Semantic search  
- Code indexing  
- Embedding generation  
- Framework analysis  
- Dependency mapping  
- AI fine-tuning datasets  

---

# 🛡 Enterprise Stability Features

This project includes:

- Robust JSON extraction from AI responses  
- Markdown-block tolerant parsing  
- CSS-safe handling (`{}` safe)  
- UTF-8 safe storage (`ensure_ascii=False`)  
- Folder structure replication  
- Automatic repository cleanup  
- Fault-tolerant AI calls (never breaks pipeline)  

---

# 🔄 Changing the Target Repository

To scrape another project:

1. Open `settings.py`
2. Replace:

```python
TARGET_REPO = "https://github.com/user/repo.git"
```

3. Run again:

```bash
./run.sh
```

The old `repos/` directory will be automatically recreated and removed after processing.

---

# 🧠 How It Works Internally

## 1. Repository Cloning

The repo is cloned into `repos/`.

## 2. File Listing

Frontend files (`.js`, `.jsx`, `.ts`, `.tsx`, `.css`, `.html`, etc.) are extracted.

## 3. AI Analysis

Each file is sent to Ollama:

```python
ollama.chat(
    model="deepseek-coder:1.3b",
    format="json",
    messages=[...]
)
```

The AI detects:

- Framework (React, Angular, Vue, None)  
- External dependencies  

## 4. JSON Generation

Each file becomes a structured JSON document.

## 5. Structure Replication

The output mirrors the original folder tree.

## 6. Cleanup

The `repos/` folder is deleted completely.

---

# 🔍 Why Local AI (Ollama)?

- No API keys required  
- No usage limits  
- No external costs  
- Fully offline  
- CPU compatible  
- Enterprise privacy safe  

---

# 📈 Future Expansion Ideas

This project is designed to scale into:

- Vector search indexing  
- Semantic code search API  
- Dependency graph generation  
- Automated documentation generation  
- Repository classification  
- AI-powered code intelligence systems  

---

# 🏁 Final Result

After execution, you have:

- A clean dataset  
- Structured code intelligence  
- Zero leftover temporary files  
- A reproducible AI scraping pipeline  

---

# 📜 License

Use freely for research, automation, indexing, or internal tooling.

---

# 👨‍💻 Project Description

Code Scraper AI is a structured code intelligence pipeline that transforms raw repositories into machine-readable AI-enriched datasets.

It bridges repository scraping and AI-powered code analysis into a deterministic, reproducible workflow suitable for research, indexing systems, or enterprise knowledge extraction.

---

If you want to extend this into:

- A REST API  
- A semantic search engine  
- A vector database pipeline  
- Or an enterprise code intelligence platform  

The architecture is ready.
