import { useState, useEffect } from 'react';
import { usePet } from '../context/PetContext';
import { petService } from '../services/petService';

export const usePets = () => {
    const [myPets, setMyPets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { currentPet, setCurrentPet } = usePet();
    
    const loadMyPets = async () => {
        try {
            setLoading(true);
            setError(null);
            const token = localStorage.getItem('token');
            
            if (!token) {
                setError('No token found');
                return;
            }

            const response = await petService.getMyPets();
            const petsData = Array.isArray(response) ? response : response.data || [];
            
            setMyPets(petsData);

            if (!currentPet && petsData.length > 0) {
                setCurrentPet(petsData[0]);
            }
        } catch (error) {
            console.error('Error loading pets:', error);
            setError('Error al cargar las mascotas');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadMyPets();
    }, [currentPet, setCurrentPet]);

    const handlePetChange = (pet) => {
        setCurrentPet(pet);
    };

    // Retornamos tanto los estados como las funciones útiles
    return { 
        myPets, 
        loading, 
        error, 
        currentPet,
        handlePetChange,
        refreshPets: loadMyPets // Exponemos la función para recargar mascotas si es necesario
    };
};