import React from 'react';
import { useNavigate } from 'react-router-dom';
import { PawPrint } from 'lucide-react';
import { Button } from "../../ui/button";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "../../ui/dropdown-menu";
import { Avatar, AvatarImage, AvatarFallback } from "../../ui/avatar";
import { usePets } from '../../hooks/usePets';

export const PetSelector = () => {
    const navigate = useNavigate();
    const { 
        myPets, 
        loading, 
        error, 
        currentPet, 
        handlePetChange 
    } = usePets();

    if (error) {
        return (
            <Button 
                variant="ghost" 
                size="icon" 
                className="relative bg-white rounded-full shadow-sm hover:bg-gray-50"
                onClick={() => navigate('/login')}
            >
                <PawPrint className="h-5 w-5 text-red-500" />
            </Button>
        );
    }

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button 
                    variant="ghost" 
                    size="icon" 
                    className="relative bg-white rounded-full shadow-sm hover:bg-gray-50"
                    disabled={loading}
                >
                    <PawPrint className="h-5 w-5 text-[#509ca2]" />
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent 
                align="end" 
                className="w-56 p-2 bg-white rounded-lg shadow-lg"
            >
                <div className="px-2 py-1.5 text-sm font-medium text-gray-500">
                    Mis Mascotas
                </div>
                {myPets.map((pet) => (
                    <DropdownMenuItem 
                        key={`pet-${pet.pet_id}`}
                        onClick={() => handlePetChange(pet)}
                        className="cursor-pointer rounded-md my-1 p-2 hover:bg-gray-50"
                    >
                        <div className="flex items-center space-x-2">
                            <Avatar className="h-8 w-8">
                                <AvatarImage 
                                    src={pet.pet_picture || '/placeholder-pet.png'} 
                                    alt={pet.name} 
                                />
                                <AvatarFallback>
                                    {pet.name ? pet.name[0].toUpperCase() : 'P'}
                                </AvatarFallback>
                            </Avatar>
                            <div className="flex-1">
                                <p className={`text-sm font-medium ${
                                    currentPet?.pet_id === pet.pet_id 
                                    ? "text-[#d55b49]" 
                                    : "text-gray-700"
                                }`}>
                                    {pet.name}
                                </p>
                            </div>
                            {currentPet?.pet_id === pet.pet_id && (
                                <span className="h-2 w-2 bg-[#d55b49] rounded-full"/>
                            )}
                        </div>
                    </DropdownMenuItem>
                ))}
                <DropdownMenuItem 
                    onClick={() => navigate('/registerPet')}
                    className="cursor-pointer mt-2 pt-2 border-t border-gray-100"
                >
                    <div className="flex items-center space-x-2 text-[#509ca2]">
                        <PawPrint className="h-4 w-4" />
                        <span className="text-sm font-medium">Agregar mascota</span>
                    </div>
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    );
};