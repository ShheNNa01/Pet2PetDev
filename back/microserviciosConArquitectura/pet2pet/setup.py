# setup.py
from setuptools import setup, find_packages

setup(
    name="pet2pet",
    version="1.0.0",
    packages=find_packages(include=['services*', 'shared*']),
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "sqlalchemy>=2.0.23",
        "psycopg2-binary>=2.9.9",
        "pydantic>=2.4.2",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.6",
        "python-dotenv>=1.0.0",
    ],
)