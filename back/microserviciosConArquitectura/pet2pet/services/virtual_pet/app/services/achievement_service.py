# services/virtual_pet/app/services/achievement_service.py
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from shared.database.models import VirtualPet, VirtualPetAchievement, VirtualPetActivity
from ..models.schemas import GameRewards, AchievementCreate

class AchievementService:
    @staticmethod
    async def check_social_achievements(
        db: Session,
        virtual_pet: VirtualPet
    ) -> List[VirtualPetAchievement]:
        """Verifica y otorga logros sociales basados en las interacciones"""
        new_achievements = []
        
        # Obtener todas las actividades de interacción social
        social_activities = db.query(VirtualPetActivity).filter(
            VirtualPetActivity.virtual_pet_id == virtual_pet.virtual_pet_id,
            VirtualPetActivity.activity_type.in_(['pet_interaction', 'group_participation'])
        ).all()
        
        # Verificar Social Butterfly
        interaction_count = len([a for a in social_activities if a.activity_type == 'pet_interaction'])
        if interaction_count >= GameRewards.SOCIAL_BUTTERFLY["requirement"]:
            achievement = await AchievementService.create_achievement(
                db,
                virtual_pet.virtual_pet_id,
                "social_butterfly",
                GameRewards.SOCIAL_BUTTERFLY["name"],
                GameRewards.SOCIAL_BUTTERFLY
            )
            if achievement:
                new_achievements.append(achievement)
        
        # Verificar Community Leader
        group_participations = len([a for a in social_activities if a.activity_type == 'group_participation'])
        if group_participations >= GameRewards.COMMUNITY_LEADER["requirement"]:
            achievement = await AchievementService.create_achievement(
                db,
                virtual_pet.virtual_pet_id,
                "community_leader",
                GameRewards.COMMUNITY_LEADER["name"],
                GameRewards.COMMUNITY_LEADER
            )
            if achievement:
                new_achievements.append(achievement)
        
        return new_achievements

    @staticmethod
    async def check_content_achievements(
        db: Session,
        virtual_pet: VirtualPet
    ) -> List[VirtualPetAchievement]:
        """Verifica y otorga logros basados en la creación de contenido"""
        new_achievements = []
        
        # Contar posts
        post_count = db.query(VirtualPetActivity).filter(
            VirtualPetActivity.virtual_pet_id == virtual_pet.virtual_pet_id,
            VirtualPetActivity.activity_type == 'post_creation'
        ).count()
        
        if post_count >= GameRewards.CONTENT_CREATOR["requirement"]:
            achievement = await AchievementService.create_achievement(
                db,
                virtual_pet.virtual_pet_id,
                "content_creator",
                GameRewards.CONTENT_CREATOR["name"],
                GameRewards.CONTENT_CREATOR
            )
            if achievement:
                new_achievements.append(achievement)
        
        return new_achievements

    @staticmethod
    async def check_loyalty_achievements(
        db: Session,
        virtual_pet: VirtualPet
    ) -> List[VirtualPetAchievement]:
        """Verifica y otorga logros basados en el tiempo de uso"""
        new_achievements = []
        
        days_since_creation = (datetime.now(timezone.utc) - virtual_pet.created_at).days
        
        if days_since_creation >= GameRewards.LOYAL_FRIEND["requirement"]:
            achievement = await AchievementService.create_achievement(
                db,
                virtual_pet.virtual_pet_id,
                "loyal_friend",
                GameRewards.LOYAL_FRIEND["name"],
                GameRewards.LOYAL_FRIEND
            )
            if achievement:
                new_achievements.append(achievement)
        
        return new_achievements

    @staticmethod
    async def create_achievement(
        db: Session,
        virtual_pet_id: int,
        achievement_type: str,
        description: str,
        rewards: Dict
    ) -> Optional[VirtualPetAchievement]:
        """Crea un nuevo logro si no existe ya"""
        # Verificar si el logro ya existe
        existing = db.query(VirtualPetAchievement).filter(
            VirtualPetAchievement.virtual_pet_id == virtual_pet_id,
            VirtualPetAchievement.achievement_type == achievement_type
        ).first()
        
        if existing:
            return None
            
        achievement = VirtualPetAchievement(
            virtual_pet_id=virtual_pet_id,
            achievement_type=achievement_type,
            description=description,
            rewards=rewards
        )
        
        db.add(achievement)
        db.commit()
        db.refresh(achievement)
        return achievement

    @staticmethod
    async def apply_achievement_rewards(
        db: Session,
        virtual_pet: VirtualPet,
        achievement: VirtualPetAchievement
    ) -> VirtualPet:
        """Aplica las recompensas del logro a la mascota virtual"""
        rewards = achievement.rewards
        
        if "reward_xp" in rewards:
            virtual_pet.experience_points += rewards["reward_xp"]
            
        if "reward_social_skill" in rewards:
            virtual_pet.attributes["social_skill"] = min(
                100.0,
                virtual_pet.attributes["social_skill"] + rewards["reward_social_skill"]
            )
            
        if "reward_happiness" in rewards:
            virtual_pet.happiness = min(100.0, virtual_pet.happiness + rewards["reward_happiness"])
            
        if "reward_food" in rewards:
            virtual_pet.attributes["food"] = min(
                100.0,
                virtual_pet.attributes["food"] + rewards["reward_food"]
            )
        
        db.commit()
        return virtual_pet

    @staticmethod
    async def check_all_achievements(
        db: Session,
        virtual_pet: VirtualPet
    ) -> List[VirtualPetAchievement]:
        """Verifica todos los tipos de logros posibles"""
        all_new_achievements = []
        
        # Verificar cada tipo de logro
        all_new_achievements.extend(await AchievementService.check_social_achievements(db, virtual_pet))
        all_new_achievements.extend(await AchievementService.check_content_achievements(db, virtual_pet))
        all_new_achievements.extend(await AchievementService.check_loyalty_achievements(db, virtual_pet))
        
        # Aplicar recompensas para cada nuevo logro
        for achievement in all_new_achievements:
            virtual_pet = await AchievementService.apply_achievement_rewards(db, virtual_pet, achievement)
            
        return all_new_achievements