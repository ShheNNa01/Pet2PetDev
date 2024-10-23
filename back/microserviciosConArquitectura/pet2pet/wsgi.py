# wsgi.py
from pathlib import Path
import sys

# Añadir el directorio raíz al PYTHONPATH
ROOT_PATH = Path(__file__).resolve().parent
sys.path.append(str(ROOT_PATH))

from services.auth.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("wsgi:app", host="0.0.0.0", port=8000, reload=True)