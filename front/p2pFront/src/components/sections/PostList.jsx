import React, { useState, useEffect, useRef, useCallback } from 'react';
import PostCard from '../ui/PostCard';
import { postService } from '../services/PostService';
import { Button } from "../ui/button";
import { Loader2 } from 'lucide-react';

export default function PostList({ refreshTrigger, onPostDeleted }) {
    const [posts, setPosts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(0);
    const [hasMore, setHasMore] = useState(true);
    const observerRef = useRef();
    const limit = 10;

    const loadPosts = useCallback(async (isInitial = false) => {
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
    }, [page]);

    const refreshPosts = useCallback(async () => {
        setPage(0);
        const data = await postService.getPosts({ skip: 0, limit });
        setPosts(data);
        setPage(1);
        setHasMore(data.length === limit);
        if (observerRef.current) {
            observerRef.current.disconnect();
        }
    }, []);

    const handleDelete = async (postId) => {
        try {
            await postService.deletePost(postId);
            setPosts(prevPosts => prevPosts.filter(post => post.post_id !== postId));
            
            console.log("Publicación eliminada, llamando a onPostDeleted"); // Debug
            if (onPostDeleted) {
                onPostDeleted();
            }
            
            await refreshPosts();
        } catch (error) {
            console.error("Error al eliminar post:", error);
        }
    };

    useEffect(() => {
        loadPosts(true);
        return () => {
            if (observerRef.current) {
                observerRef.current.disconnect();
            }
        };
    }, []);

    useEffect(() => {
        if (refreshTrigger > 0) {
            console.log("Refresh Triggered in PostList"); // Debugging
            refreshPosts();
        }
    }, [refreshTrigger, refreshPosts]);

    const lastPostRef = useCallback(node => {
        if (isLoading) return;

        if (observerRef.current) {
            observerRef.current.disconnect();
        }

        observerRef.current = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting && hasMore) {
                loadPosts();
            }
        });

        if (node) {
            observerRef.current.observe(node);
        }
    }, [isLoading, hasMore, loadPosts]);

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
            {posts.map((post, index) => (
                <div 
                    key={post.post_id}
                    ref={posts.length === index + 1 ? lastPostRef : null}
                >
                    <PostCard 
                        post={post} 
                        onDelete={() => handleDelete(post.post_id)} 
                    />
                </div>
            ))}
            {isLoading && (
                <div className="flex justify-center py-4">
                    <Loader2 className="h-6 w-6 animate-spin text-[#509ca2]" />
                </div>
            )}
        </div>
    );
}
