import React from 'react';
import { PawPrint } from 'lucide-react';

export const PetFormHeader = () => {
    return (
        <div className="text-center space-y-2 mb-8">
        <h1 className="text-3xl font-bold text-[#d55b49]">
            Registrar Mascota
        </h1>
        <p className="text-gray-500 italic">
            "Un registro para recordar que cada huella deja una historia"
        </p>
        <div className="flex justify-center">
            <PawPrint className="text-[#509ca2] h-8 w-8" />
        </div>
        </div>
    );
};