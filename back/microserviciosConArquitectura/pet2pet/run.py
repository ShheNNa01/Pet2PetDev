from pathlib import Path
import sys
import uvicorn
from shared.config.settings import settings

# Añadir el directorio raíz al PYTHONPATH
ROOT_PATH = Path(__file__).resolve().parent
sys.path.append(str(ROOT_PATH))

if __name__ == "__main__":
    uvicorn.run(
        "api_gateway.app:create_app",
        host="0.0.0.0",
        port=int(settings.AUTH_SERVICE_PORT),
        reload=True,
        factory=True,
        log_level="debug",
        reload_dirs=[str(ROOT_PATH)]
    )