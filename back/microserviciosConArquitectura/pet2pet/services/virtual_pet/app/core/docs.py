# services/virtual_pet/app/core/docs.py
from typing import Dict

# Tags metadata para la documentación de la API
tags_metadata = [
    {
        "name": "virtual-pets",
        "description": "Operaciones con mascotas virtuales. Incluye creación, actualización y gestión de estadísticas.",
    },
    {
        "name": "actions",
        "description": "Acciones que pueden realizar las mascotas virtuales, como jugar, alimentarse y socializar.",
    },
    {
        "name": "achievements",
        "description": "Sistema de logros y recompensas para las mascotas virtuales.",
    }
]

# Ejemplos de respuestas para la documentación
example_responses = {
    "virtual_pet_response": {
        "description": "Ejemplo de respuesta de mascota virtual",
        "value": {
            "virtual_pet_id": 1,
            "pet_id": 1,
            "level": 5,
            "experience_points": 1250,
            "happiness": 85.5,
            "energy": 70.0,
            "attributes": {
                "food": 75.0,
                "health": 90.0,
                "happiness": 85.5,
                "social_skill": 65.0
            },
            "last_interaction": "2024-10-28T14:30:00Z",
            "created_at": "2024-10-20T10:00:00Z",
            "updated_at": "2024-10-28T14:30:00Z",
            "status": True
        }
    },
    "action_response": {
        "description": "Ejemplo de respuesta de acción",
        "value": {
            "status": "success",
            "action": "post_creation",
            "stats": {
                "level": 5,
                "experience": {
                    "current": 1250,
                    "next_level": 1500,
                    "progress": 83.33
                },
                "stats": {
                    "happiness": 85.5,
                    "energy": 70.0,
                    "attributes": {
                        "food": 75.0,
                        "health": 90.0,
                        "happiness": 85.5,
                        "social_skill": 65.0
                    }
                },
                "time_since_last_interaction": 2.5
            },
            "new_achievements": [
                {
                    "type": "content_creator",
                    "description": "¡Has creado 100 publicaciones!",
                    "rewards": {
                        "reward_xp": 2000,
                        "reward_food": 100.0
                    }
                }
            ]
        }
    },
    "daily_tasks_response": {
        "description": "Ejemplo de respuesta de tareas diarias",
        "value": [
            {
                "type": "post_creation",
                "name": "Crear una publicación",
                "points": 50,
                "reward": "Comida +20"
            },
            {
                "type": "pet_interaction",
                "name": "Interactuar con otra mascota",
                "points": 30,
                "reward": "Salud +15"
            }
        ]
    }
}

# Descripciones detalladas de los endpoints
endpoint_descriptions = {
    "create_virtual_pet": """
    Crea una nueva mascota virtual para una mascota existente.
    
    La mascota virtual iniciará con:
    * Nivel 1
    * 0 puntos de experiencia
    * 100% de felicidad y energía
    * Atributos al máximo (100%)
    
    Cada mascota real solo puede tener una mascota virtual asociada.
    """,
    
    "perform_action": """
    Realiza una acción con la mascota virtual que afectará sus estadísticas.
    
    Acciones disponibles:
    * post_creation: Crear una publicación (+50 XP, +20 Comida)
    * pet_interaction: Interactuar con otra mascota (+30 XP, +15 Salud)
    * daily_challenge: Completar un desafío (+100 XP, +25 Felicidad)
    * group_participation: Participar en un grupo (+40 XP, +10 Destreza Social)
    
    Las estadísticas tienen un máximo de 100% y un mínimo de 0%.
    Los puntos de experiencia acumulados determinarán cuando la mascota sube de nivel.
    """,
    
    "daily_tasks": """
    Obtiene la lista de tareas diarias disponibles para la mascota virtual.
    
    Características:
    * Las tareas se resetean diariamente
    * Cada tarea solo puede completarse una vez al día
    * Las tareas otorgan puntos de experiencia y beneficios específicos
    * La disponibilidad de tareas puede variar según el nivel de la mascota
    """,
    
    "get_stats": """
    Obtiene estadísticas detalladas de la mascota virtual.
    
    Incluye:
    * Nivel actual y progreso hacia el siguiente nivel
    * Puntos de experiencia actuales y necesarios para subir de nivel
    * Estado de todos los atributos (comida, salud, felicidad, destreza social)
    * Tiempo desde la última interacción
    * Estado de energía y felicidad
    """
}