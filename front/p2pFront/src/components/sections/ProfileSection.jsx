import React, { useEffect, useState } from "react";
import { Card, CardContent } from "../ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Button } from "../ui/button";
import { useAuth } from '../context/AuthContext';
import { usePet } from '../context/PetContext';
import { useNavigate } from 'react-router-dom';
import { petService } from '../services/petService';

export default function ProfileSection() {
    const { user } = useAuth();
    const { currentPet } = usePet();
    const navigate = useNavigate();
    const [followCounts, setFollowCounts] = useState({
        followersCount: 0,
        followingCount: 0
    });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchFollowCounts = async () => {
            if (currentPet?.pet_id) {
                setLoading(true);
                try {
                    const counts = await petService.getFollowCounts(currentPet.pet_id);
                    setFollowCounts(counts);
                } catch (error) {
                    console.error('Error al obtener contadores:', error);
                } finally {
                    setLoading(false);
                }
            }
        };
    
        // Ejecutar inicialmente
        fetchFollowCounts();
    
        // Escuchar cambios en follows/unfollows
        const handleFollowChange = (event) => {
            const { petId, followerPetId } = event.detail;
            // Actualizar contadores si la mascota actual está involucrada
            if (currentPet?.pet_id === petId || currentPet?.pet_id === followerPetId) {
                fetchFollowCounts();
            }
        };
    
        window.addEventListener('petFollowStatusChanged', handleFollowChange);
    
        // Limpiar al desmontar
        return () => {
            window.removeEventListener('petFollowStatusChanged', handleFollowChange);
        };
    }, [currentPet?.pet_id]);

    const handleEditClick = () => {
        if (currentPet) {
            navigate(`/pets/${currentPet.pet_id}/edit`);
        } else {
            navigate('/profile/edit');
        }
    };

    // Si hay una mascota seleccionada, mostrar su perfil
    if (currentPet) {
        return (
            <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
                <CardContent className="pt-6">
                    <div className="flex flex-col items-center space-y-4">
                        <Avatar className="h-24 w-24 ring-2 ring-[#509ca2]/20">
                            <AvatarImage 
                                src={currentPet.pet_picture || "/placeholder-pet.svg"} 
                                alt={currentPet.name} 
                            />
                            <AvatarFallback>{currentPet.name[0]?.toUpperCase() || '?'}</AvatarFallback>
                        </Avatar>
                        <div className="text-center">
                            <h3 className="text-xl font-semibold">{currentPet.name}</h3>
                            <p className="text-sm text-gray-500 mt-1">
                                {currentPet.breed?.breed_name || 'Mascota adorable'}
                            </p>
                            <div className="mt-4 flex justify-center gap-8">
                                <button 
                                    onClick={() => navigate(`/pets/${currentPet.pet_id}/followers`)}
                                    className="text-center hover:bg-gray-50 px-4 py-2 rounded-lg transition-colors"
                                    disabled={loading}
                                >
                                    <p className="font-semibold text-lg">
                                        {loading ? '...' : followCounts.followersCount}
                                    </p>
                                    <p className="text-sm text-gray-500">Seguidores</p>
                                </button>
                                <button 
                                    onClick={() => navigate(`/pets/${currentPet.pet_id}/following`)}
                                    className="text-center hover:bg-gray-50 px-4 py-2 rounded-lg transition-colors"
                                    disabled={loading}
                                >
                                    <p className="font-semibold text-lg">
                                        {loading ? '...' : followCounts.followingCount}
                                    </p>
                                    <p className="text-sm text-gray-500">Siguiendo</p>
                                </button>
                            </div>
                            {currentPet.bio && (
                                <p className="mt-4 text-sm text-gray-600">
                                    {currentPet.bio}
                                </p>
                            )}
                        </div>
                        <Button 
                            onClick={handleEditClick}
                            className="w-full bg-[#509ca2] hover:bg-[#509ca2]/90"
                        >
                            Editar perfil
                        </Button>
                    </div>
                </CardContent>
            </Card>
        );
    }

    // Si no hay mascota seleccionada, mostrar perfil del usuario
    return (
        <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
            <CardContent className="pt-6">
                <div className="flex flex-col items-center space-y-4">
                    <Avatar className="h-24 w-24 ring-2 ring-[#509ca2]/20">
                        <AvatarImage 
                            src={user?.avatar_url || "/placeholder.svg"} 
                            alt={user?.username} 
                        />
                        <AvatarFallback>{user?.username?.[0]?.toUpperCase() || '?'}</AvatarFallback>
                    </Avatar>
                    <div className="text-center">
                        <h3 className="text-xl font-semibold">{user?.username}</h3>
                        <p className="text-sm text-gray-500 mt-1">
                            {user?.email}
                        </p>
                    </div>
                    <Button 
                        onClick={handleEditClick}
                        className="w-full bg-[#509ca2] hover:bg-[#509ca2]/90"
                    >
                        Editar perfil
                    </Button>
                    {!currentPet && (
                        <Button 
                            onClick={() => navigate('/pets/new')}
                            className="w-full bg-[#509ca2]/20 hover:bg-[#509ca2]/30"
                        >
                            Agregar mascota
                        </Button>
                    )}
                </div>
            </CardContent>
        </Card>
    );
}