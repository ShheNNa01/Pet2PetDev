from fastapi import HTTPException, UploadFile, status
from PIL import Image
import aiofiles
import os
import uuid
from datetime import datetime
from typing import Optional
import mimetypes

class FileService:
    UPLOAD_DIR = "uploads/pets"
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png"}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    @classmethod
    async def save_pet_image(cls, file: UploadFile, pet_id: int) -> str:
        """
        Guarda la imagen de la mascota y retorna la URL
        """
        try:
            # Validar el archivo
            await cls._validate_image(file)
            
            # Crear directorio si no existe
            os.makedirs(cls.UPLOAD_DIR, exist_ok=True)
            
            # Generar nombre único para el archivo
            file_extension = os.path.splitext(file.filename)[1].lower()
            filename = f"{pet_id}_{uuid.uuid4()}{file_extension}"
            filepath = os.path.join(cls.UPLOAD_DIR, filename)

            # Guardar el archivo
            async with aiofiles.open(filepath, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)

            # Optimizar imagen
            await cls._optimize_image(filepath)

            return filepath

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error saving file: {str(e)}"
            )

    @classmethod
    async def _validate_image(cls, file: UploadFile):
        """
        Valida que el archivo sea una imagen válida
        """
        # Validar extensión
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file extension. Allowed extensions: .jpg, .jpeg, .png"
            )

        # Validar tipo MIME
        mime_type, _ = mimetypes.guess_type(file.filename)
        if mime_type not in cls.ALLOWED_MIMETYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is not a valid image"
            )

        # Validar tamaño
        content = await file.read()
        await file.seek(0)  # Regresar al inicio del archivo
        
        if len(content) > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {cls.MAX_FILE_SIZE/1024/1024}MB"
            )

    @classmethod
    async def _optimize_image(cls, filepath: str):
        """
        Optimiza la imagen para reducir su tamaño
        """
        try:
            with Image.open(filepath) as img:
                # Convertir a RGB si es necesario
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionar si es muy grande
                max_size = (800, 800)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Guardar con optimización
                img.save(filepath, 'JPEG', quality=85, optimize=True)
        
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)  # Eliminar archivo si hay error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error optimizing image: {str(e)}"
            )

    @classmethod
    async def delete_pet_image(cls, image_path: str):
        """
        Elimina la imagen de una mascota
        """
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting image: {str(e)}"
            )