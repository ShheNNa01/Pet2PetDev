import { useEffect, useState } from 'react';
import { petService } from '../services/petService';
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { UserPlus } from 'lucide-react';
import { usePet } from '../context/PetContext'; // Asegúrate de importar el contexto

export default function NewFriends({ userId }) {
    const [newFriends, setNewFriends] = useState([]);
    const [myPets, setMyPets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { currentPet } = usePet(); // Obtener la mascota actual del contexto

    useEffect(() => {
        const fetchData = async () => {
            if (!currentPet?.pet_id) return;
            
            setLoading(true);
            try {
                // Obtener mis mascotas
                const userPets = await petService.getMyPets({ skip: 0, limit: 100 });
                setMyPets(userPets);
                
                // Obtener las mascotas que ya sigue la mascota actual
                const following = await petService.getPetFollowing(currentPet.pet_id, {
                    skip: 0,
                    limit: 100
                });
                const followingIds = new Set(following.following.map(pet => pet.pet_id));
                
                // Obtener todas las mascotas potenciales
                const pets = await petService.getPets({ 
                    skip: 0, 
                    limit: 10, 
                    includeImage: true 
                });
                
                // Filtrar:
                // 1. Mascotas que no son mías
                // 2. Mascotas que no estoy siguiendo ya
                // 3. No incluir la mascota actual
                const filteredPets = pets.filter(pet => 
                    !followingIds.has(pet.pet_id) && // No está siguiendo
                    pet.pet_id !== currentPet.pet_id && // No es la mascota actual
                    !userPets.some(myPet => myPet.pet_id === pet.pet_id) // No es una de mis mascotas
                );
                
                setNewFriends(filteredPets);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [userId, currentPet?.pet_id]);

    const handleFollow = async (petToFollowId) => {
        if (!currentPet?.pet_id) {
            alert('Necesitas seleccionar una mascota para poder seguir a otros');
            return;
        }
    
        try {
            await petService.followPet(petToFollowId, currentPet.pet_id);
            
            // La actualización de contadores ahora se maneja a través del evento
            // Actualizar la lista de nuevos amigos
            setNewFriends(prev => prev.filter(friend => friend.pet_id !== petToFollowId));
            
            alert('Ahora sigues a esta mascota');
        } catch (error) {
            console.error('Error siguiendo mascota:', error);
            alert('No se pudo seguir a la mascota');
        }
    };

    if (loading) {
        return <div>Cargando...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (newFriends.length === 0) {
        return (
            <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
                <CardHeader>
                    <h2 className="text-[#d55b49] text-xl font-semibold">Nuevos Amigos</h2>
                </CardHeader>
                <CardContent>
                    <p className="text-center text-gray-500 py-4">
                        No hay nuevas mascotas para seguir en este momento
                    </p>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
            <CardHeader>
                <h2 className="text-[#d55b49] text-xl font-semibold">Nuevos Amigos</h2>
            </CardHeader>
            <CardContent>
                <div className="space-y-4">
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