# services/virtual_pet/app/services/game_service.py
from datetime import datetime, timezone
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Dict, Tuple, List
from shared.database.models import VirtualPet, VirtualPetActivity
from .virtual_pet_service import VirtualPetService
from .achievement_service import AchievementService
from ..models.schemas import LevelConfig, GameRewards

class GameService:
    def __init__(self):
        self.virtual_pet_service = VirtualPetService()
        self.achievement_service = AchievementService()

    async def process_game_action(
        self,
        db: Session,
        pet_id: int,
        action_type: str,
        details: Dict = None
    ) -> Tuple[VirtualPet, List]:
        """
        Procesa una acción del juego, actualiza las estadísticas y verifica logros
        """
        # Obtener o crear mascota virtual
        virtual_pet = await self.virtual_pet_service.get_virtual_pet(db, pet_id)
        if not virtual_pet:
            return None, []

        # Actualizar estadísticas basadas en tiempo transcurrido
        virtual_pet = await self.virtual_pet_service.update_stats(db, virtual_pet)

        # Procesar la acción específica
        virtual_pet = await self.virtual_pet_service.process_activity(
            db, virtual_pet, action_type, details or {}
        )

        # Verificar logros
        new_achievements = await self.achievement_service.check_all_achievements(db, virtual_pet)

        return virtual_pet, new_achievements

    @staticmethod
    async def get_daily_tasks(db: Session, pet_id: int) -> List[Dict]:
        """
        Obtiene las tareas diarias disponibles para la mascota
        """
        today = datetime.now(timezone.utc).date()
        
        # Verificar actividades ya completadas hoy
        completed_activities = db.query(VirtualPetActivity).filter(
            VirtualPetActivity.virtual_pet_id == pet_id,
            func.date(VirtualPetActivity.timestamp) == today
        ).all()
        
        completed_types = {activity.activity_type for activity in completed_activities}
        
        # Lista de todas las tareas posibles
        all_tasks = [
            {
                "type": "post_creation",
                "name": "Crear una publicación",
                "points": LevelConfig.POINTS_POST_CREATION,
                "reward": "Comida +20"
            },
            {
                "type": "pet_interaction",
                "name": "Interactuar con otra mascota",
                "points": LevelConfig.POINTS_PET_INTERACTION,
                "reward": "Salud +15"
            },
            {
                "type": "daily_challenge",
                "name": "Completar un desafío",
                "points": LevelConfig.POINTS_DAILY_CHALLENGE,
                "reward": "Felicidad +25"
            },
            {
                "type": "group_participation",
                "name": "Participar en un grupo",
                "points": LevelConfig.POINTS_GROUP_PARTICIPATION,
                "reward": "Destreza Social +10"
            }
        ]
        
        # Filtrar tareas no completadas
        available_tasks = [
            task for task in all_tasks
            if task["type"] not in completed_types
        ]
        
        return available_tasks

    @staticmethod
    async def get_game_stats(virtual_pet: VirtualPet) -> Dict:
        """
        Obtiene estadísticas detalladas del juego para la mascota virtual
        """
        next_level_xp = LevelConfig.get_xp_for_level(virtual_pet.level)
        
        return {
            "level": virtual_pet.level,
            "experience": {
                "current": virtual_pet.experience_points,
                "next_level": next_level_xp,
                "progress": (virtual_pet.experience_points / next_level_xp) * 100
            },
            "stats": {
                "happiness": virtual_pet.happiness,
                "energy": virtual_pet.energy,
                "attributes": virtual_pet.attributes
            },
            "time_since_last_interaction": (
                datetime.now(timezone.utc) - virtual_pet.last_interaction
            ).total_seconds() / 3600  # en horas
        }