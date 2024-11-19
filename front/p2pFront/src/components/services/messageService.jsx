// src/services/messageService.js

import axiosInstance from './config/axios';

export const messageService = {
    // Obtener todas las conversaciones
    getConversations: async () => {
        try {
            const response = await axiosInstance.get('/messages/conversations');
            return response.data;
        } catch (error) {
            console.error('Error obteniendo conversaciones:', error);
            throw error;
        }
    },

    // Obtener mensajes de una conversación específica
    getConversation: async (otherPetId, skip = 0, limit = 50) => {
        try {
            const response = await axiosInstance.get(`/messages/conversation/${otherPetId}`, {
                params: { skip, limit }
            });
            return response.data;
        } catch (error) {
            console.error('Error obteniendo conversación:', error);
            throw error;
        }
    },

    // Enviar un nuevo mensaje
    sendMessage: async (receiverPetId, message) => {
        try {
            const response = await axiosInstance.post('/messages/', {
                receiver_pet_id: receiverPetId,
                message
            });
            return response.data;
        } catch (error) {
            console.error('Error enviando mensaje:', error);
            throw error;
        }
    },

    // Marcar conversación como leída
    markAsRead: async (otherPetId) => {
        try {
            const response = await axiosInstance.put(`/messages/conversation/${otherPetId}/read`);
            return response.data;
        } catch (error) {
            console.error('Error marcando conversación como leída:', error);
            throw error;
        }
    },

    // Obtener estadísticas de mensajes no leídos
    getUnreadStats: async () => {
        try {
            const response = await axiosInstance.get('/messages/unread/count');
            return response.data;
        } catch (error) {
            console.error('Error obteniendo estadísticas de mensajes:', error);
            throw error;
        }
    }
};