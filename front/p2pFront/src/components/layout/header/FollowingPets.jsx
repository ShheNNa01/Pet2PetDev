import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { Input } from "../../ui/input";
import { Avatar, AvatarImage, AvatarFallback } from "../../ui/avatar";
import { petService } from '../../services/petService';
import { getMediaUrl } from '../../services/config/axios';

export const FollowingPets = ({ onSelectPet, currentPetId }) => {
  const [followingPets, setFollowingPets] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const loadFollowing = async () => {
      try {
        setIsLoading(true);
        const response = await petService.getPetFollowing(currentPetId);
        setFollowingPets(response.following || []);
      } catch (error) {
        console.error('Error cargando mascotas seguidas:', error);
      } finally {
        setIsLoading(false);
      }
    };

    if (currentPetId) {
      loadFollowing();
    }
  }, [currentPetId]);

  const filteredPets = followingPets.filter(pet => 
    pet.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-48">
        <div className="flex space-x-2">
          <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.3s]"></div>
          <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.15s]"></div>
          <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4">
      <div className="mb-4 relative">
        <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Buscar mascota..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-10"
        />
      </div>

      {filteredPets.length === 0 ? (
        <div className="text-center text-muted-foreground py-8">
          {searchTerm ? 'No se encontraron mascotas' : 'No sigues a ninguna mascota'}
        </div>
      ) : (
        <div className="space-y-2">
          {filteredPets.map((pet) => (
            <div
              key={pet.pet_id}
              onClick={() => onSelectPet(pet.pet_id)}
              className="flex items-center p-3 rounded-lg cursor-pointer hover:bg-accent"
            >
              <Avatar className="h-10 w-10 mr-3">
                <AvatarImage 
                  src={getMediaUrl(pet.pet_picture)} 
                  alt={pet.name} 
                />
                <AvatarFallback>{pet.name[0]}</AvatarFallback>
              </Avatar>
              <div>
                <h3 className="font-medium">{pet.name}</h3>
                <p className="text-sm text-muted-foreground">
                  {pet.breed?.breed_name || 'Sin raza especificada'}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};