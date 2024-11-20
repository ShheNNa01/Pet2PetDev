import React from 'react';
import { Check, X } from 'lucide-react';
import { passwordRequirements } from '../utils/passwordValidation';

export const PasswordRequirements = ({ password }) => {
    return (
        <div className="space-y-2 mt-2">
            {passwordRequirements.map((req, index) => (
                <div key={index} className="flex items-center space-x-2">
                    {req.test(password) ? (
                        <Check className="h-4 w-4 text-green-500" />
                    ) : (
                        <X className="h-4 w-4 text-red-500" />
                    )}
                    <span className={`text-sm ${req.test(password) ? 'text-green-500' : 'text-gray-500'}`}>
                        {req.label}
                    </span>
                </div>
            ))}
        </div>
    );
};