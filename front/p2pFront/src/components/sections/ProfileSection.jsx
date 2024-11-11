import React from "react";
import { Card, CardContent } from "../ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Button } from "../ui/button";
import { useAuth } from '../context/AuthContext';
import { usePet } from '../context/PetContext';
import { useNavigate } from 'react-router-dom';

export default function ProfileSection() {
    const { user } = useAuth();
    const { currentPet } = usePet();
    const navigate = useNavigate();

    const handleEditClick = () => {
        if (currentPet) {
            navigate(`/pets/${currentPet.id}/edit`);
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
                                src={currentPet.image_url || "/placeholder-pet.svg"} 
                                alt={currentPet.name} 
                            />
                            <AvatarFallback>{currentPet.name[0]}</AvatarFallback>
                        </Avatar>
                        <div className="text-center">
                            <h3 className="text-xl font-semibold">{currentPet.name}</h3>
                            <p className="text-sm text-gray-500 mt-1">
                                {currentPet.breed?.name || 'Mascota adorable'}
                            </p>
                            <div className="mt-2 flex justify-center space-x-4">
                                <div className="text-center">
                                    <p className="font-semibold">Seguidores</p>
                                    <p className="text-sm text-gray-500">
                                        {currentPet.followers_count || 0}
                                    </p>
                                </div>
                                <div className="text-center">
                                    <p className="font-semibold">Siguiendo</p>
                                    <p className="text-sm text-gray-500">
                                        {currentPet.following_count || 0}
                                    </p>
                                </div>
                            </div>
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
                        <AvatarFallback>{user?.username?.[0]}</AvatarFallback>
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