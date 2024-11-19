import axiosInstance from './config/axios';

export const petService = {
    // Obtener tipos de mascotas
    getPetTypes: async () => {
        try {
            const response = await axiosInstance.get('/pets/types', {
                params: { 
                    skip: 0,
                    limit: 100
                }
            });
            return response.data;
        } catch (error) {
            console.error('Error obteniendo tipos de mascotas:', error);
            throw error;
        }
    },

    // Obtener razas
    getBreeds: async (params = {}) => {
        try {
            const { pet_type_id } = params;
            const response = await axiosInstance.get('/pets/breeds', {
                params: {
                    pet_type_id,
                    skip: 0,
                    limit: 100
                }
            });
            return response.data;
        } catch (error) {
            console.error('Error obteniendo razas:', error);
            throw error;
        }
    },

    // Crear nueva mascota
    createPet: async (petData) => {
        try {
            if (!petData.name || !petData.birthdate || !petData.breed_id || !petData.gender) {
                throw new Error('Faltan datos requeridos para crear la mascota');
            }
    
            const response = await axiosInstance.post('/pets', petData);
            return response.data;
        } catch (error) {
            console.error('Error creando mascota:', error);
            throw error;
        }
    },

    // Obtener mis mascotas
    getMyPets: async (params = {}) => {
        try {
            const { skip = 0, limit = 10 } = params;
            const response = await axiosInstance.get('/pets/my-pets', {
                params: { skip, limit }
            });
            return response.data;
        } catch (error) {
            console.error('Error obteniendo mis mascotas:', error);
            throw error;
        }
    },

    // Obtener mascota por ID
    getPetById: async (petId) => {
        try {
            if (!petId) throw new Error('Se requiere el ID de la mascota');
            const response = await axiosInstance.get(`/pets/${petId}`);
            return response.data;
        } catch (error) {
            console.error('Error obteniendo mascota:', error);
            throw error;
        }
    },

    // Actualizar mascota
    updatePet: async (petId, updateData) => {
        try {
            if (!petId) throw new Error('Se requiere el ID de la mascota');
            
            const validFields = {
                name: updateData.name,
                breed_id: updateData.breed_id,
                birthdate: updateData.birthdate,
                gender: updateData.gender,
                bio: updateData.bio,
                status: updateData.status
            };

            const cleanedFields = Object.entries(validFields)
                .reduce((acc, [key, value]) => {
                    if (value !== undefined && value !== null) {
                        acc[key] = value;
                    }
                    return acc;
                }, {});

            const response = await axiosInstance.put(`/pets/${petId}`, cleanedFields);
            return response.data;
        } catch (error) {
            console.error('Error actualizando mascota:', error);
            throw error;
        }
    },

    // Subir imagen de mascota
    uploadPetImage: async (petId, file) => {
        try {
            if (!petId || !file) {
                throw new Error('Se requiere el ID de la mascota y el archivo');
            }

            const formData = new FormData();
            formData.append('file', file);

            const response = await axiosInstance.post(`/pets/${petId}/image`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            return response.data;
        } catch (error) {
            console.error('Error subiendo imagen de mascota:', error);
            throw error;
        }
    },

    // Eliminar mascota
    deletePet: async (petId) => {
        try {
            if (!petId) throw new Error('Se requiere el ID de la mascota');
            const response = await axiosInstance.delete(`/pets/${petId}`);
            return response.data;
        } catch (error) {
            console.error('Error eliminando mascota:', error);
            throw error;
        }
    },

    // Seguir mascota con actualización de contadores
    followPet: async (petId, followerPetId) => {
        try {
            if (!petId || !followerPetId) {
                throw new Error('Se requieren ambos IDs de mascota');
            }
    
            const response = await axiosInstance.post(`/pets/${petId}/follow`, null, {
                params: {
                    follower_pet_id: followerPetId
                }
            });
    
            // Emitir evento personalizado para notificar el cambio
            const event = new CustomEvent('petFollowStatusChanged', {
                detail: { petId, followerPetId, action: 'follow' }
            });
            window.dispatchEvent(event);
    
            return response.data;
        } catch (error) {
            console.error('Error siguiendo mascota:', error);
            throw error;
        }
    },
    
    unfollowPet: async (petId, followerPetId) => {
        try {
            if (!petId || !followerPetId) {
                throw new Error('Se requieren ambos IDs de mascota');
            }
    
            const response = await axiosInstance.post(`/pets/${petId}/unfollow`, null, {
                params: {
                    follower_pet_id: followerPetId
                }
            });
    
            // Emitir evento personalizado para notificar el cambio
            const event = new CustomEvent('petFollowStatusChanged', {
                detail: { petId, followerPetId, action: 'unfollow' }
            });
            window.dispatchEvent(event);
    
            return response.data;
        } catch (error) {
            console.error('Error dejando de seguir mascota:', error);
            throw error;
        }
    },

    // Obtener seguidores con contador
    getPetFollowers: async (petId, params = {}) => {
        try {
            if (!petId) throw new Error('Se requiere el ID de la mascota');
            
            const { skip = 0, limit = 10 } = params;
            const response = await axiosInstance.get(`/pets/${petId}/followers`, {
                params: { skip, limit }
            });

            // Asegurarse de que la respuesta incluya el contador total
            return {
                followers: response.data,
                total: response.headers['x-total-count'] || response.data.length
            };
        } catch (error) {
            console.error('Error obteniendo seguidores:', error);
            throw error;
        }
    },

    // Obtener seguidos con contador
    getPetFollowing: async (petId, params = {}) => {
        try {
            if (!petId) throw new Error('Se requiere el ID de la mascota');
            
            const { skip = 0, limit = 10 } = params;
            const response = await axiosInstance.get(`/pets/${petId}/following`, {
                params: { skip, limit }
            });

            // Asegurarse de que la respuesta incluya el contador total
            return {
                following: response.data,
                total: response.headers['x-total-count'] || response.data.length
            };
        } catch (error) {
            console.error('Error obteniendo mascotas seguidas:', error);
            throw error;
        }
    },

    // Obtener contadores de seguidores y seguidos
    getFollowCounts: async (petId) => {
        try {
            if (!petId) throw new Error('Se requiere el ID de la mascota');
    
            const response = await axiosInstance.get(`/pets/${petId}/followers/count`);
            return {
                followersCount: response.data.followers_count,
                followingCount: response.data.following_count
            };
        } catch (error) {
            console.error('Error obteniendo contadores:', error);
            throw error;
        }
    },

    // Actualizar contadores localmente
    updateFollowCounts: async (petId, followerPetId, isFollowing) => {
        try {
            // Actualizar los contadores para ambas mascotas
            const [targetPet, followerPet] = await Promise.all([
                petService.getFollowCounts(petId),
                petService.getFollowCounts(followerPetId)
            ]);

            return {
                targetPet: targetPet,
                followerPet: followerPet
            };
        } catch (error) {
            console.error('Error actualizando contadores:', error);
            throw error;
        }
    },

    // Obtener mascotas con filtros
    getPets: async (params = {}) => {
        try {
            const {
                skip = 0,
                limit = 10,
                name,
                pet_type_id,
                breed_id,
                gender,
                includeImage
            } = params;

            const queryParams = {
                skip,
                limit,
                ...(name && { name }),
                ...(pet_type_id && { pet_type_id }),
                ...(breed_id && { breed_id }),
                ...(gender && { gender }),
                ...(includeImage && { include_image: includeImage })
            };

            const response = await axiosInstance.get('/pets', {
                params: queryParams
            });
            return response.data;
        } catch (error) {
            console.error('Error obteniendo mascotas:', error);
            throw error;
        }
    }
};