#!/bin/bash
# Activar entorno
source venv/bin/activate

echo "Clonando y listando archivos frontend..."
python code_scraper_api/downloader.py

echo "Analizando archivos con AI y generando JSON..."
python code_scraper_api/analyzer.py

echo "Proceso completado. Los JSON se encuentran en la carpeta data/"
