import React, { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import { PasswordStrengthBar } from './PasswordStrengthBar';
import { PasswordRequirements } from './PasswordRequirements';
import { validatePassword } from '../utils/passwordValidation';

export const PasswordInput = ({ 
    register, 
    name, 
    label, 
    error, 
    placeholder, 
    validate, 
    onChange,
    showRequirements = true 
}) => {
    const [showPassword, setShowPassword] = useState(false);
    const [passwordStrength, setPasswordStrength] = useState(0);
    const [currentPassword, setCurrentPassword] = useState('');

    const handlePasswordChange = (e) => {
        const newPassword = e.target.value;
        setCurrentPassword(newPassword);
        const validation = validatePassword(newPassword);
        setPasswordStrength(validation.strength);
        if (onChange) onChange(e);
    };

    return (
        <div className="space-y-2 w-full">
            <label className="text-sm font-medium text-gray-700">
                {label}
            </label>
            <div className="relative">
                <input
                    type={showPassword ? "text" : "password"}
                    {...register(name, {
                        ...validate,
                        onChange: handlePasswordChange
                    })}
                    className={`w-full px-4 py-3 rounded-lg border ${error ? 'border-[#d55b49]' : 'border-gray-300'} 
                                focus:ring-2 focus:ring-[#509ca2] focus:border-transparent transition-all 
                                bg-white/50 backdrop-blur-sm pr-10`}
                    placeholder={placeholder}
                />
                <div 
                    className="absolute inset-y-0 right-0 flex items-center pr-2 cursor-pointer"
                    onClick={() => setShowPassword(!showPassword)}
                >
                    {showPassword ? (
                        <Eye className="h-5 w-5 text-[#d55b49] hover:text-[#509ca2] transition-colors duration-200" />
                    ) : (
                        <EyeOff className="h-5 w-5 text-[#d55b49] hover:text-[#509ca2] transition-colors duration-200" />
                    )}
                </div>
            </div>
            {showRequirements && currentPassword && (
                <>
                    <PasswordStrengthBar strength={passwordStrength} />
                    <PasswordRequirements password={currentPassword} />
                </>
            )}
            {error && (
                <p className="text-sm text-[#d55b49]">{error.message}</p>
            )}
        </div>
    );
};