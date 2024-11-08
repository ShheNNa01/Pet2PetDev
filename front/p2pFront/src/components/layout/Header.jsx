import React, { useState } from "react";
import { 
    Bone, Dog, CircleDot, User, Fish, Video, 
    MessageCircle, Send, PawPrint, ChevronLeft, Menu,
    Settings, LogOut, LayoutDashboard 
} from 'lucide-react';
import logo from '../../assets/icons/Mesa de trabajo 50.png';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from "../ui/button";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "../ui/dropdown-menu";
import { Sheet, SheetContent, SheetTrigger } from "../ui/sheet";
import { ScrollArea } from "../ui/scroll-area";
import { Input } from "../ui/input";
import { Avatar, AvatarImage, AvatarFallback } from "../ui/avatar";

export default function Header() {
    const navigate = useNavigate();
    const { user, logout } = useAuth();
    const [chatOpen, setChatOpen] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [selectedChat, setSelectedChat] = useState(null);
    const [chatMessage, setChatMessage] = useState("");

    const handleLogout = async () => {
        await logout();
        navigate('/');
    };
    const petChats = [
        { id: 1, pet: 'Firulais', lastMessage: 'Hola!', avatar: 'path-to-avatar.jpg' },
        { id: 2, pet: 'Mittens', lastMessage: '¿Cómo estás?', avatar: 'path-to-avatar.jpg' },
        { id: 3, pet: 'Rocky', lastMessage: '¿Vamos al parque?', avatar: 'path-to-avatar.jpg' }
    ];

    return (
        <nav className="bg-white shadow-sm sticky top-0 z-10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    <div className="flex items-center">
                        <img src={logo} alt="Logo de Pet2Pet" className="h-16 w-32" />
                    </div>
                    <div className="hidden md:flex items-center justify-center space-x-8">
                        <NavItem icon={<Bone className="text-pink-500" />} text="Nido" />
                        <NavItem icon={<CircleDot className="text-green-500" />} text="Descubrir" />
                        <NavItem icon={<Dog className="text-purple-500 h-10 w-10" />} text="Mis Peludos" />
                        <NavItem icon={<Fish className="text-blue-500" />} text="Chismes" />
                        <NavItem icon={<Video className="text-red-500" />} text="Cine" />
                    </div>
                    <div className="flex items-center space-x-4">
                        <Sheet open={chatOpen} onOpenChange={setChatOpen}>
                            <SheetTrigger asChild>
                                <Button variant="ghost" size="icon" className="relative" aria-label="Chat de mascotas">
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
                        <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                                <Button variant="ghost" size="icon" aria-label="Perfil de usuario">
                                    <User className="h-5 w-5" />
                                </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                                <DropdownMenuItem 
                                    onClick={() => navigate('/profile')}
                                    className="cursor-pointer"
                                >
                                    Perfil
                                </DropdownMenuItem>

                                {user?.is_admin && (
                                    <DropdownMenuItem 
                                        onClick={() => navigate('/dashboard')}
                                        className="cursor-pointer text-[#d55b49]"
                                    >
                                        Dashboard
                                    </DropdownMenuItem>
                                )}

                                <DropdownMenuItem 
                                    onClick={() => navigate('/settings')}
                                    className="cursor-pointer"
                                >
                                    Configuración
                                </DropdownMenuItem>

                                <DropdownMenuItem 
                                    onClick={handleLogout}
                                    className="cursor-pointer text-red-600"
                                >
                                    Cerrar sesión
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                        <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                                <Button variant="ghost" size="icon" aria-label="Cambiar mascota">
                                    <PawPrint className="h-5 w-5 text-pink-500" />
                                </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                                <DropdownMenuItem>Firulais</DropdownMenuItem>
                                <DropdownMenuItem>Mittens</DropdownMenuItem>
                                <DropdownMenuItem>Rocky</DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                        <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
                            <SheetTrigger asChild>
                                <Button variant="ghost" size="icon" className="md:hidden" aria-label="Menú">
                                    <Menu className="h-5 w-5" />
                                </Button>
                            </SheetTrigger>
                            <SheetContent side="left" className="w-[300px] sm:w-[400px]">
                                <nav className="flex flex-col space-y-4">
                                    <NavItem icon={<Bone className="text-pink-500" />} text="Nido" />
                                    <NavItem icon={<CircleDot className="text-green-500" />} text="Descubrir" />
                                    <NavItem icon={<User className="text-purple-500" />} text="Mis Peludos" />
                                    <NavItem icon={<Fish className="text-blue-500" />} text="Chismes" />
                                    <NavItem icon={<Video className="text-red-500" />} text="Cine" />
                                </nav>
                            </SheetContent>
                        </Sheet>
                    </div>
                </div>
            </div>
        </nav>
    );
}

function NavItem({ icon, text }) {
    return (
        <Button variant="ghost" className="flex items-center space-x-2">
            {icon}
            <span>{text}</span>
        </Button>
    );
}
