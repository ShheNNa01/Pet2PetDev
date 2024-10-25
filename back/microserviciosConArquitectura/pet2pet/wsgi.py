from pathlib import Path
import sys

# Añadir el directorio raíz al PYTHONPATH
ROOT_PATH = Path(__file__).resolve().parent
sys.path.append(str(ROOT_PATH))

import uvicorn
from shared.config.settings import settings
from api_gateway.app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "wsgi:app",
        host="0.0.0.0",
        port=settings.AUTH_SERVICE_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )