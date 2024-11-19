import React from 'react';
import { Avatar, AvatarImage, AvatarFallback } from "../../ui/avatar";
import { Badge } from "../../ui/badge";
import { ScrollArea } from "../../ui/scroll-area";
import { format } from 'date-fns';
import { getMediaUrl } from '../../services/config/axios';

export const ChatList = ({ conversations = [], onSelectChat, selectedPetId }) => {
  if (!Array.isArray(conversations) || conversations.length === 0) {
    return (
      <div className="p-4 text-center text-muted-foreground">
        No hay conversaciones disponibles
      </div>
    );
  }

  return (
    <ScrollArea className="h-[calc(100vh-4rem)]">
      <div className="p-4">
        <h2 className="text-xl font-semibold mb-4">Mensajes</h2>
        <div className="space-y-2">
          {conversations.map((chat) => (
            <div
              key={chat.other_pet.pet_id}
              onClick={() => onSelectChat(chat.other_pet.pet_id)}
              className={`
                flex items-center p-3 rounded-lg cursor-pointer
                transition-colors duration-200
                ${selectedPetId === chat.other_pet.pet_id ? 'bg-primary/10' : 'hover:bg-accent'}
              `}
            >
              <Avatar className="h-12 w-12 mr-3">
                <AvatarImage 
                  src={getMediaUrl(chat.other_pet.pet_picture)} 
                  alt={chat.other_pet.name} 
                />
                <AvatarFallback>{chat.other_pet.name[0]}</AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <div className="flex justify-between items-start">
                  <h3 className="font-medium truncate">{chat.other_pet.name}</h3>
                  <span className="text-xs text-muted-foreground">
                    {format(new Date(chat.last_message.created_at), 'HH:mm')}
                  </span>
                </div>
                <p className="text-sm text-muted-foreground truncate">
                  {chat.last_message.message}
                </p>
                {chat.unread_count > 0 && (
                  <Badge variant="default" className="mt-1">
                    {chat.unread_count} nuevo{chat.unread_count !== 1 ? 's' : ''}
                  </Badge>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </ScrollArea>
  );
};