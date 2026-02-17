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
# UTILIDADES ROBUSTAS
# ==========================================================

def extract_json_from_text(text: str):
    """
    Extrae el primer bloque JSON válido dentro de un texto.
    Tolera bloques ```json y texto extra antes/después.
    """

    if not text:
        return None

    try:
        # Eliminar bloques markdown
        text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
        text = re.sub(r"```", "", text)

        # Buscar primer bloque {...}
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
    Detecta framework y dependencias usando Ollama.
    Nunca rompe el pipeline.
    """

    prompt_text = f"""
Analiza el siguiente código y determina:

1. Framework usado (React, Angular, Vue, None)
2. Librerías externas utilizadas

Responde SOLO con JSON válido con esta estructura:

{{
  "framework": "...",
  "dependencies": []
}}

Código:
{chr(10).join(code_lines)}
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format="json",  # fuerza salida JSON
            messages=[{"role": "user", "content": prompt_text}]
        )

        content = response.get("message", {}).get("content", "").strip()

        # Intentar parse directo
        try:
            return json.loads(content)
        except Exception:
            pass

        # Intentar extracción robusta
        parsed = extract_json_from_text(content)

        if parsed:
            return parsed

        raise ValueError("No se pudo extraer JSON válido")

    except Exception as e:
        print(f"⚠ Error AI en {file_name}: {e}")
        return {
            "framework": None,
            "dependencies": []
        }


# ==========================================================
# PROCESAMIENTO PRINCIPAL
# ==========================================================

def process_files():
    """
    Procesa archivos listados en data/files_list.json,
    analiza con AI y guarda JSON replicando estructura.
    """

    files_list_path = Path("data/files_list.json")

    if not files_list_path.exists():
        print("❌ No existe data/files_list.json")
        return

    with open(files_list_path, "r", encoding="utf-8") as f:
        files_meta = json.load(f)

    repos_root = Path(settings.REPOS_PATH)
    data_root = Path(settings.DATA_PATH)

    print(f"📁 Repos root: {repos_root}")
    print(f"📦 Data root: {data_root}")

    for fmeta in tqdm(files_meta, desc="Procesando archivos AI"):

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

        # Construir ruta destino replicando estructura original
        output_path = data_root / relative_path
        output_path = output_path.with_suffix(output_path.suffix + ".json")

        # Crear carpetas necesarias
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
                    ensure_ascii=False  # 🔥 clave para CSS y caracteres especiales
                )
        except Exception as e:
            print(f"❌ Error guardando {output_path}: {e}")

    print("✔ JSON generados respetando estructura del repositorio")


# ==========================================================
# CLEANUP ENTERPRISE
# ==========================================================

def cleanup_repos():
    """
    Elimina completamente la carpeta de repositorios
    después del procesamiento.
    """

    repos_path = Path(settings.REPOS_PATH)

    if repos_path.exists() and repos_path.is_dir():
        print(f"🧹 Eliminando repositorios en {repos_path}...")
        try:
            shutil.rmtree(repos_path)
            print("✔ Repositorios eliminados correctamente")
        except Exception as e:
            print(f"❌ Error eliminando repos: {e}")
    else:
        print("No hay repositorios para eliminar")


# ==========================================================
# ENTRYPOINT
# ==========================================================

if __name__ == "__main__":
    print("🚀 Iniciando análisis enterprise...")
    process_files()
    cleanup_repos()
    print("✅ Pipeline completado correctamente")
