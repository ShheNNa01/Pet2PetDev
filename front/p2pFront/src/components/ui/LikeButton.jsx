import React, { useState, useEffect } from 'react';
import { Heart } from 'lucide-react';
import { Button } from "./button";
import { usePet } from '../context/PetContext';
import { postService } from '../services/PostService';

export default function LikeButton({ postId, initialLikes, initialPetReactionId, size = "default" }) {
    const { currentPet } = usePet();
    const [isLiked, setIsLiked] = useState(!!initialPetReactionId);
    const [likesCount, setLikesCount] = useState(initialLikes || 0);
    const [isAnimating, setIsAnimating] = useState(false);
    const [reactionId, setReactionId] = useState(initialPetReactionId);

    // Actualizar el estado cuando cambia la mascota seleccionada
    useEffect(() => {
        // Resetear el estado cuando se cambia de mascota
        setIsLiked(false);
        setReactionId(null);
    }, [currentPet?.pet_id]);

    const handleLike = async () => {
        if (!currentPet?.pet_id) {
            alert('Por favor, selecciona una mascota antes de dar like');
            return;
        }

        try {
            setIsAnimating(true);
            
            const result = await postService.toggleReaction(
                postId, 
                reactionId, 
                currentPet.pet_id // Añadimos el pet_id a la llamada
            );
            
            setIsLiked(result.liked);
            setReactionId(result.reactionId);
            setLikesCount(prev => result.liked ? prev + 1 : prev - 1);
            
            setTimeout(() => setIsAnimating(false), 500);
        } catch (error) {
            console.error('Error al procesar like:', error);
            alert('Error al procesar la reacción');
            // Revertir cambios visuales en caso de error
            setIsLiked(!isLiked);
            setLikesCount(prev => isLiked ? prev - 1 : prev + 1);
        }
    };

    const buttonSize = size === "small" ? "h-5 text-xs" : "h-8 text-sm";
    const iconSize = size === "small" ? "h-3 w-3" : "h-4 w-4";

    return (
        <Button
            variant="ghost"
            size="sm"
            onClick={handleLike}
            className={`
                group transition-all duration-200 ${buttonSize}
                ${isLiked ? "text-[#d55b49]" : "text-gray-500 hover:text-[#d55b49]"}
                ${!currentPet?.pet_id ? 'cursor-not-allowed opacity-50' : ''}
            `}
            disabled={!currentPet?.pet_id}
            title={!currentPet?.pet_id ? 'Selecciona una mascota para dar like' : ''}
        >
            <Heart
                className={`
                    ${iconSize} mr-1.5 transition-all duration-200
                    ${isAnimating ? 'scale-125' : 'scale-100'}
                    ${isLiked ? 'fill-[#d55b49]' : 'fill-transparent group-hover:scale-110'}
                `}
            />
            {likesCount}
        </Button>
    );
}