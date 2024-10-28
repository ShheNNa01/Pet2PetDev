from typing import List, Dict, Any, Optional
import re
import json
import logging
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from ..models.schemas import (
    ContentFilter,
    FilterResult,
    ContentType,
    ModerationStatus
)

logger = logging.getLogger(__name__)

class ContentFilterService:
    def __init__(self):
        # Cargar diccionarios de palabras prohibidas y patrones
        self.load_filter_dictionaries()

    def load_filter_dictionaries(self):
        """Cargar diccionarios de filtrado desde archivos"""
        try:
            # En una implementación real, estos vendrían de una base de datos o archivo
            self.profanity_dict = {
                "es": set(["palabra1", "palabra2"]),
                "en": set(["word1", "word2"])
            }
            self.hate_speech_patterns = {
                "es": [r"patron1", r"patron2"],
                "en": [r"pattern1", r"pattern2"]
            }
            self.adult_content_patterns = {
                "es": [r"patron_adulto1", r"patron_adulto2"],
                "en": [r"adult_pattern1", r"adult_pattern2"]
            }
        except Exception as e:
            logger.error(f"Error loading filter dictionaries: {str(e)}")
            raise

    async def filter_content(
        self,
        content: str,
        content_type: ContentType,
        settings: ContentFilter
    ) -> FilterResult:
        """
        Filtrar contenido basado en la configuración proporcionada
        """
        try:
            matched_filters = []
            confidence_score = 0.0
            filtered_content = content
            recommendations = []

            # Verificar cada tipo de filtro habilitado
            for filter_type in settings.filter_types:
                if filter_type == "profanity":
                    profanity_result = self._check_profanity(
                        content,
                        settings.language,
                        settings.sensitivity_level
                    )
                    matched_filters.extend(profanity_result["matches"])
                    confidence_score = max(confidence_score, profanity_result["confidence"])
                    filtered_content = profanity_result["filtered_content"]
                    recommendations.extend(profanity_result["recommendations"])

                elif filter_type == "hate_speech":
                    hate_speech_result = self._check_hate_speech(
                        content,
                        settings.language,
                        settings.sensitivity_level
                    )
                    matched_filters.extend(hate_speech_result["matches"])
                    confidence_score = max(confidence_score, hate_speech_result["confidence"])
                    recommendations.extend(hate_speech_result["recommendations"])

                elif filter_type == "adult_content":
                    adult_content_result = self._check_adult_content(
                        content,
                        settings.language,
                        settings.sensitivity_level
                    )
                    matched_filters.extend(adult_content_result["matches"])
                    confidence_score = max(confidence_score, adult_content_result["confidence"])
                    recommendations.extend(adult_content_result["recommendations"])

            # Verificar palabras clave personalizadas
            if settings.custom_keywords:
                custom_result = self._check_custom_keywords(
                    content,
                    settings.custom_keywords,
                    settings.excluded_terms or []
                )
                matched_filters.extend(custom_result["matches"])
                confidence_score = max(confidence_score, custom_result["confidence"])
                recommendations.extend(custom_result["recommendations"])

            # Determinar si el contenido debe ser marcado
            is_flagged = confidence_score >= (0.5 + (settings.sensitivity_level - 1) * 0.2)

            return FilterResult(
                is_flagged=is_flagged,
                confidence_score=confidence_score,
                matched_filters=list(set(matched_filters)),  # Eliminar duplicados
                filtered_content=filtered_content if is_flagged else None,
                recommendations=list(set(recommendations))  # Eliminar duplicados
            )

        except Exception as e:
            logger.error(f"Error filtering content: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error filtering content: {str(e)}"
            )

    def _check_profanity(
        self,
        content: str,
        language: str,
        sensitivity_level: int
    ) -> Dict[str, Any]:
        """Verificar contenido por palabras prohibidas"""
        matches = []
        filtered_content = content.lower()
        confidence = 0.0
        recommendations = []

        # Obtener diccionario para el idioma
        profanity_words = self.profanity_dict.get(language, set())

        # Buscar coincidencias
        words = filtered_content.split()
        matched_words = set()

        for word in words:
            clean_word = re.sub(r'[^\w\s]', '', word.lower())
            if clean_word in profanity_words:
                matched_words.add(clean_word)
                filtered_content = filtered_content.replace(
                    word,
                    '*' * len(word)
                )

        if matched_words:
            matches.extend(matched_words)
            confidence = min(len(matched_words) / 5, 1.0)  # Máximo 1.0
            recommendations.append(
                "El contenido contiene lenguaje inapropiado que debe ser revisado"
            )

        return {
            "matches": matches,
            "confidence": confidence * sensitivity_level / 3,
            "filtered_content": filtered_content,
            "recommendations": recommendations
        }

    def _check_hate_speech(
        self,
        content: str,
        language: str,
        sensitivity_level: int
    ) -> Dict[str, Any]:
        """Verificar contenido por discurso de odio"""
        matches = []
        confidence = 0.0
        recommendations = []

        # Obtener patrones para el idioma
        patterns = self.hate_speech_patterns.get(language, [])

        # Buscar coincidencias
        for pattern in patterns:
            if re.search(pattern, content.lower()):
                matches.append(pattern)
                confidence = max(confidence, 0.8)  # Alta confianza para hate speech
                recommendations.append(
                    "Se detectó posible discurso de odio que requiere revisión"
                )

        return {
            "matches": matches,
            "confidence": confidence * sensitivity_level / 3,
            "recommendations": recommendations
        }

    def _check_adult_content(
        self,
        content: str,
        language: str,
        sensitivity_level: int
    ) -> Dict[str, Any]:
        """Verificar contenido para adultos"""
        matches = []
        confidence = 0.0
        recommendations = []

        # Obtener patrones para el idioma
        patterns = self.adult_content_patterns.get(language, [])

        # Buscar coincidencias
        for pattern in patterns:
            if re.search(pattern, content.lower()):
                matches.append(pattern)
                confidence = max(confidence, 0.7)  # Confianza moderada-alta
                recommendations.append(
                    "Se detectó posible contenido para adultos que requiere revisión"
                )

        return {
            "matches": matches,
            "confidence": confidence * sensitivity_level / 3,
            "recommendations": recommendations
        }

    def _check_custom_keywords(
        self,
        content: str,
        keywords: List[str],
        excluded_terms: List[str]
    ) -> Dict[str, Any]:
        """Verificar palabras clave personalizadas"""
        matches = []
        confidence = 0.0
        recommendations = []

        content_lower = content.lower()

        # Verificar exclusiones primero
        for term in excluded_terms:
            if term.lower() in content_lower:
                return {
                    "matches": [],
                    "confidence": 0.0,
                    "recommendations": []
                }

        # Buscar palabras clave
        for keyword in keywords:
            if keyword.lower() in content_lower:
                matches.append(keyword)
                confidence = max(confidence, 0.6)  # Confianza moderada para keywords personalizadas
                recommendations.append(
                    f"Se encontró la palabra clave personalizada '{keyword}' que requiere revisión"
                )

        return {
            "matches": matches,
            "confidence": confidence,
            "recommendations": recommendations
        }