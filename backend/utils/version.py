import json
import os
from pathlib import Path


def get_version():
    # Usando Path para manejar rutas de manera más segura
    current_dir = Path(__file__).parent
    version_path = current_dir.parent.parent / "version.json"
    try:
        with open(version_path, "r") as f:
            version_data = json.load(f)
        return version_data
    except FileNotFoundError:
        return {"api": "0.0.0", "frontend": "0.0.0"}
