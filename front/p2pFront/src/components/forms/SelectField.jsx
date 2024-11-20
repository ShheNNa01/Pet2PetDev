import React from 'react';
import Label from '../ui/label';

export const SelectField = ({ 
    label, 
    value, 
    onChange, 
    options, 
    placeholder, 
    error, 
    disabled = false,
    required = false 
}) => {
    return (
        <div className="space-y-2">
        <Label className="text-gray-700 font-medium">
            {label} {required && <span className="text-[#d55b49]">*</span>}
        </Label>
        <div className="relative">
            <select
            value={value}
            onChange={onChange}
            disabled={disabled}
            className={`
                w-full rounded-lg border px-4 py-2.5
                ${disabled ? 'bg-gray-50' : 'bg-white'}
                ${error ? 'border-[#d55b49]' : 'border-[#509ca2]'}
                focus:ring-2 focus:ring-[#d55b49] focus:border-transparent
                hover:cursor-pointer appearance-none
                transition-all duration-200
            `}
            style={{ maxHeight: '256px', overflowY: 'auto' }}
            >
            <option value="">{placeholder}</option>
            {options.map((option) => (
                <option 
                key={option.value} 
                value={option.value}
                >
                {option.label}
                </option>
            ))}
            </select>
            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3">
            <svg className="h-5 w-5 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
            </div>
        </div>
        {error && (
            <p className="text-sm text-[#d55b49]">{error}</p>
        )}
        </div>
    );
};