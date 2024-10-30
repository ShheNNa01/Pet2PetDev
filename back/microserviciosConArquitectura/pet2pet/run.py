# run.py
from pathlib import Path
import sys
import uvicorn
import os
import argparse
from dotenv import load_dotenv

# Añadir el directorio raíz al PYTHONPATH
ROOT_PATH = Path(__file__).resolve().parent
sys.path.append(str(ROOT_PATH))

def load_environment_variables(environment: str):
    """Carga las variables de entorno según el ambiente especificado"""
    env_file = f".env.{environment}"
    
    if not os.path.exists(env_file):
        print(f"Error: No se encontró el archivo {env_file}")
        sys.exit(1)
    
    load_dotenv(env_file)
    print(f"Cargando configuración de: {env_file}")

def create_required_directories():
    """Crea los directorios necesarios si no existen"""
    directories = ['logs', 'uploads', 'exports']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Pet2Pet API Server')
    parser.add_argument(
        '--env',
        choices=['development', 'testing', 'production'],
        default='development',
        help='Ambiente de ejecución'
    )
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host de ejecución'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Puerto de ejecución'
    )
    
    args = parser.parse_args()
    
    # Cargar variables de entorno
    load_environment_variables(args.env)
    
    # Crear directorios necesarios
    create_required_directories()
    
    # Configuración de uvicorn
    config = {
        "app": "api_gateway.app:create_app",
        "host": args.host,
        "port": args.port,
        "reload": args.env != "production",
        "factory": True,
        "log_level": "debug" if args.env != "production" else "info",
        "workers": 1 if args.env != "production" else 4,
        "reload_dirs": [str(ROOT_PATH)] if args.env != "production" else None,
    }
    
    print(f"Iniciando servidor en modo: {args.env}")
    print(f"URL: http://{args.host}:{args.port}")
    
    uvicorn.run(**config)

if __name__ == "__main__":
    main()