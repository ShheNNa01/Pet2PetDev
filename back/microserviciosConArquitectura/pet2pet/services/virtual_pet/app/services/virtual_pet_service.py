# services/virtual_pet/app/services/virtual_pet_service.py
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import Dict, Optional, List
from shared.database.models import VirtualPet, VirtualPetActivity, VirtualPetAchievement
from ..models.schemas import (
    VirtualPetCreate, VirtualPetUpdate, ActivityCreate, 
    AchievementCreate, LevelConfig, GameRewards
)

class VirtualPetService:
    @staticmethod
    async def create_virtual_pet(db: Session, pet_data: VirtualPetCreate) -> VirtualPet:
        initial_attributes = {
            "food": 100.0,
            "health": 100.0,
            "happiness": 100.0,
            "social_skill": 100.0
        }
        
        db_virtual_pet = VirtualPet(
            pet_id=pet_data.pet_id,
            level=1,
            experience_points=0,
            happiness=100.0,
            energy=100.0,
            attributes=initial_attributes,
            status=True
        )
        
        db.add(db_virtual_pet)
        db.commit()
        db.refresh(db_virtual_pet)
        return db_virtual_pet

    @staticmethod
    async def get_virtual_pet(db: Session, pet_id: int) -> Optional[VirtualPet]:
        return db.query(VirtualPet).filter(VirtualPet.pet_id == pet_id).first()

    @staticmethod
    async def update_stats(db: Session, virtual_pet: VirtualPet) -> VirtualPet:
        """Actualiza las estadísticas basadas en el tiempo transcurrido"""
        now = datetime.now(timezone.utc)
        hours_passed = (now - virtual_pet.last_interaction).total_seconds() / 3600
        
        # Actualizar atributos
        attrs = virtual_pet.attributes
        attrs["food"] = max(0.0, attrs["food"] - (LevelConfig.FOOD_DECAY_RATE * hours_passed))
        virtual_pet.happiness = max(0.0, virtual_pet.happiness - (LevelConfig.HAPPINESS_DECAY_RATE * hours_passed))
        virtual_pet.energy = max(0.0, virtual_pet.energy - (LevelConfig.ENERGY_DECAY_RATE * hours_passed))
        
        virtual_pet.last_interaction = now
        db.commit()
        return virtual_pet

    @staticmethod
    async def add_experience(
        db: Session, 
        virtual_pet: VirtualPet, 
        points: int,
        activity_type: str,
        details: Dict
    ) -> VirtualPet:
        """Añade experiencia y maneja el aumento de nivel"""
        virtual_pet.experience_points += points
        
        # Registrar actividad
        activity = VirtualPetActivity(
            virtual_pet_id=virtual_pet.virtual_pet_id,
            activity_type=activity_type,
            points_earned=points,
            details=details
        )
        db.add(activity)
        
        # Verificar si sube de nivel
        next_level_xp = LevelConfig.get_xp_for_level(virtual_pet.level)
        while virtual_pet.experience_points >= next_level_xp and virtual_pet.level < LevelConfig.MAX_LEVEL:
            virtual_pet.level += 1
            # Bonus por subir de nivel
            virtual_pet.happiness = 100.0
            virtual_pet.energy = 100.0
            virtual_pet.attributes = {
                "food": 100.0,
                "health": 100.0,
                "happiness": 100.0,
                "social_skill": 100.0
            }
            next_level_xp = LevelConfig.get_xp_for_level(virtual_pet.level)
        
        db.commit()
        return virtual_pet

    @staticmethod
    async def process_activity(
        db: Session,
        virtual_pet: VirtualPet,
        activity_type: str,
        details: Dict
    ) -> VirtualPet:
        """Procesa una actividad y actualiza las estadísticas correspondientes"""
        points = 0
        attrs = virtual_pet.attributes
        
        if activity_type == "post_creation":
            points = LevelConfig.POINTS_POST_CREATION
            attrs["food"] = min(100.0, attrs["food"] + LevelConfig.FOOD_PER_POST)
            
        elif activity_type == "pet_interaction":
            points = LevelConfig.POINTS_PET_INTERACTION
            attrs["health"] = min(100.0, attrs["health"] + LevelConfig.HEALTH_PER_INTERACTION)
            
        elif activity_type == "daily_challenge":
            points = LevelConfig.POINTS_DAILY_CHALLENGE
            attrs["happiness"] = min(100.0, attrs["happiness"] + LevelConfig.HAPPINESS_PER_CHALLENGE)
            
        elif activity_type == "group_participation":
            points = LevelConfig.POINTS_GROUP_PARTICIPATION
            attrs["social_skill"] = min(100.0, attrs["social_skill"] + LevelConfig.SOCIAL_SKILL_PER_GROUP)
        
        virtual_pet.attributes = attrs
        return await VirtualPetService.add_experience(db, virtual_pet, points, activity_type, details)