# services/virtual_pet/app/models/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class VirtualPetAttributes(BaseModel):
    food: float = Field(default=100.0, ge=0.0, le=100.0)
    health: float = Field(default=100.0, ge=0.0, le=100.0)
    happiness: float = Field(default=100.0, ge=0.0, le=100.0)
    social_skill: float = Field(default=100.0, ge=0.0, le=100.0)

class VirtualPetBase(BaseModel):
    level: int = Field(default=1, ge=1, le=100)
    experience_points: int = Field(default=0, ge=0)
    happiness: float = Field(default=100.0, ge=0.0, le=100.0)
    energy: float = Field(default=100.0, ge=0.0, le=100.0)
    attributes: VirtualPetAttributes

    class Config:
        json_schema_extra = {
            "example": {
                "level": 1,
                "experience_points": 0,
                "happiness": 100.0,
                "energy": 100.0,
                "attributes": {
                    "food": 100.0,
                    "health": 100.0,
                    "happiness": 100.0,
                    "social_skill": 100.0
                }
            }
        }

class VirtualPetCreate(VirtualPetBase):
    pet_id: int

class VirtualPetUpdate(BaseModel):
    experience_points: Optional[int] = None
    happiness: Optional[float] = None
    energy: Optional[float] = None
    attributes: Optional[Dict[str, float]] = None

class VirtualPetInDB(VirtualPetBase):
    virtual_pet_id: int
    pet_id: int
    last_interaction: datetime
    created_at: datetime
    updated_at: datetime
    status: bool

    class Config:
        from_attributes = True

class VirtualPetResponse(VirtualPetInDB):
    pass

# Activity Schemas
class ActivityBase(BaseModel):
    activity_type: str = Field(..., description="Type of activity: post, interaction, daily_challenge, group")
    points_earned: int = Field(..., ge=0)
    details: Dict[str, Any]

class ActivityCreate(ActivityBase):
    virtual_pet_id: int

class ActivityInDB(ActivityBase):
    activity_id: int
    virtual_pet_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class ActivityResponse(ActivityInDB):
    pass

# Achievement Schemas
class AchievementBase(BaseModel):
    achievement_type: str = Field(..., description="Type of achievement: social, usage_time, daily_tasks")
    description: str
    rewards: Dict[str, Any]

class AchievementCreate(AchievementBase):
    virtual_pet_id: int

class AchievementInDB(AchievementBase):
    achievement_id: int
    virtual_pet_id: int
    unlocked_at: datetime

    class Config:
        from_attributes = True

class AchievementResponse(AchievementInDB):
    pass

# Game Constants
class LevelConfig(BaseModel):
    MAX_LEVEL: int = 100
    BASE_XP_REQUIREMENT: int = 100
    XP_MULTIPLIER: float = 1.5
    
    # Puntos por actividad
    POINTS_POST_CREATION: int = 50
    POINTS_PET_INTERACTION: int = 30
    POINTS_DAILY_CHALLENGE: int = 100
    POINTS_GROUP_PARTICIPATION: int = 40
    
    # Beneficios por actividad
    FOOD_PER_POST: float = 20.0
    HEALTH_PER_INTERACTION: float = 15.0
    HAPPINESS_PER_CHALLENGE: float = 25.0
    SOCIAL_SKILL_PER_GROUP: float = 10.0
    
    # Decrementos por tiempo
    FOOD_DECAY_RATE: float = 5.0  # por hora
    HAPPINESS_DECAY_RATE: float = 3.0  # por hora
    ENERGY_DECAY_RATE: float = 4.0  # por hora
    
    @classmethod
    def get_xp_for_level(cls, level: int) -> int:
        """Calcula los puntos de experiencia necesarios para el siguiente nivel"""
        return int(cls.BASE_XP_REQUIREMENT * (cls.XP_MULTIPLIER ** (level - 1)))

class GameRewards(BaseModel):
    # Logros sociales
    SOCIAL_BUTTERFLY: Dict[str, Any] = {
        "name": "Mariposa Social",
        "requirement": 50,  # interacciones
        "reward_xp": 500,
        "reward_social_skill": 50.0
    }
    
    COMMUNITY_LEADER: Dict[str, Any] = {
        "name": "Líder Comunitario",
        "requirement": 10,  # grupos creados/unidos
        "reward_xp": 1000,
        "reward_social_skill": 100.0
    }
    
    # Logros de tiempo
    LOYAL_FRIEND: Dict[str, Any] = {
        "name": "Amigo Fiel",
        "requirement": 30,  # días
        "reward_xp": 1500,
        "reward_happiness": 100.0
    }
    
    # Logros de actividad
    CONTENT_CREATOR: Dict[str, Any] = {
        "name": "Creador de Contenido",
        "requirement": 100,  # posts
        "reward_xp": 2000,
        "reward_food": 100.0
    }