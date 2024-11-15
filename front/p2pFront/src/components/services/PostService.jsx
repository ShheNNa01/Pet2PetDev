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

            // Procesar las URLs de las imágenes
            const processedPosts = response.data.map(post => {
                console.log('Post original:', post);
                return {
                    ...post,
                    media_urls: post.media_urls ? post.media_urls.map(url => {
                        console.log('URL original:', url);
                        const processedUrl = getMediaUrl(url);
                        console.log('URL procesada:', processedUrl);
                        return processedUrl;
                    }) : []
                };
            });

            return processedPosts;
        } catch (error) {
            console.error('Error obteniendo posts:', error);
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

    updatePost: async (postId, postData) => {
        try {
            const formData = new FormData();

            if (postData.content) {
                formData.append('content', postData.content);
            }

            if (postData.files) {
                postData.files.forEach(file => {
                    formData.append('files', file);
                });
            }

            const response = await axiosInstance.put(`/posts/${postId}`, formData, {
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
};
