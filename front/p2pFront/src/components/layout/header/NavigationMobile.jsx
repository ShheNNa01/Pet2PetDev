import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Menu, Bone, CircleDot, Dog, Fish, Video } from 'lucide-react';
import { Sheet, SheetContent, SheetTrigger } from "../../ui/sheet";
import { Button } from "../../ui/button";
import { NavItem } from './NavItem';

export const NavigationMobile = () => {
    const navigate = useNavigate();
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    return (
        <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
            <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="md:hidden">
                    <Menu className="h-5 w-5" />
                </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-[300px] sm:w-[400px]">
                <nav className="flex flex-col space-y-4">
                    <NavItem 
                        icon={<Bone className="text-pink-500" />} 
                        text="Nido" 
                        onClick={() => {
                            navigate('/');
                            setMobileMenuOpen(false);
                        }} 
                    />
                    <NavItem 
                        icon={<CircleDot className="text-green-500" />} 
                        text="Descubrir" 
                        onClick={() => {
                            navigate('/discover');
                            setMobileMenuOpen(false);
                        }} 
                    />
                    <NavItem 
                        icon={<Dog className="text-purple-500" />} 
                        text="Mis Peludos" 
                        onClick={() => {
                            navigate('/pets');
                            setMobileMenuOpen(false);
                        }} 
                    />
                    <NavItem 
                        icon={<Fish className="text-blue-500" />} 
                        text="Chismes" 
                        onClick={() => {
                            navigate('/gossip');
                            setMobileMenuOpen(false);
                        }} 
                    />
                    <NavItem 
                        icon={<Video className="text-red-500" />} 
                        text="Cine" 
                        onClick={() => {
                            navigate('/cinema');
                            setMobileMenuOpen(false);
                        }} 
                    />
                </nav>
            </SheetContent>
        </Sheet>
    );
};
