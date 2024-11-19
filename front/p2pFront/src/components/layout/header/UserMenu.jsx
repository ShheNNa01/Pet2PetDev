import React from 'react';
import { useNavigate } from 'react-router-dom';
import { 
    User, 
    Settings, 
    LogOut, 
    LayoutDashboard 
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { Button } from "../../ui/button";
import { 
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger 
} from "../../ui/dropdown-menu";

export const UserMenu = () => {
    const navigate = useNavigate();
    const { user, logout } = useAuth();

    const handleLogout = async () => {
        try {
            await logout();
            navigate('/');
        } catch (error) {
            console.error('Error during logout:', error);
        }
    };

    return (
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
    );
};