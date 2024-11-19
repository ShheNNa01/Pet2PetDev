import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Bone, CircleDot, Dog, Fish, Video } from 'lucide-react';
import { NavItem } from './NavItem';

export const NavigationDesktop = () => {
    const navigate = useNavigate();
    
    return (
        <div className="hidden md:flex items-center justify-center space-x-8">
            <NavItem 
                icon={<Bone className="text-pink-500" />} 
                text="Nido" 
                onClick={() => navigate('/')} 
            />
            <NavItem 
                icon={<CircleDot className="text-green-500" />} 
                text="Descubrir" 
                onClick={() => navigate('/discover')} 
            />
            <NavItem 
                icon={<Dog className="text-purple-500 h-10 w-10" />} 
                text="Mis Peludos" 
                onClick={() => navigate('/pets')} 
            />
            <NavItem 
                icon={<Fish className="text-blue-500" />} 
                text="Chismes" 
                onClick={() => navigate('/gossip')} 
            />
            <NavItem 
                icon={<Video className="text-red-500" />} 
                text="Cine" 
                onClick={() => navigate('/cinema')} 
            />
        </div>
    );
};