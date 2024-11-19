import React, { useState } from 'react';
import { MessageCircle, Send, ChevronLeft } from 'lucide-react';
import { Sheet, SheetContent, SheetTrigger } from "../../ui/sheet";
import { ScrollArea } from "../../ui/scroll-area";
import { Input } from "../../ui/input";
import { Button } from "../../ui/button";
import { ChatList } from './ChatList';
import { ChatMessage } from './ChatMessage';

export const ChatPanel = () => {
    const [chatOpen, setChatOpen] = useState(false);
    const [selectedChat, setSelectedChat] = useState(null);
    const [chatMessage, setChatMessage] = useState("");

    // Datos de ejemplo para el chat (puedes reemplazarlos con datos reales)
    const petChats = [
        { id: 1, pet: 'Firulais', lastMessage: 'Hola!', avatar: 'path-to-avatar.jpg' },
        { id: 2, pet: 'Mittens', lastMessage: '¿Cómo estás?', avatar: 'path-to-avatar.jpg' },
        { id: 3, pet: 'Rocky', lastMessage: '¿Vamos al parque?', avatar: 'path-to-avatar.jpg' }
    ];

    // Mensajes de ejemplo (puedes reemplazarlos con datos reales)
    const messages = [
        { id: 1, text: "¡Hola! ¿Cómo estás?", isOutgoing: false },
        { id: 2, text: "¡Muy bien! ¿Y tú?", isOutgoing: true }
    ];

    const handleSendMessage = () => {
        if (chatMessage.trim()) {
            // Aquí puedes implementar la lógica para enviar el mensaje
            console.log('Enviando mensaje:', chatMessage);
            setChatMessage('');
        }
    };

    return (
        <Sheet open={chatOpen} onOpenChange={setChatOpen}>
            <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="relative">
                    <MessageCircle className="h-5 w-5" />
                    <span className="absolute top-0 right-0 h-2 w-2 bg-red-500 rounded-full"></span>
                </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-[300px] sm:w-[400px]">
                {selectedChat ? (
                    <div className="flex flex-col h-full">
                        <Button 
                            variant="ghost" 
                            onClick={() => setSelectedChat(null)} 
                            className="mb-4"
                        >
                            <ChevronLeft className="mr-2 h-4 w-4" />
                            Volver a chats
                        </Button>
                        <ScrollArea className="flex-grow mb-4">
                            <div className="space-y-4">
                                {messages.map((message) => (
                                    <ChatMessage 
                                        key={message.id}
                                        message={message.text}
                                        isOutgoing={message.isOutgoing}
                                    />
                                ))}
                            </div>
                        </ScrollArea>
                        <div className="flex items-center mt-4">
                            <Input 
                                placeholder="Escribe un mensaje..." 
                                value={chatMessage}
                                onChange={(e) => setChatMessage(e.target.value)}
                                className="flex-grow mr-2"
                                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                            />
                            <Button 
                                size="icon" 
                                onClick={handleSendMessage}
                                disabled={!chatMessage.trim()}
                            >
                                <Send className="h-4 w-4" />
                            </Button>
                        </div>
                    </div>
                ) : (
                    <ChatList 
                        chats={petChats} 
                        onSelectChat={setSelectedChat}
                    />
                )}
            </SheetContent>
        </Sheet>
    );
};