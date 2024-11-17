import axiosInstance, { getMediaUrl, BASE_URL } from './config/axios';

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB en bytes

export const postService = {
    getPosts: async (params = {}) => {
        try {
            const response = await axiosInstance.get('/posts/', {
                params: {
                    ...params
                }
            });

            // Solo procesamos las URLs de las imágenes, dejamos los comentarios tal cual vienen
            const processedPosts = response.data.map(post => ({
                ...post,
                media_urls: post.media_urls ? post.media_urls.map(url => getMediaUrl(url)) : []
            }));

            return processedPosts;
        } catch (error) {
            console.error('Error obteniendo posts:', error);
            throw error;
        }
    },

    getPostById: async (postId) => {
        try {
            const response = await axiosInstance.get(`/posts/${postId}`);
            
            return {
                ...response.data,
                media_urls: response.data.media_urls ? 
                    response.data.media_urls.map(url => getMediaUrl(url)) : 
                    []
            };
        } catch (error) {
            console.error('Error obteniendo post:', error);
            throw error;
        }
    },

    createPost: async (postData) => {
        try {
            const formData = new FormData();
            formData.append('content', postData.content || '');
            formData.append('location', postData.location || '');
            formData.append('pet_id', postData.pet_id);

            if (postData.files && postData.files.length > 0) {
                postData.files.forEach(file => {
                    formData.append('files', file);
                });
            }

            const response = await axiosInstance.post('/posts/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            // Procesar las URLs de las imágenes en la respuesta
            if (response.data.media_urls) {
                response.data.media_urls = response.data.media_urls.map(url => 
                    getMediaUrl(url)
                );
            }

            return response.data;
        } catch (error) {
            console.error('Error al crear post:', error);
            throw error;
        }
    },

    // Método específico para subir un archivo
    addMediaToPost: async (postId, file) => {
        try {
            const mediaFormData = new FormData();
            mediaFormData.append('file', file);
    
            const response = await axiosInstance.post(
                `/posts/${postId}/media`,
                mediaFormData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            );
    
            return response.data;
        } catch (error) {
            console.error('Error al subir archivo:', error);
            throw new Error(`Error al subir el archivo ${file.name}`);
        }
    },

    updatePost: async (postId, postData) => {
        try {
            // 1. Primero actualizar solo content y location con PUT
            const response = await axiosInstance.put(`/posts/${postId}`, {
                content: postData.content || '',
                location: postData.location || ''
            });

            let updatedPost = response.data;

            // 2. Si hay archivos nuevos, subir cada uno usando addMediaToPost
            if (postData.files && postData.files.length > 0) {
                for (const file of postData.files) {
                    try {
                        const mediaResponse = await postService.addMediaToPost(postId, file);
                        // Actualizar las URLs
                        updatedPost.media_urls = [
                            ...(updatedPost.media_urls || []),
                            ...mediaResponse.media_urls
                        ];
                    } catch (mediaError) {
                        console.error(`Error al subir archivo ${file.name}:`, mediaError);
                        throw mediaError;
                    }
                }
            }

            // Procesar todas las URLs al final
            return {
                ...updatedPost,
                media_urls: updatedPost.media_urls ? 
                    updatedPost.media_urls.map(url => getMediaUrl(url)) : 
                    []
            };
        } catch (error) {
            console.error('Error al actualizar post:', error);
            throw error;
        }
    },


    deletePost: async (postId) => {
        try {
            await axiosInstance.delete(`/posts/${postId}`);
        } catch (error) {
            console.error('Error al eliminar post:', error);
            throw error;
        }
    },

    validateFile: (file) => {
        if (!file) {
            throw new Error('Archivo no válido');
        }

        if (file.size > MAX_FILE_SIZE) {
            throw new Error(`El archivo ${file.name} excede el límite de 5MB`);
        }

        const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4'];
        if (!validTypes.includes(file.type)) {
            throw new Error(`El archivo ${file.name} no es un tipo válido. Se permiten jpg, png, gif y mp4`);
        }

        return true;
    },

    getMyPosts: async (params = {}) => {
        try {
            const { skip = 0, limit = 10, pet_id } = params;
            
            const queryParams = {
                skip,
                limit,
                ...(pet_id && { pet_id }) // Incluir pet_id solo si está definido
            };

            const response = await axiosInstance.get('/posts/my-posts', {
                params: queryParams
            });

            // Procesar las URLs de las imágenes
            const processedPosts = response.data.map(post => ({
                ...post,
                media_urls: post.media_urls ? post.media_urls.map(url => getMediaUrl(url)) : []
            }));

            return processedPosts;
        } catch (error) {
            console.error('Error obteniendo mis posts:', error);
            throw error;
        }
    },
    createComment: async (postId, commentData) => {
        try {
            const response = await axiosInstance.post(`/posts/${postId}/comments`, {
                comment: commentData.content,
                pet_id: commentData.pet_id
            });
            return response.data;
        } catch (error) {
            console.error('Error al crear comentario:', error);
            throw error;
        }
    },

    deleteComment: async (commentId) => {
        try {
            await axiosInstance.delete(`/posts/comments/${commentId}`);
            return true;
        } catch (error) {
            console.error('Error al eliminar comentario:', error);
            throw error;
        }
    },

    createReaction: async (postId, petId) => {
        try {
            const response = await axiosInstance.post(`/posts/${postId}/reactions`, {
                reaction_type: "like",
                pet_id: petId
            });
            return response.data;
        } catch (error) {
            console.error('Error al crear reacción:', error);
            throw error;
        }
    },
    
    deleteReaction: async (reactionId) => {
        try {
            await axiosInstance.delete(`/posts/reactions/${reactionId}`);
            return true;
        } catch (error) {
            console.error('Error al eliminar reacción:', error);
            throw error;
        }
    },
    
    toggleReaction: async (postId, existingReactionId = null, petId) => {
        try {
            if (existingReactionId) {
                // Si ya existe una reacción, la eliminamos
                await postService.deleteReaction(existingReactionId);
                return { liked: false, reactionId: null };
            } else {
                // Si no existe una reacción, la creamos
                const response = await postService.createReaction(postId, petId);
                return { 
                    liked: true, 
                    reactionId: response.reaction_id 
                };
            }
        } catch (error) {
            console.error('Error al toggle reacción:', error);
            throw error;
        }
    }
    
};
