from fastapi import HTTPException, UploadFile, status
from PIL import Image
import aiofiles
import os
import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from shared.database.models import MediaFile

class MediaService:
    UPLOAD_DIR = "media/posts"
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png"}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    @classmethod
    async def save_media(cls, file: UploadFile, post_id: int, db: Session) -> MediaFile:
        """
        Guarda un archivo de medios y crea un registro en la base de datos
        """
        try:
            # Validar el archivo
            await cls._validate_file(file)
            
            # Crear directorio si no existe
            os.makedirs(cls.UPLOAD_DIR, exist_ok=True)
            
            # Generar nombre único
            file_extension = os.path.splitext(file.filename)[1].lower()
            filename = f"{post_id}_{uuid.uuid4()}{file_extension}"
            filepath = os.path.join(cls.UPLOAD_DIR, filename)

            # Guardar archivo
            async with aiofiles.open(filepath, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)

            # Optimizar imagen
            await cls._optimize_image(filepath)

            # Crear registro en la base de datos
            media_file = MediaFile(
                post_id=post_id,
                media_url=filepath,
                media_type=file.content_type
            )
            
            db.add(media_file)
            db.commit()
            db.refresh(media_file)

            return media_file

        except Exception as e:
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error saving file: {str(e)}"
            )

    @classmethod
    async def _validate_file(cls, file: UploadFile):
        """
        Valida el archivo
        """
        # Validar extensión
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file extension"
            )

        # Validar tipo MIME
        if file.content_type not in cls.ALLOWED_MIMETYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type"
            )

        # Validar tamaño
        content = await file.read()
        await file.seek(0)
        
        if len(content) > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large"
            )

    @classmethod
    async def _optimize_image(cls, filepath: str):
        """
        Optimiza la imagen
        """
        try:
            with Image.open(filepath) as img:
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                max_size = (1200, 1200)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                img.save(filepath, 'JPEG', quality=85, optimize=True)
        
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error optimizing image: {str(e)}"
            )

    @classmethod
    async def delete_media(cls, media_path: str):
        """
        Elimina un archivo de medios
        """
        try:
            if os.path.exists(media_path):
                os.remove(media_path)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting media: {str(e)}"
            )