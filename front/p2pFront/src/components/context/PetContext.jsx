import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { petService } from '../services/petService';
import { useAuth } from './AuthContext';
import { Outlet } from 'react-router-dom';

const PetContext = createContext(undefined);

export function PetProvider({ children }) {
    const { isAuthenticated } = useAuth();
    const [currentPet, setCurrentPet] = useState(() => {
        // Intentar recuperar la mascota actual del localStorage al iniciar
        const savedPet = localStorage.getItem('currentPet');
        return savedPet ? JSON.parse(savedPet) : null;
    });
    const [myPets, setMyPets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Memoizar la función de setCurrentPet para incluir persistencia
    const handleSetCurrentPet = useCallback((pet) => {
        setCurrentPet(pet);
        if (pet) {
            localStorage.setItem('currentPet', JSON.stringify(pet));
        } else {
            localStorage.removeItem('currentPet');
        }
    }, []);

    useEffect(() => {
        const fetchMyPets = async () => {
            if (!isAuthenticated) {
                console.log('No autenticado, saltando fetch de mascotas');
                setLoading(false);
                return;
            }
            try {
                console.log('Iniciando fetch de mascotas...');
                setLoading(true);
                setError(null);

                const token = localStorage.getItem('token');
                if (!token) {
                    throw new Error('No hay token disponible');
                }

                const response = await petService.getMyPets();
                console.log('Respuesta completa de getMyPets:', response);
                // Si response es directamente el array
                if (Array.isArray(response)) {
                    console.log('Response es un array:', response);
                    setMyPets(response);
                    // Solo establecer currentPet si no hay uno guardado
                    if (!currentPet && response.length > 0) {
                        handleSetCurrentPet(response[0]);
                    }
                }
                // Si response tiene una propiedad data
                else if (response?.data) {
                    console.log('Response tiene propiedad data:', response.data);
                    setMyPets(response.data);
                    // Solo establecer currentPet si no hay uno guardado
                    if (!currentPet && response.data.length > 0) {
                        handleSetCurrentPet(response.data[0]);
                    }
                } else {
                    console.log('Estructura de respuesta inesperada:', response);
                }
            } catch (err) {
                console.error('Error detallado al cargar mascotas:', err);
                setError('Error al cargar las mascotas');
                // Si el error es de autenticación, limpiar el pet actual
                if (err.response?.status === 401) {
                    handleSetCurrentPet(null);
                }
            } finally {
                setLoading(false);
            }
        };

        fetchMyPets();
    }, [isAuthenticated, currentPet, handleSetCurrentPet]);

    // Debug de estados
    useEffect(() => {
        console.log('Estado actualizado:', {
            myPets,
            currentPet,
            loading,
            error
        });
    }, [myPets, currentPet, loading, error]);

    // Función para recargar mascotas
    const refreshPets = useCallback(async () => {
        const fetchMyPets = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await petService.getMyPets();
                const petsData = Array.isArray(response) ? response : response.data || [];
                setMyPets(petsData);
                
                // Actualizar currentPet si existe en la nueva lista
                if (currentPet) {
                    const updatedCurrentPet = petsData.find(pet => pet.pet_id === currentPet.pet_id);
                    if (updatedCurrentPet) {
                        handleSetCurrentPet(updatedCurrentPet);
                    }
                }
            } catch (err) {
                console.error('Error al recargar mascotas:', err);
                setError('Error al recargar las mascotas');
            } finally {
                setLoading(false);
            }
        };

        if (isAuthenticated) {
            await fetchMyPets();
        }
    }, [isAuthenticated, currentPet, handleSetCurrentPet]);

    const value = {
        currentPet,
        setCurrentPet: handleSetCurrentPet,
        myPets,
        setMyPets,
        loading,
        error,
        refreshPets
    };

    return (
        <PetContext.Provider value={value}>
            <Outlet />
        </PetContext.Provider>
    );
}

export const usePet = () => {
    const context = useContext(PetContext);
    if (context === undefined) {
        throw new Error('usePet must be used within a PetProvider');
    }
    return context;
};