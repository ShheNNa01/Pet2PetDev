import React, { useState, useEffect } from "react";
import { 
    Bone, Dog, CircleDot, User, Fish, Video, 
    MessageCircle, Send, PawPrint, ChevronLeft, Menu,
    Settings, LogOut, LayoutDashboard 
} from 'lucide-react';
import logo from '../../assets/icons/Mesa de trabajo 50.png';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { usePet } from '../context/PetContext';
import { petService } from '../services/petService';
import { Button } from "../ui/button";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "../ui/dropdown-menu";
import { Sheet, SheetContent, SheetTrigger } from "../ui/sheet";
import { ScrollArea } from "../ui/scroll-area";
import { Input } from "../ui/input";
import { Avatar, AvatarImage, AvatarFallback } from "../ui/avatar";

export default function Header() {
    const navigate = useNavigate();
    const { user, logout } = useAuth();
    const { currentPet, setCurrentPet } = usePet();
    const [myPets, setMyPets] = useState([]);
    const [chatOpen, setChatOpen] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [selectedChat, setSelectedChat] = useState(null);
    const [chatMessage, setChatMessage] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Cargar mascotas del usuario
    useEffect(() => {
        const loadMyPets = async () => {
            try {
                setLoading(true);
                setError(null);
                const token = localStorage.getItem('token');
                
                if (!token) {
                    console.error('No token found');
                    return;
                }

                const response = await petService.getMyPets();
                console.log('Respuesta de mascotas:', response);
                
                const petsData = Array.isArray(response) ? response : response.data || [];
                console.log('Mascotas cargadas:', petsData);
                
                setMyPets(petsData);

                // Si no hay mascota seleccionada y hay mascotas disponibles, seleccionar la primera
                if (!currentPet && petsData.length > 0) {
                    setCurrentPet(petsData[0]);
                }
            } catch (error) {
                console.error('Error loading pets:', error);
                setError('Error al cargar las mascotas');
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            loadMyPets();
        }
    }, [user, currentPet, setCurrentPet]);

    const handlePetChange = (pet) => {
        console.log('Cambiando a mascota:', pet);
        setCurrentPet(pet);
    };

    const handleLogout = async () => {
        try {
            await logout();
            navigate('/');
        } catch (error) {
            console.error('Error during logout:', error);
        }
    };

    // Datos de ejemplo para el chat (puedes reemplazarlos con datos reales)
    const petChats = [
        { id: 1, pet: 'Firulais', lastMessage: 'Hola!', avatar: 'path-to-avatar.jpg' },
        { id: 2, pet: 'Mittens', lastMessage: '¿Cómo estás?', avatar: 'path-to-avatar.jpg' },
        { id: 3, pet: 'Rocky', lastMessage: '¿Vamos al parque?', avatar: 'path-to-avatar.jpg' }
    ];

    return (
        <nav className="bg-white shadow-sm sticky top-0 z-10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <div className="flex items-center">
                        <img src={logo} alt="Logo de Pet2Pet" className="h-16 w-32" />
                    </div>

                    {/* Navigation Links - Desktop */}
                    <div className="hidden md:flex items-center justify-center space-x-8">
                        <NavItem icon={<Bone className="text-pink-500" />} text="Nido" onClick={() => navigate('/')} />
                        <NavItem icon={<CircleDot className="text-green-500" />} text="Descubrir" onClick={() => navigate('/discover')} />
                        <NavItem icon={<Dog className="text-purple-500 h-10 w-10" />} text="Mis Peludos" onClick={() => navigate('/pets')} />
                        <NavItem icon={<Fish className="text-blue-500" />} text="Chismes" onClick={() => navigate('/gossip')} />
                        <NavItem icon={<Video className="text-red-500" />} text="Cine" onClick={() => navigate('/cinema')} />
                    </div>

                    {/* Right Side Icons */}
                    <div className="flex items-center space-x-4">
                        {/* Chat Button */}
                        <Sheet open={chatOpen} onOpenChange={setChatOpen}>
                            <SheetTrigger asChild>
                                <Button variant="ghost" size="icon" className="relative">
                                    <MessageCircle className="h-5 w-5" />
                                    <span className="absolute top-0 right-0 h-2 w-2 bg-red-500 rounded-full"></span>
                                </Button>
                            </SheetTrigger>
                            <SheetContent side="right" className="w-[300px] sm:w-[400px]">
                                {selectedChat ? (
                                    <div className="flex flex-col h-full">
                                        <Button variant="ghost" onClick={() => setSelectedChat(null)} className="mb-4">
                                            <ChevronLeft className="mr-2 h-4 w-4" />
                                            Volver a chats
                                        </Button>
                                        <ScrollArea className="flex-grow mb-4">
                                            <div className="space-y-4">
                                                <div className="flex justify-start">
                                                    <div className="bg-white rounded-lg p-2 max-w-[80%]">
                                                        <p className="text-sm">¡Hola! ¿Cómo estás?</p>
                                                    </div>
                                                </div>
                                                <div className="flex justify-end">
                                                    <div className="bg-blue-500 text-white rounded-lg p-2 max-w-[80%]">
                                                        <p className="text-sm">¡Muy bien! ¿Y tú?</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </ScrollArea>
                                        <div className="flex items-center mt-4">
                                            <Input 
                                                placeholder="Escribe un mensaje..." 
                                                value={chatMessage}
                                                onChange={(e) => setChatMessage(e.target.value)}
                                                className="flex-grow mr-2" 
                                            />
                                            <Button size="icon" onClick={() => setChatMessage('')}>
                                                <Send className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </div>
                                ) : (
                                    <ScrollArea className="h-full">
                                        <h2 className="text-lg font-semibold mb-4">Chats de mascotas</h2>
                                        {petChats.map((chat) => (
                                            <div
                                                key={chat.id}
                                                className="flex items-center p-2 hover:bg-accent rounded-md cursor-pointer"
                                                onClick={() => setSelectedChat(chat.id)}
                                            >
                                                <Avatar className="h-10 w-10 mr-3">
                                                    <AvatarImage src={chat.avatar} alt={chat.pet} />
                                                    <AvatarFallback>{chat.pet[0]}</AvatarFallback>
                                                </Avatar>
                                                <div>
                                                    <h3 className="font-semibold">{chat.pet}</h3>
                                                    <p className="text-sm text-muted-foreground">{chat.lastMessage}</p>
                                                </div>
                                            </div>
                                        ))}
                                    </ScrollArea>
                                )}
                            </SheetContent>
                        </Sheet>

                        {/* User Menu */}
                        <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                                <Button variant="ghost" size="icon">
                                    <User className="h-5 w-5" />
                                </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                                <DropdownMenuItem 
                                    onClick={() => navigate('/profile')}
                                    className="cursor-pointer"
                                >
                                    <User className="w-4 h-4 mr-2" />
                                    Perfil
                                </DropdownMenuItem>

                                {user?.role_id === 2 && (
                                    <DropdownMenuItem 
                                        onClick={() => navigate('/dashboard')}
                                        className="cursor-pointer text-[#d55b49]"
                                    >
                                        <LayoutDashboard className="w-4 h-4 mr-2" />
                                        Dashboard
                                    </DropdownMenuItem>
                                )}

                                <DropdownMenuItem 
                                    onClick={() => navigate('/settings')}
                                    className="cursor-pointer"
                                >
                                    <Settings className="w-4 h-4 mr-2" />
                                    Configuración
                                </DropdownMenuItem>

                                <DropdownMenuItem 
                                    onClick={handleLogout}
                                    className="cursor-pointer text-red-600"
                                >
                                    <LogOut className="w-4 h-4 mr-2" />
                                    Cerrar sesión
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>

                        {/* Pet Selector */}
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

                        {/* Mobile Menu */}
                        <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
                            <SheetTrigger asChild>
                                <Button variant="ghost" size="icon" className="md:hidden">
                                    <Menu className="h-5 w-5" />
                                </Button>
                            </SheetTrigger>
                            <SheetContent side="left" className="w-[300px] sm:w-[400px]">
                                <nav className="flex flex-col space-y-4">
                                    <NavItem icon={<Bone className="text-pink-500" />} text="Nido" onClick={() => navigate('/')} />
                                    <NavItem icon={<CircleDot className="text-green-500" />} text="Descubrir" onClick={() => navigate('/discover')} />
                                    <NavItem icon={<Dog className="text-purple-500" />} text="Mis Peludos" onClick={() => navigate('/pets')} />
                                    <NavItem icon={<Fish className="text-blue-500" />} text="Chismes" onClick={() => navigate('/gossip')} />
                                    <NavItem icon={<Video className="text-red-500" />} text="Cine" onClick={() => navigate('/cinema')} />
                                </nav>
                            </SheetContent>
                        </Sheet>
                    </div>
                </div>
            </div>
        </nav>
    );
}

function NavItem({ icon, text, onClick }) {
    return (
        <Button variant="ghost" className="flex items-center space-x-2" onClick={onClick}>
            {icon}
            <span>{text}</span>
        </Button>
    );
}