import { useEffect, useState } from 'react';
import { petService } from '../services/petService';
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { UserPlus } from 'lucide-react';

export default function NewFriends({ userId }) {
    const [newFriends, setNewFriends] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchNewFriends = async () => {
            try {
                const pets = await petService.getPets({ skip: 0, limit: 10, includeImage: true });
                const filteredPets = pets.filter(pet => pet.user_id !== userId);
                setNewFriends(filteredPets);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchNewFriends();
    }, [userId]);

    if (loading) {
        return <div>Cargando...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
            <CardHeader>
                <h2 className="text-[#d55b49] text-xl font-semibold">Nuevos Amigos</h2>
            </CardHeader>
            <CardContent>
                <div className="space-y-4"> {/* Contenedor para las tarjetas individuales */}
                    {newFriends.map((friend) => (
                        <Card key={friend.pet_id} className="bg-white shadow rounded-lg overflow-hidden">
                            <CardHeader className="flex items-center gap-3 p-4">
                                <Avatar className="h-12 w-12 bg-gray-200 border border-gray-300 rounded-full flex items-center justify-center overflow-hidden">
                                    <AvatarImage
                                        src={friend.pet_picture}
                                        className="h-full w-full object-cover"
                                        alt={friend.name}
                                    />
                                    <AvatarFallback className="bg-gray-200 text-gray-500">
                                        {friend.name ? friend.name[0] : "?"}
                                    </AvatarFallback>
                                </Avatar>
                                <h3 className="text-lg font-semibold">{friend.name}</h3>
                            </CardHeader>
                            <CardContent className="flex justify-end p-4">
                                <Button
                                    variant="outline"
                                    size="sm"
                                    className="h-7 px-3 border-[#509ca2] text-[#d55b49] hover:bg-[#509ca2] text-xs font-normal"
                                    onClick={() => handleFollow(friend.pet_id)}
                                >
                                    <UserPlus className="h-3.5 w-3.5 mr-1.5" />
                                    Seguir
                                </Button>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}

// Implementa la función handleFollow
const handleFollow = async (petId) => {
    try {
        await petService.followPet(petId, userId);
        alert('Ahora sigues a esta mascota');
    } catch (error) {
        console.error('Error siguiendo mascota:', error);
        alert('No se pudo seguir a la mascota');
    }
};
