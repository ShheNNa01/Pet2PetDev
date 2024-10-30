# dev.py
import subprocess
import sys
from pathlib import Path

def run_dev_server():
    """Ejecuta el servidor en modo desarrollo con configuración por defecto"""
    try:
        # Ejecutar migraciones
        print("Ejecutando migraciones...")
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        
        # Iniciar servidor
        print("Iniciando servidor de desarrollo...")
        subprocess.run(["python", "run.py", "--env", "development"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el servidor: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
        sys.exit(0)

if __name__ == "__main__":
    run_dev_server()