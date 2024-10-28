# services/virtual_pet/app/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

from services.virtual_pet.app.models.schemas import (
    VirtualPetCreate, VirtualPetResponse, VirtualPetUpdate,
    ActivityResponse, AchievementResponse
)
from services.virtual_pet.app.services.virtual_pet_service import VirtualPetService
from services.virtual_pet.app.services.game_service import GameService
from services.virtual_pet.app.api.dependencies import get_virtual_pet_service
from shared.database.session import get_db

router = APIRouter()

@router.post("/", response_model=VirtualPetResponse, status_code=status.HTTP_201_CREATED)
async def create_virtual_pet(
    virtual_pet_data: VirtualPetCreate,
    db: Session = Depends(get_db),
    virtual_pet_service: VirtualPetService = Depends(get_virtual_pet_service)
):
    """
    Crea una nueva mascota virtual para una mascota existente.
    """
    existing_pet = await virtual_pet_service.get_virtual_pet(db, virtual_pet_data.pet_id)
    if existing_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Virtual pet already exists for this pet"
        )
    
    return await virtual_pet_service.create_virtual_pet(db, virtual_pet_data)

@router.get("/{pet_id}", response_model=VirtualPetResponse)
async def get_virtual_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    virtual_pet_service: VirtualPetService = Depends(get_virtual_pet_service)
):
    """
    Obtiene los detalles de una mascota virtual por ID de mascota.
    """
    virtual_pet = await virtual_pet_service.get_virtual_pet(db, pet_id)
    if not virtual_pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Virtual pet not found"
        )
    
    # Actualizar estadísticas basadas en el tiempo transcurrido
    return await virtual_pet_service.update_stats(db, virtual_pet)

@router.post("/{pet_id}/actions/{action_type}", response_model=Dict)
async def perform_action(
    pet_id: int,
    action_type: str,
    details: Dict = None,
    db: Session = Depends(get_db)
):
    """
    Realiza una acción con la mascota virtual.
    Acciones disponibles: post_creation, pet_interaction, daily_challenge, group_participation
    """
    game_service = GameService()
    
    virtual_pet, new_achievements = await game_service.process_game_action(
        db, pet_id, action_type, details
    )
    
    if not virtual_pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Virtual pet not found"
        )
    
    # Obtener estadísticas actualizadas
    stats = await game_service.get_game_stats(virtual_pet)
    
    return {
        "status": "success",
        "action": action_type,
        "stats": stats,
        "new_achievements": [
            {
                "type": achievement.achievement_type,
                "description": achievement.description,
                "rewards": achievement.rewards
            }
            for achievement in new_achievements
        ]
    }

@router.get("/{pet_id}/daily-tasks", response_model=List[Dict])
async def get_daily_tasks(
    pet_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene las tareas diarias disponibles para la mascota virtual.
    """
    game_service = GameService()
    return await game_service.get_daily_tasks(db, pet_id)

@router.get("/{pet_id}/stats", response_model=Dict)
async def get_pet_stats(
    pet_id: int,
    db: Session = Depends(get_db),
    virtual_pet_service: VirtualPetService = Depends(get_virtual_pet_service)
):
    """
    Obtiene estadísticas detalladas de la mascota virtual.
    """
    virtual_pet = await virtual_pet_service.get_virtual_pet(db, pet_id)
    if not virtual_pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Virtual pet not found"
        )
    
    game_service = GameService()
    return await game_service.get_game_stats(virtual_pet)

@router.patch("/{pet_id}/feed", response_model=VirtualPetResponse)
async def feed_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    virtual_pet_service: VirtualPetService = Depends(get_virtual_pet_service)
):
    """
    Alimenta a la mascota virtual.
    """
    virtual_pet = await virtual_pet_service.get_virtual_pet(db, pet_id)
    if not virtual_pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Virtual pet not found"
        )
    
    # Actualizar atributos de comida
    attrs = virtual_pet.attributes
    attrs["food"] = min(100.0, attrs["food"] + 30.0)  # Aumenta la comida en 30 puntos
    virtual_pet.attributes = attrs
    
    details = {"food_increase": 30.0}
    return await virtual_pet_service.process_activity(
        db, virtual_pet, "feeding", details
    )

@router.patch("/{pet_id}/play", response_model=VirtualPetResponse)
async def play_with_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    virtual_pet_service: VirtualPetService = Depends(get_virtual_pet_service)
):
    """
    Juega con la mascota virtual.
    """
    virtual_pet = await virtual_pet_service.get_virtual_pet(db, pet_id)
    if not virtual_pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Virtual pet not found"
        )
    
    # Aumentar felicidad y reducir energía
    virtual_pet.happiness = min(100.0, virtual_pet.happiness + 20.0)
    virtual_pet.energy = max(0.0, virtual_pet.energy - 10.0)
    
    details = {
        "happiness_increase": 20.0,
        "energy_decrease": 10.0
    }
    return await virtual_pet_service.process_activity(
        db, virtual_pet, "playing", details
    )

@router.patch("/{pet_id}/rest", response_model=VirtualPetResponse)
async def rest_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    virtual_pet_service: VirtualPetService = Depends(get_virtual_pet_service)
):
    """
    Hace descansar a la mascota virtual para recuperar energía.
    """
    virtual_pet = await virtual_pet_service.get_virtual_pet(db, pet_id)
    if not virtual_pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Virtual pet not found"
        )
    
    # Recuperar energía
    virtual_pet.energy = min(100.0, virtual_pet.energy + 40.0)
    
    details = {"energy_increase": 40.0}
    return await virtual_pet_service.process_activity(
        db, virtual_pet, "resting", details
    )