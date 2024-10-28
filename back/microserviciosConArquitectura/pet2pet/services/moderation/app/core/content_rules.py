# services/moderation/app/core/content_rules.py
from typing import Dict, List, Set

class ContentRules:
    # Niveles de sensibilidad para diferentes tipos de contenido
    SENSITIVITY_LEVELS = {
        1: "Muy permisivo",
        2: "Permisivo",
        3: "Moderado",
        4: "Estricto",
        5: "Muy estricto"
    }

    # Palabras prohibidas por nivel de sensibilidad
    PROHIBITED_WORDS: Dict[int, Set[str]] = {
        1: set(),  # Solo contenido extremo
        2: set(),  # Contenido muy ofensivo
        3: set(),  # Contenido moderadamente ofensivo
        4: set(),  # Contenido levemente ofensivo
        5: set()   # Cualquier contenido cuestionable
    }

    # Reglas para imágenes
    IMAGE_RULES = {
        "max_size_mb": 10,
        "allowed_formats": ["jpg", "jpeg", "png", "gif"],
        "min_dimension": 200,
        "max_dimension": 4096,
        "prohibited_content": [
            "violencia_explicita",
            "contenido_adulto",
            "crueldad_animal",
            "simbolos_de_odio"
        ]
    }

    # Límites de contenido por tipo
    CONTENT_LIMITS = {
        "post": {
            "max_length": 5000,
            "max_images": 10,
            "max_tags": 20,
            "rate_limit_minutes": 5
        },
        "comment": {
            "max_length": 1000,
            "max_images": 2,
            "rate_limit_minutes": 1
        },
        "message": {
            "max_length": 2000,
            "max_images": 5,
            "rate_limit_minutes": 1
        }
    }

    # Reglas de spam
    SPAM_RULES = {
        "max_identical_posts": 3,
        "max_mentions_per_post": 10,
        "max_hashtags_per_post": 20,
        "max_links_per_post": 5,
        "min_time_between_posts_seconds": 30,
        "url_blacklist": set(),
        "domain_whitelist": set()
    }

    # Sistema de puntos de penalización
    PENALTY_POINTS = {
        "inappropriate_content": 2,
        "spam": 1,
        "harassment": 3,
        "hate_speech": 4,
        "violence": 4,
        "fake_account": 5,
        "intellectual_property": 3,
        "animal_abuse": 5
    }

    # Umbrales de acción basados en puntos
    ACTION_THRESHOLDS = {
        "warning": 3,
        "temporary_ban": 6,
        "permanent_ban": 10
    }

    # Duración de penalizaciones (en días)
    PENALTY_DURATIONS = {
        "temporary_ban_first": 1,
        "temporary_ban_second": 7,
        "temporary_ban_third": 30
    }

    @staticmethod
    def get_content_sensitivity(content: str, sensitivity_level: int) -> Dict[str, float]:
        """
        Evalúa la sensibilidad del contenido y devuelve puntuaciones por categoría
        """
        # Implementar lógica de evaluación de contenido
        return {
            "profanity": 0.0,
            "spam": 0.0,
            "toxicity": 0.0,
            "threat": 0.0,
            "harassment": 0.0
        }

    @staticmethod
    def check_rate_limit(user_id: int, content_type: str) -> bool:
        """
        Verifica si el usuario ha excedido los límites de publicación
        """
        # Implementar lógica de rate limiting
        return True

    @staticmethod
    def calculate_trust_score(
        total_posts: int,
        reports_received: int,
        reports_confirmed: int,
        account_age_days: int
    ) -> float:
        """
        Calcula el puntaje de confianza del usuario
        """
        base_score = 100.0
        
        # Factores positivos
        base_score += min(total_posts * 0.1, 20)  # Máximo +20 por posts
        base_score += min(account_age_days * 0.05, 30)  # Máximo +30 por antigüedad
        
        # Factores negativos
        base_score -= reports_confirmed * 5  # -5 por cada reporte confirmado
        base_score -= (reports_received - reports_confirmed) * 1  # -1 por reportes no confirmados
        
        return max(0.0, min(100.0, base_score))

    @staticmethod
    def should_auto_moderate(
        content_type: str,
        sensitivity_scores: Dict[str, float],
        user_trust_score: float
    ) -> bool:
        """
        Determina si el contenido debe ser moderado automáticamente
        """
        if user_trust_score < 30:
            return True
            
        for category, score in sensitivity_scores.items():
            if score > 0.8:  # 80% de confianza en la detección
                return True
                
        return False