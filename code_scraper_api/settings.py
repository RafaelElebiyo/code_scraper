# code_scraper_api/settings.py

REPO_URL = "https://github.com/RafaelElebiyo/Xamen_Generator"
LOCAL_REPO_PATH = "repos/Xamen_Generator"  # Carpeta donde se clona el repo
REPOS_PATH = "repos"
DATA_PATH = "data"

# Extensiones frontend a procesar
FRONTEND_EXTENSIONS = [".ts", ".tsx", ".js", ".jsx", ".html", ".css", ".xml"]

# Configuración AI
AI_MODEL = "deepseek-coder:1.3b"
AI_BATCH_SIZE = 3  # Archivos por batch para eficiencia CPU
