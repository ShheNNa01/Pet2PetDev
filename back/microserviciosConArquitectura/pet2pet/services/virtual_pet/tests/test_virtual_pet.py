# services/virtual_pet/tests/test_virtual_pet.py
import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.services.virtual_pet_service import VirtualPetService
from app.services.game_service import GameService
from app.models.schemas import VirtualPetCreate, LevelConfig
from shared.database.models import VirtualPet, VirtualPetActivity, VirtualPetAchievement

@pytest.fixture
def virtual_pet_data():
    return VirtualPetCreate(
        pet_id=1,
        level=1,
        experience_points=0,
        happiness=100.0,
        energy=100.0,
        attributes={
            "food": 100.0,
            "health": 100.0,
            "happiness": 100.0,
            "social_skill": 100.0
        }
    )

@pytest.fixture
async def virtual_pet_service():
    return VirtualPetService()

@pytest.fixture
async def game_service():
    return GameService()

class TestVirtualPetService:
    async def test_create_virtual_pet(
        self,
        db: Session,
        virtual_pet_service: VirtualPetService,
        virtual_pet_data: VirtualPetCreate
    ):
        # Crear mascota virtual
        virtual_pet = await virtual_pet_service.create_virtual_pet(db, virtual_pet_data)
        
        assert virtual_pet is not None
        assert virtual_pet.pet_id == virtual_pet_data.pet_id
        assert virtual_pet.level == 1
        assert virtual_pet.experience_points == 0
        assert virtual_pet.happiness == 100.0
        assert virtual_pet.energy == 100.0
        assert virtual_pet.attributes["food"] == 100.0

    async def test_update_stats(
        self,
        db: Session,
        virtual_pet_service: VirtualPetService,
        virtual_pet_data: VirtualPetCreate
    ):
        # Crear mascota virtual
        virtual_pet = await virtual_pet_service.create_virtual_pet(db, virtual_pet_data)
        
        # Simular paso del tiempo
        virtual_pet.last_interaction = datetime.now() - timedelta(hours=2)
        
        # Actualizar stats
        updated_pet = await virtual_pet_service.update_stats(db, virtual_pet)
        
        assert updated_pet.attributes["food"] < 100.0
        assert updated_pet.happiness < 100.0
        assert updated_pet.energy < 100.0

    async def test_add_experience(
        self,
        db: Session,
        virtual_pet_service: VirtualPetService,
        virtual_pet_data: VirtualPetCreate
    ):
        # Crear mascota virtual
        virtual_pet = await virtual_pet_service.create_virtual_pet(db, virtual_pet_data)
        
        # Añadir experiencia
        points = LevelConfig.get_xp_for_level(1)  # Puntos necesarios para nivel 2
        updated_pet = await virtual_pet_service.add_experience(
            db,
            virtual_pet,
            points,
            "test_activity",
            {"test": "data"}
        )
        
        assert updated_pet.level == 2
        assert updated_pet.experience_points >= points
        assert updated_pet.happiness == 100.0  # Bonus por subir de nivel
        assert updated_pet.energy == 100.0     # Bonus por subir de nivel

class TestGameService:
    async def test_process_game_action(
        self,
        db: Session,
        game_service: GameService,
        virtual_pet_data: VirtualPetCreate
    ):
        # Crear mascota virtual primero
        virtual_pet_service = VirtualPetService()
        virtual_pet = await virtual_pet_service.create_virtual_pet(db, virtual_pet_data)
        
        # Procesar una acción de juego
        updated_pet, achievements = await game_service.process_game_action(
            db,
            virtual_pet.pet_id,
            "post_creation",
            {"content": "Test post"}
        )
        
        assert updated_pet is not None
        assert updated_pet.experience_points > 0
        assert updated_pet.attributes["food"] > virtual_pet.attributes["food"]

    async def test_daily_tasks(
        self,
        db: Session,
        game_service: GameService,
        virtual_pet_data: VirtualPetCreate
    ):
        # Crear mascota virtual
        virtual_pet_service = VirtualPetService()
        virtual_pet = await virtual_pet_service.create_virtual_pet(db, virtual_pet_data)
        
        # Obtener tareas diarias
        tasks = await game_service.get_daily_tasks(db, virtual_pet.pet_id)
        
        assert len(tasks) > 0
        assert all(isinstance(task, dict) for task in tasks)
        assert all("type" in task and "points" in task for task in tasks)

# Más pruebas pueden ser añadidas según sea necesario