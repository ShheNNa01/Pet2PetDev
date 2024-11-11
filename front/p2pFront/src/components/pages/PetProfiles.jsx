import React, { useState, useEffect } from 'react';
import { Avatar, AvatarImage, AvatarFallback } from '../ui/avatar';
import { Button } from '../ui/button';
import { PlusCircle, Pencil } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { petService } from '../services/petService';
import { useAuth } from '../context/AuthContext';
import { usePet } from '../context/PetContext';

export default function PetProfiles() {
    const [isEditing, setIsEditing] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [pets, setPets] = useState([]);
    const navigate = useNavigate();
    const { user } = useAuth();
    const { setCurrentPet } = usePet();

    useEffect(() => {
        const loadPets = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await petService.getMyPets();
            const petsData = Array.isArray(response) ? response : response.data || [];
            setPets(petsData);
        } catch (err) {
            console.error('Error loading pets:', err);
            setError('Error al cargar las mascotas');
        } finally {
            setLoading(false);
        }
        };

        if (user) {
        loadPets();
        }
    }, [user]);

    const handlePetSelect = (pet) => {
        if (!isEditing) {
        setCurrentPet(pet);
        navigate('/');
        }
    };

    const handleEditPet = (petId) => {
        if (isEditing) {
        navigate(`/edit-pet/${petId}`);
        }
    };

    if (loading) {
        return (
        <div className="min-h-screen bg-[#1a1a1a] flex items-center justify-center">
            <p className="text-[#eeede8] text-lg">Cargando...</p>
        </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#1a1a1a] flex flex-col">
        <div className="flex justify-end p-8">
            <Button
            variant="ghost"
            className="text-[#eeede8] hover:text-[#d55b49] transition-colors"
            onClick={() => setIsEditing(!isEditing)}
            >
            <Pencil className="h-5 w-5 mr-2" />
            {isEditing ? 'Listo' : 'Administrar Perfiles'}
            </Button>
        </div>
        
        <main className="flex-grow flex items-center justify-center px-4">
            <div className="max-w-4xl w-full">
            <h1 className="text-3xl md:text-4xl font-bold text-[#eeede8] text-center mb-8">
                ¿Quién quiere pasear hoy?
            </h1>

            {error && (
                <p className="text-[#d55b49] text-center mb-8">{error}</p>
            )}

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 justify-items-center">
                {pets.map((pet) => (
                <div
                    key={pet.pet_id}
                    className="group relative"
                    onClick={() => handlePetSelect(pet)}
                >
                    <div className="flex flex-col items-center space-y-4 cursor-pointer">
                    <div className="relative">
                        <Avatar className="w-[96px] h-[96px] border-2 border-transparent group-hover:border-[#509ca2] transition-all duration-300">
                        <AvatarImage 
                            src={pet.pet_picture || '/placeholder-pet.png'} 
                            alt={pet.name} 
                        />
                        <AvatarFallback className="bg-[#509ca2] text-[#eeede8]">
                            {pet.name[0]}
                        </AvatarFallback>
                        </Avatar>
                        {isEditing && (
                        <div 
                            className="absolute inset-0 bg-black/60 rounded-full flex items-center justify-center"
                            onClick={(e) => {
                            e.stopPropagation();
                            handleEditPet(pet.pet_id);
                            }}
                        >
                            <Pencil className="h-8 w-8 text-[#eeede8]" />
                        </div>
                        )}
                    </div>
                    <span className="text-[#eeede8] text-lg group-hover:text-[#509ca2] transition-colors">
                        {pet.name}
                    </span>
                    <span className="text-[#eeede8]/60 text-sm">
                        {pet.breed_name || 'Mascota'}
                    </span>
                    </div>
                </div>
                ))}

                <div
                onClick={() => navigate('/register-pet')}
                className="flex flex-col items-center space-y-4 cursor-pointer group"
                >
                <div className="w-[96px] h-[96px] rounded-full border-2 border-[#509ca2] border-dashed flex items-center justify-center group-hover:border-[#d55b49] transition-colors">
                    <PlusCircle className="h-12 w-12 text-[#509ca2] group-hover:text-[#d55b49] transition-colors" />
                </div>
                <span className="text-[#eeede8] text-lg group-hover:text-[#509ca2] transition-colors">
                    Agregar Mascota
                </span>
                </div>
            </div>
            </div>
        </main>

        <footer className="text-center py-8">
            <p className="text-[#eeede8]/60 text-sm">
            Selecciona un perfil para ver la información de tu mascota
            </p>
        </footer>
        </div>
    );
}