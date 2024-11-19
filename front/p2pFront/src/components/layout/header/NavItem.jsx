import React from 'react';
import { Button } from "../../ui/button";

export const NavItem = ({ icon, text, onClick }) => {
    return (
        <Button 
            variant="ghost" 
            className="flex items-center space-x-2" 
            onClick={onClick}
        >
            {icon}
            <span>{text}</span>
        </Button>
    );
};