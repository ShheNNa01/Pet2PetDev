import axiosInstance from './config/axios';

export const petService = {
    getPetTypes: async (params = {}) => {
        try {
            const { skip = 0, limit = 10 } = params;
            const response = await axiosInstance.get('/pets/types', {
                params: { skip, limit }
            });
            return response.data;
        } catch (error) {
            console.error('Error obteniendo tipos de mascotas:', error);
            throw error;
        }
    },

    getBreeds: async (params = {}) => {
        try {
            const { 
                pet_type_id,
                skip = 0, 
                limit = 10 
            } = params;
            
            const response = await axiosInstance.get('/pets/breeds', {
                params: {
                    pet_type_id,
                    skip,
                    limit
                }
            });
            return response.data;
        } catch (error) {
            console.error('Error obteniendo razas:', error);
            throw error;
        }
    },

    createPet: async (petData) => {
        try {
            if (!petData.name || !petData.birthdate || !petData.breed_id || !petData.gender) {
                throw new Error('Faltan datos requeridos para crear la mascota');
            }

            const response = await axiosInstance.post('/pets', {
                name: petData.name,
                birthdate: petData.birthdate,
                breed_id: petData.breed_id,
                gender: petData.gender
            });
            return response.data;
        } catch (error) {
            console.error('Error creando mascota:', error);
            throw error;
        }
    },

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

    updatePet: async (petId, updateData) => {
        try {
            if (!petId) throw new Error('Se requiere el ID de la mascota');
            
            const validFields = {};
            if (updateData.name) validFields.name = updateData.name;
            if (updateData.birthdate) validFields.birthdate = updateData.birthdate;
            if (updateData.gender) validFields.gender = updateData.gender;

            const response = await axiosInstance.put(`/pets/${petId}`, validFields);
            return response.data;
        } catch (error) {
            console.error('Error actualizando mascota:', error);
            throw error;
        }
    },

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

    deletePet: async (petId) => {
        try {
            if (!petId) throw new Error('Se requiere el ID de la mascota');
            await axiosInstance.delete(`/pets/${petId}`);
            return true;
        } catch (error) {
            console.error('Error eliminando mascota:', error);
            throw error;
        }
    },

    // [Actualizar los métodos de follow/unfollow según la nueva estructura]
    followPet: async (petId, followerPetId) => {
        try {
            if (!petId || !followerPetId) {
                throw new Error('Se requieren ambos IDs de mascota');
            }

            const response = await axiosInstance.post(`/pets/${petId}/follow`, {
                follower_pet_id: followerPetId
            });
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

            const response = await axiosInstance.post(`/pets/${petId}/unfollow`, {
                follower_pet_id: followerPetId
            });
            return response.data;
        } catch (error) {
            console.error('Error dejando de seguir mascota:', error);
            throw error;
        }
    },

    // [Actualizar los métodos de followers/following según la nueva estructura]
    getPetFollowers: async (petId, params = {}) => {
        try {
            if (!petId) throw new Error('Se requiere el ID de la mascota');
            
            const { skip = 0, limit = 10 } = params;
            const response = await axiosInstance.get(`/pets/${petId}/followers`, {
                params: { skip, limit }
            });
            return response.data;
        } catch (error) {
            console.error('Error obteniendo seguidores:', error);
            throw error;
        }
    },

    getPetFollowing: async (petId, params = {}) => {
        try {
            if (!petId) throw new Error('Se requiere el ID de la mascota');
            
            const { skip = 0, limit = 10 } = params;
            const response = await axiosInstance.get(`/pets/${petId}/following`, {
                params: { skip, limit }
            });
            return response.data;
        } catch (error) {
            console.error('Error obteniendo mascotas seguidas:', error);
            throw error;
        }
    },

    // [Mantener el método getPets tal cual]
    getPets: async (params = {}) => {
        try {
            const {
                skip = 0,
                limit = 10,
                name,
                pet_type_id,
                breed_id,
                gender
            } = params;

            const queryParams = {
                skip,
                limit,
                ...(name && { name }),
                ...(pet_type_id && { pet_type_id }),
                ...(breed_id && { breed_id }),
                ...(gender && { gender })
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