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

    const handleDelete = async (postId) => {
        try {
            await postService.deletePost(postId);
            // Actualiza el estado filtrando el post eliminado
            setPosts(prevPosts => prevPosts.filter(post => post.post_id !== postId));
        } catch (error) {
            console.error("Error al eliminar post:", error);
        }
    };

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
            {posts.map((post) => (
                <PostCard key={post.post_id} post={post} onDelete={() => handleDelete(post.post_id)} />
            ))}

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
