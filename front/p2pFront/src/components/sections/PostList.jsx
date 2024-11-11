import React, { useState, useEffect } from 'react';
import PostCard from '../ui/PostCard';
import { postService } from '../services/PostService';
import { Button } from "../ui/button";
import { Loader2 } from 'lucide-react';

export default function PostList({ refreshTrigger }) {
    const [posts, setPosts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(0);
    const [hasMore, setHasMore] = useState(true);
    const limit = 10;

    const loadPosts = async (isInitial = false) => {
        try {
            setIsLoading(true);
            setError(null);
            const skip = isInitial ? 0 : page * limit;
            const data = await postService.getPosts({ skip, limit });
            
            // Debug: Ver estructura completa de los datos
            console.log('Posts cargados:', data);
            if (data.length > 0) {
                console.log('Ejemplo de estructura de post:', {
                    post_id: data[0].post_id,
                    content: data[0].content,
                    media_urls: data[0].media_urls,
                    files: data[0].files,
                    images: data[0].images,
                });
                
                // Debug: Ver si hay imágenes y su estructura
                if (data[0].media_urls) console.log('media_urls:', data[0].media_urls);
                if (data[0].files) console.log('files:', data[0].files);
                if (data[0].images) console.log('images:', data[0].images);
            }
            
            if (isInitial) {
                setPosts(data);
                setPage(1);
            } else {
                setPosts(prev => [...prev, ...data]);
                setPage(prev => prev + 1);
            }  
            
            setHasMore(data.length === limit);
        } catch (error) {
            setError('Error al cargar las publicaciones');
            console.error('Error loading posts:', error);
        } finally {
            setIsLoading(false);
        }
    };

    // Efecto para carga inicial
    useEffect(() => {
        loadPosts(true);
    }, []);

    // Efecto para cuando se actualiza refreshTrigger
    useEffect(() => {
        if (refreshTrigger > 0) {
            setPage(0);
            loadPosts(true);
        }
    }, [refreshTrigger]);

    if (error) {
        return (
            <div className="text-center py-8">
                <p className="text-red-500">{error}</p>
                <Button
                    onClick={() => loadPosts(true)}
                    variant="outline"
                    className="mt-4"
                >
                    Intentar de nuevo
                </Button>
            </div>
        );
    }

    return (
        <div className="space-y-8">
            {posts.map((post) => {
                // Debug: Ver datos de cada post antes de renderizar
                console.log('Renderizando post:', {
                    id: post.post_id,
                    content: post.content,
                    media: post.media_urls || post.files || post.images,
                });
                return <PostCard key={post.post_id} post={post} />;
            })}

            {isLoading && (
                <div className="flex justify-center py-4">
                    <Loader2 className="h-6 w-6 animate-spin text-[#509ca2]" />
                </div>
            )}

            {!isLoading && hasMore && (
                <div className="flex justify-center">
                    <Button
                        onClick={() => loadPosts()}
                        variant="outline"
                        className="text-[#509ca2] hover:bg-[#509ca2]/10"
                    >
                        Cargar más publicaciones
                    </Button>
                </div>
            )}
        </div>
    );
}