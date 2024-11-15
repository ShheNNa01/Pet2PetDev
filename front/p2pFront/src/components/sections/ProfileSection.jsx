import React, { useEffect, useState } from "react";
import { Card, CardContent } from "../ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Button } from "../ui/button";
import { useAuth } from '../context/AuthContext';
import { usePet } from '../context/PetContext';
import { useNavigate } from 'react-router-dom';
import { petService } from '../services/petService';
import { Camera, Edit, UserPlus, PawPrint } from "lucide-react";

export default function ProfileSection() {
    const { user } = useAuth();
    const { currentPet } = usePet();
    const navigate = useNavigate();
    const [followCounts, setFollowCounts] = useState({
        followersCount: 0,
        followingCount: 0
    });
    const [loading, setLoading] = useState(false);
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        // Cargar datos del usuario desde localStorage
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            setUserData(JSON.parse(storedUser));
        }
    }, []);

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

        fetchFollowCounts();

        const handleFollowChange = (event) => {
            const { petId, followerPetId } = event.detail;
            if (currentPet?.pet_id === petId || currentPet?.pet_id === followerPetId) {
                fetchFollowCounts();
            }
        };

        window.addEventListener('petFollowStatusChanged', handleFollowChange);
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

    const handleProfileClick = () => {
        if (currentPet) {
            navigate(`/petProfile?id=${currentPet.pet_id}`);
        } else {
            navigate('/userProfile');
        }
    };

    // Si hay una mascota seleccionada, mostrar su perfil
    if (currentPet) {
        return (
            <Card className="bg-white shadow-lg rounded-xl overflow-hidden border border-gray-100">
                <CardContent className="p-6">
                    <div className="flex flex-col items-center space-y-6">
                        <div 
                            onClick={handleProfileClick}
                            className="relative cursor-pointer group"
                        >
                            <div className="rounded-full p-1 bg-gradient-to-r from-[#509ca2] to-[#45858b]">
                                <Avatar className="h-28 w-28 ring-4 ring-white">
                                    <AvatarImage 
                                        src={currentPet.pet_picture || "/placeholder-pet.svg"} 
                                        alt={currentPet.name}
                                        className="object-cover"
                                    />
                                    <AvatarFallback className="bg-[#509ca2]/10">
                                        <PawPrint className="h-12 w-12 text-[#509ca2]" />
                                    </AvatarFallback>
                                </Avatar>
                            </div>
                            <div className="absolute inset-0 flex items-center justify-center bg-black/0 group-hover:bg-black/20 rounded-full transition-all">
                                <Camera className="text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                            </div>
                        </div>
                        <div className="text-center space-y-3">
                            <div>
                                <h3 
                                    onClick={handleProfileClick}
                                    className="text-2xl font-bold cursor-pointer hover:text-[#509ca2] transition-colors"
                                >
                                    {currentPet.name}
                                </h3>
                                <p className="text-sm text-gray-500 mt-1">
                                    {currentPet.breed?.breed_name || 'Mascota adorable'} • {currentPet.gender === 'M' ? '♂️' : '♀️'}
                                </p>
                            </div>
                            
                            <div className="flex justify-center gap-12">
                                <button 
                                    onClick={() => navigate(`/pets/${currentPet.pet_id}/followers`)}
                                    className="text-center hover:bg-gray-50 px-6 py-3 rounded-xl transition-colors"
                                    disabled={loading}
                                >
                                    <p className="font-bold text-2xl text-[#509ca2]">
                                        {loading ? '...' : followCounts.followersCount}
                                    </p>
                                    <p className="text-sm font-medium text-gray-600">Seguidores</p>
                                </button>
                                <button 
                                    onClick={() => navigate(`/pets/${currentPet.pet_id}/following`)}
                                    className="text-center hover:bg-gray-50 px-6 py-3 rounded-xl transition-colors"
                                    disabled={loading}
                                >
                                    <p className="font-bold text-2xl text-[#509ca2]">
                                        {loading ? '...' : followCounts.followingCount}
                                    </p>
                                    <p className="text-sm font-medium text-gray-600">Siguiendo</p>
                                </button>
                            </div>
                            
                            {currentPet.bio && (
                                <p className="text-sm text-gray-600 px-4">
                                    {currentPet.bio}
                                </p>
                            )}
                        </div>
                        
                        <Button 
                            onClick={handleEditClick}
                            className="w-full bg-[#509ca2] hover:bg-[#509ca2]/90 text-white font-medium py-2.5 rounded-xl flex items-center justify-center gap-2"
                        >
                            <Edit className="h-4 w-4" />
                            Editar perfil
                        </Button>
                    </div>
                </CardContent>
            </Card>
        );
    }

    // Si no hay mascota seleccionada, mostrar perfil del usuario
    return (
        <Card className="bg-white shadow-lg rounded-xl overflow-hidden border border-gray-100">
            <CardContent className="p-6">
                <div className="flex flex-col items-center space-y-6">
                    <div 
                        onClick={handleProfileClick}
                        className="relative cursor-pointer group"
                    >
                        <div className="rounded-full p-1 bg-gradient-to-r from-[#509ca2] to-[#45858b]">
                            <Avatar className="h-28 w-28 ring-4 ring-white">
                                <AvatarImage 
                                    src={userData?.avatar_url || "/placeholder.svg"} 
                                    alt={userData?.username || user?.username}
                                    className="object-cover"
                                />
                                <AvatarFallback className="bg-[#509ca2]/10">
                                    {(userData?.username?.[0] || user?.username?.[0] || '?').toUpperCase()}
                                </AvatarFallback>
                            </Avatar>
                        </div>
                        <div className="absolute inset-0 flex items-center justify-center bg-black/0 group-hover:bg-black/20 rounded-full transition-all">
                            <Camera className="text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                        </div>
                    </div>
                    <div className="text-center space-y-4">
                        <div>
                            <h3 
                                onClick={handleProfileClick}
                                className="text-2xl font-bold cursor-pointer hover:text-[#509ca2] transition-colors"
                            >
                                {userData?.username || user?.username}
                            </h3>
                            <p className="text-sm text-gray-500 mt-1">
                                {userData?.email || user?.email}
                            </p>
                        </div>
                        
                        <div className="flex flex-col gap-3 w-full">
                            <Button 
                                onClick={handleEditClick}
                                className="w-full bg-[#509ca2] hover:bg-[#509ca2]/90 text-white font-medium py-2.5 rounded-xl flex items-center justify-center gap-2"
                            >
                                <Edit className="h-4 w-4" />
                                Editar perfil
                            </Button>
                            
                            {!currentPet && (
                                <Button 
                                    onClick={() => navigate('/registerPet')}
                                    className="w-full bg-[#509ca2]/10 hover:bg-[#509ca2]/20 text-[#509ca2] font-medium py-2.5 rounded-xl flex items-center justify-center gap-2"
                                >
                                    <UserPlus className="h-4 w-4" />
                                    Agregar mascota
                                </Button>
                            )}
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}