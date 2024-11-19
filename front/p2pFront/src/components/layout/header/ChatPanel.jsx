import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, Send, ChevronLeft } from 'lucide-react';
import { Sheet, SheetContent, SheetTrigger, SheetTitle } from "../../ui/sheet";
import { ScrollArea } from "../../ui/scroll-area";
import { Input } from "../../ui/input";
import { Button } from "../../ui/button";
import { Badge } from "../../ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../../ui/tabs";
import { messageService } from '../../services/messageService';
import { petService } from '../../services/petService';
import { ChatList } from './ChatList';
import { ChatMessage } from './ChatMessage';
import { FollowingPets } from './FollowingPets';

export const ChatPanel = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedChat, setSelectedChat] = useState(null);
  const [activeTab, setActiveTab] = useState("chats");
  const [conversations, setConversations] = useState([]);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [unreadCount, setUnreadCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [currentPetId, setCurrentPetId] = useState(null);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const getCurrentPet = async () => {
      try {
        const myPets = await petService.getMyPets();
        if (myPets && myPets.length > 0) {
          setCurrentPetId(myPets[0].pet_id);
        }
      } catch (error) {
        console.error('Error obteniendo mascota actual:', error);
      }
    };

    getCurrentPet();
  }, []);

  useEffect(() => {
    if (isOpen) {
      loadConversations();
    }
  }, [isOpen]);

  const loadConversations = async () => {
    try {
      setIsLoading(true);
      const [convos, stats] = await Promise.all([
        messageService.getConversations(),
        messageService.getUnreadStats()
      ]);
      setConversations(convos);
      setUnreadCount(stats?.total_unread || 0);
    } catch (error) {
      console.error('Error cargando conversaciones:', error);
      setError('No se pudieron cargar las conversaciones');
    } finally {
      setIsLoading(false);
    }
  };

  const loadMessages = async () => {
    if (selectedChat) {
      try {
        setIsLoading(true);
        const data = await messageService.getConversation(selectedChat);
        setMessages(data);
        await messageService.markAsRead(selectedChat);
        await loadConversations();
      } catch (error) {
        console.error('Error cargando mensajes:', error);
        setError('No se pudieron cargar los mensajes');
      } finally {
        setIsLoading(false);
      }
    }
  };

  useEffect(() => {
    loadMessages();
  }, [selectedChat]);

  const handleSendMessage = async () => {
    if (!newMessage.trim() || !selectedChat) return;

    try {
      const sent = await messageService.sendMessage(selectedChat, newMessage.trim());
      if (sent) {
        setMessages(prev => [...prev, sent]);
        setNewMessage('');
        await loadConversations();
      }
    } catch (error) {
      console.error('Error enviando mensaje:', error);
      setError('No se pudo enviar el mensaje');
    }
  };

  const handleSelectNewChat = async (petId) => {
    setSelectedChat(petId);
    setActiveTab("chats");
  };

  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          <MessageCircle className="h-5 w-5" />
          {unreadCount > 0 && (
            <Badge 
              variant="destructive" 
              className="absolute -top-1 -right-1 h-5 w-5 flex items-center justify-center p-0 text-xs"
            >
              {unreadCount}
            </Badge>
          )}
        </Button>
      </SheetTrigger>

      <SheetContent side="right" className="w-full sm:w-[400px] p-0">
        <SheetTitle className="sr-only">Chat</SheetTitle>
        
        <div className="flex flex-col h-full">
          {error && (
            <div className="p-4 text-sm text-red-500 bg-red-50">
              {error}
              <Button 
                variant="link" 
                size="sm" 
                onClick={() => {
                  setError(null);
                  selectedChat ? loadMessages() : loadConversations();
                }}
                className="ml-2"
              >
                Reintentar
              </Button>
            </div>
          )}

          {selectedChat ? (
            <div className="flex flex-col h-full">
              <div className="p-4 border-b">
                <Button 
                  variant="ghost" 
                  onClick={() => setSelectedChat(null)}
                  className="mb-2"
                >
                  <ChevronLeft className="mr-2 h-4 w-4" />
                  Volver
                </Button>
                {conversations.find(c => c.pet_id === selectedChat) && (
                  <div className="flex items-center">
                    <Avatar className="h-10 w-10 mr-3">
                      <AvatarImage 
                        src={getMediaUrl(conversations.find(c => c.pet_id === selectedChat).pet_picture)} 
                        alt="Pet avatar"
                      />
                      <AvatarFallback>
                        {conversations.find(c => c.pet_id === selectedChat).pet_name[0]}
                      </AvatarFallback>
                    </Avatar>
                    <h3 className="font-semibold">
                      {conversations.find(c => c.pet_id === selectedChat).pet_name}
                    </h3>
                  </div>
                )}
              </div>

              <ScrollArea className="flex-1 p-4">
                {messages.length === 0 ? (
                  <div className="flex flex-col items-center justify-center h-full text-muted-foreground">
                    <MessageCircle className="h-12 w-12 mb-2 opacity-20" />
                    <p>No hay mensajes aún</p>
                    <p className="text-sm">¡Envía el primer mensaje!</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {messages.map((msg) => (
                      <ChatMessage
                        key={msg.message_id}
                        message={msg.message}
                        isOutgoing={msg.sender_pet_id !== selectedChat}
                        timestamp={msg.created_at}
                      />
                    ))}
                    <div ref={messagesEndRef} />
                  </div>
                )}
              </ScrollArea>

              <div className="p-4 border-t">
                <form 
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSendMessage();
                  }}
                  className="flex items-center gap-2"
                >
                  <Input
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    placeholder="Escribe un mensaje..."
                    aria-label="Mensaje"
                    className="flex-1"
                  />
                  <Button 
                    type="submit"
                    disabled={!newMessage.trim()}
                    aria-label="Enviar mensaje"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </form>
              </div>
            </div>
          ) : (
            <Tabs defaultValue="chats" value={activeTab} onValueChange={setActiveTab}>
              <div className="border-b">
                <TabsList className="w-full">
                  <TabsTrigger value="chats" className="flex-1">
                    Chats
                  </TabsTrigger>
                  <TabsTrigger value="following" className="flex-1">
                    Siguiendo
                  </TabsTrigger>
                </TabsList>
              </div>

              <TabsContent value="chats" className="mt-0">
                <ChatList
                  conversations={conversations}
                  onSelectChat={setSelectedChat}
                  selectedPetId={selectedChat}
                />
              </TabsContent>

              <TabsContent value="following" className="mt-0">
                <FollowingPets
                  onSelectPet={handleSelectNewChat}
                  currentPetId={currentPetId}
                />
              </TabsContent>
            </Tabs>
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
};