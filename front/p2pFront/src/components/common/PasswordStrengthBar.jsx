import React from 'react';

export const PasswordStrengthBar = ({ strength }) => {
    const getColor = () => {
        if (strength >= 80) return 'bg-green-500';
        if (strength >= 60) return 'bg-blue-500';
        if (strength >= 40) return 'bg-yellow-500';
        if (strength >= 20) return 'bg-orange-500';
        return 'bg-red-500';
    };

    return (
        <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
                className={`h-full ${getColor()} transition-all duration-300`}
                style={{ width: `${strength}%` }}
            />
        </div>
    );
};
