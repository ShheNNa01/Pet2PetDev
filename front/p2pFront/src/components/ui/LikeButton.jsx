    // LikeButton.jsx
    import React, { useState } from 'react';
    import { Heart } from 'lucide-react';
    import { Button } from "./button";

    export default function LikeButton({ count, onLike, size = "default" }) {
    const [isLiked, setIsLiked] = useState(false);
    const [isAnimating, setIsAnimating] = useState(false);

    const handleLike = () => {
        setIsLiked(!isLiked);
        setIsAnimating(true);
        onLike();
        setTimeout(() => setIsAnimating(false), 500);
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
        `}
        >
        <Heart 
            className={`
            ${iconSize} mr-1.5 transition-all duration-200
            ${isAnimating ? 'scale-125' : 'scale-100'}
            ${isLiked ? 'fill-[#d55b49]' : 'fill-transparent group-hover:scale-110'}
            `}
        />
        {count}
        </Button>
    );
    }