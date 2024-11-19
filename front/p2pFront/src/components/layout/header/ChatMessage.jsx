import React from 'react';
import { format } from 'date-fns';

export const ChatMessage = ({ message, isOutgoing, timestamp }) => {
  return (
    <div className={`flex ${isOutgoing ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`
        max-w-[80%] px-4 py-2 rounded-2xl
        ${isOutgoing 
          ? 'bg-primary text-primary-foreground rounded-br-sm' 
          : 'bg-muted rounded-bl-sm'
        }
      `}>
        <p className="text-sm whitespace-pre-wrap break-words">
          {message}
        </p>
        {timestamp && (
          <span className="text-xs opacity-70 mt-1 block">
            {format(new Date(timestamp), 'HH:mm')}
          </span>
        )}
      </div>
    </div>
  );
};