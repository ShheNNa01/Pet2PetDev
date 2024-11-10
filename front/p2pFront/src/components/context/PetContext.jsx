import React, { createContext, useContext, useState, useEffect } from 'react';
import { petService } from '../services/petService';

const PetContext = createContext();

export function PetProvider({ children }) {
    const [currentPet, setCurrentPet] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCurrentPet = async () => {
        try {
            const response = await petService.getMyPets({ limit: 1 });
            if (response.data && response.data.length > 0) {
            setCurrentPet(response.data[0]);
            }
            setLoading(false);
        } catch (err) {
            setError('Error al cargar la mascota');
            setLoading(false);
        }
        };

        fetchCurrentPet();
    }, []);

    return (
        <PetContext.Provider value={{ currentPet, loading, error, setCurrentPet }}>
        {children}
        </PetContext.Provider>
    );
}

export const usePet = () => useContext(PetContext);