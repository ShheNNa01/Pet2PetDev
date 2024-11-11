import React, { createContext, useContext, useState, useEffect } from 'react';
import { petService } from '../services/petService';
import { useAuth } from './AuthContext';
import { Outlet } from 'react-router-dom';

const PetContext = createContext(undefined);

export function PetProvider({ children }) {
    const { isAuthenticated } = useAuth();
    const [currentPet, setCurrentPet] = useState(null);
    const [myPets, setMyPets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchMyPets = async () => {
            if (!isAuthenticated) {
                console.log('No autenticado, saltando fetch de mascotas');
                return;
            }
            
            try {
                console.log('Iniciando fetch de mascotas...');
                setLoading(true);
                const response = await petService.getMyPets();
                console.log('Respuesta completa de getMyPets:', response);
                
                // Si response es directamente el array
                if (Array.isArray(response)) {
                    console.log('Response es un array:', response);
                    setMyPets(response);
                    if (!currentPet && response.length > 0) {
                        setCurrentPet(response[0]);
                    }
                }
                // Si response tiene una propiedad data
                else if (response?.data) {
                    console.log('Response tiene propiedad data:', response.data);
                    setMyPets(response.data);
                    if (!currentPet && response.data.length > 0) {
                        setCurrentPet(response.data[0]);
                    }
                } else {
                    console.log('Estructura de respuesta inesperada:', response);
                }
            } catch (err) {
                console.error('Error detallado al cargar mascotas:', err);
                setError('Error al cargar las mascotas');
            } finally {
                setLoading(false);
            }
        };

        fetchMyPets();
    }, [isAuthenticated]);

    // Debug de estados
    useEffect(() => {
        console.log('Estado actualizado:', {
            myPets,
            currentPet,
            loading,
            error
        });
    }, [myPets, currentPet, loading, error]);

    const value = {
        currentPet,
        setCurrentPet,
        myPets,
        setMyPets,
        loading,
        error
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