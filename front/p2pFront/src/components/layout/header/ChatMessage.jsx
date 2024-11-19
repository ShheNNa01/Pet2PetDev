import React from 'react';

export const ChatMessage = ({ message, isOutgoing }) => {
    return (
        <div className={`flex justify-${isOutgoing ? 'end' : 'start'}`}>
            <div className={`${
                isOutgoing 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-white'
                } rounded-lg p-2 max-w-[80%]`}
            >
                <p className="text-sm">{message}</p>
            </div>
        </div>
    );
};