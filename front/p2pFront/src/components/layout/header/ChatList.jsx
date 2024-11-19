import React from 'react';
import { Avatar, AvatarImage, AvatarFallback } from "../../ui/avatar";
import { ScrollArea } from "../../ui/scroll-area";

export const ChatList = ({ chats, onSelectChat }) => {
    return (
        <ScrollArea className="h-full">
            <h2 className="text-lg font-semibold mb-4">Chats de mascotas</h2>
            {chats.map((chat) => (
                <div
                    key={chat.id}
                    className="flex items-center p-2 hover:bg-accent rounded-md cursor-pointer"
                    onClick={() => onSelectChat(chat.id)}
                >
                    <Avatar className="h-10 w-10 mr-3">
                        <AvatarImage src={chat.avatar} alt={chat.pet} />
                        <AvatarFallback>{chat.pet[0]}</AvatarFallback>
                    </Avatar>
                    <div>
                        <h3 className="font-semibold">{chat.pet}</h3>
                        <p className="text-sm text-muted-foreground">{chat.lastMessage}</p>
                    </div>
                </div>
            ))}
        </ScrollArea>
    );
};