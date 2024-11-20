import React from 'react';
import { Textarea } from '../ui/textarea';
import Label from '../ui/label';

export const TextAreaField = ({ 
    label, 
    register, 
    name, 
    error, 
    placeholder,
    required = false 
}) => {
    return (
        <div className="space-y-2">
        <Label className="text-gray-700 font-medium">
            {label} {required && <span className="text-[#d55b49]">*</span>}
        </Label>
        <Textarea
            {...register(name)}
            placeholder={placeholder}
            className={`
            w-full px-4 py-3 rounded-lg min-h-[120px] resize-none
            ${error ? 'border-[#d55b49]' : 'border-[#509ca2]'}
            focus:ring-2 focus:ring-[#d55b49] focus:border-transparent
            bg-white hover:border-[#d55b49]
            transition-all duration-200
            `}
        />
        {error && (
            <p className="text-sm text-[#d55b49]">{error.message}</p>
        )}
        </div>
    );
};