import React from "react";
import logo from '../../../assets/icons/Mesa de trabajo 50.png';
import { NavigationDesktop } from './NavigationDesktop';
import { NavigationMobile } from './NavigationMobile';
import { ChatPanel } from './ChatPanel';
import { UserMenu } from './UserMenu';
import { PetSelector } from './PetSelector';

const Header = () => {
    return (
        <nav className="bg-white shadow-sm sticky top-0 z-10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Logo */}
                    <div className="flex items-center">
                        <img 
                            src={logo} 
                            alt="Logo de Pet2Pet" 
                            className="h-16 w-32" 
                        />
                    </div>

                    {/* Navigation Links - Desktop */}
                    <NavigationDesktop />

                    {/* Right Side Icons */}
                    <div className="flex items-center space-x-4">
                        <ChatPanel />
                        <UserMenu />
                        <PetSelector />
                        <NavigationMobile />
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Header;