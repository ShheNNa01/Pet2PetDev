import React, { useState, useEffect } from 'react';
import { Avatar, AvatarImage, AvatarFallback } from '../ui/avatar';
import { Button } from '../ui/button';
import { PlusCircle, Pencil, ArrowLeft } from 'lucide-react';
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
    const { currentPet, setCurrentPet } = usePet();

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
                if (err.response?.status === 401) {
                    navigate('/login');
                }
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            loadPets();
        }
    }, [user, navigate]);

    const handlePetSelect = (pet) => {
        if (!isEditing) {
            console.log('Cambiando a mascota:', pet);
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
            <div className="flex justify-between items-center p-8">
                {/* Botón Regresar */}
                <Button
                    variant="ghost"
                    className="text-[#eeede8] hover:text-[#d55b49] transition-colors"
                    onClick={() => navigate('/')}
                >
                    <ArrowLeft className="h-5 w-5 mr-2" />
                    Regresar
                </Button>

                {/* Botón Editar */}
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
                <div className="max-w-3xl w-full">
                    <h1 className="text-4xl font-bold text-[#eeede8] text-center mb-16">
                        ¿Quién quiere pasear hoy?
                    </h1>

                    {error && (
                        <p className="text-[#d55b49] text-center mb-8">{error}</p>
                    )}

                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 justify-items-center">
                        {pets.map((pet) => (
                            <div
                                key={pet.pet_id}
                                className="group relative w-32"
                                onClick={() => handlePetSelect(pet)}
                            >
                                <div className="flex flex-col items-center space-y-4 cursor-pointer">
                                    <div className="relative w-24 h-24">
                                        {pet.pet_picture ? (
                                            <Avatar className="w-24 h-24 border-2 border-transparent group-hover:border-[#509ca2] transition-all duration-300">
                                                <AvatarImage 
                                                    src={pet.pet_picture} 
                                                    alt={pet.name}
                                                    className="object-cover"
                                                />
                                                <AvatarFallback className="bg-[#509ca2] text-[#eeede8] text-3xl font-light">
                                                    {pet.name[0].toUpperCase()}
                                                </AvatarFallback>
                                            </Avatar>
                                        ) : (
                                            <div className="w-24 h-24 rounded-full bg-gray-800 border-2 border-transparent group-hover:border-[#509ca2] flex items-center justify-center transition-all duration-300">
                                                <span className="text-4xl text-[#eeede8] font-light">
                                                    {pet.name[0].toUpperCase()}
                                                </span>
                                            </div>
                                        )}
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
                                    <div className="flex flex-col items-center space-y-1">
                                        <span className="text-[#eeede8] text-lg font-medium group-hover:text-[#509ca2] transition-colors">
                                            {pet.name}
                                        </span>
                                        <span className="text-[#eeede8]/60 text-sm">
                                            {pet.breed_name ? pet.breed_name : pet.type_name || 'Mascota'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        ))}

                        <div
                            onClick={() => navigate('/registerPet')}
                            className="w-32 flex flex-col items-center space-y-4 cursor-pointer group"
                        >
                            <div className="w-24 h-24 rounded-full border-2 border-[#509ca2] border-dashed flex items-center justify-center group-hover:border-[#d55b49] transition-colors">
                                <PlusCircle className="h-12 w-12 text-[#509ca2] group-hover:text-[#d55b49] transition-colors" />
                            </div>
                            <span className="text-[#eeede8] text-lg text-center group-hover:text-[#509ca2] transition-colors">
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