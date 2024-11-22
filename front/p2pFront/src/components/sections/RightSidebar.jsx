import React, { useEffect, useState } from "react";
import { Card, CardContent, CardHeader } from "../ui/card";
import { Badge } from "../ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Heart, MessageCircle } from "lucide-react";
import { postService } from "../services/PostService";

export default function RightSidebar() {
    const [data, setData] = useState({
        trendingPosts: [],
        featuredPosts: [],
        isLoading: true,
        error: null
    });

    useEffect(() => {
        let isMounted = true;

        const loadPosts = async () => {
            try {
                setData(prev => ({ ...prev, isLoading: true, error: null }));
                
                const [trends, featured] = await Promise.all([
                    postService.fetchTrendingPosts(),
                    postService.getPosts({ featured: true })
                ]);

                if (!isMounted) return;

                // Asegurar posts únicos usando post_id
                const uniqueFeatured = [...new Map(featured.map(post => [post.post_id, post])).values()];
                const uniqueTrends = [...new Map(trends.map(trend => [trend.post_id, trend])).values()];

                setData({
                    trendingPosts: uniqueTrends,
                    featuredPosts: uniqueFeatured,
                    isLoading: false,
                    error: null
                });

            } catch (error) {
                if (!isMounted) return;
                console.error("Error al cargar los posts:", error);
                setData(prev => ({
                    ...prev,
                    error: "Error al cargar el contenido",
                    isLoading: false
                }));
            }
        };

        loadPosts();
        return () => {
            isMounted = false;
        };
    }, []);

    const { trendingPosts, featuredPosts, isLoading, error } = data;

    return (
        <div className="space-y-6">
            {/* Tendencias */}
            <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
                <CardHeader>
                    <h2 className="text-lg font-semibold text-[#d55b49]">Tendencias</h2>
                </CardHeader>
                <CardContent>
                    {isLoading ? (
                        <p className="text-gray-500 text-sm">Cargando tendencias...</p>
                    ) : error ? (
                        <p className="text-red-500 text-sm">{error}</p>
                    ) : trendingPosts.length > 0 ? (
                        <div className="space-y-4">
                            {trendingPosts.map(trend => (
                                <div key={`trend-${trend.post_id}`} className="space-y-1">
                                    <h3 className="text-sm font-semibold hover:text-[#509ca2] cursor-pointer transition-colors">
                                        {trend.tag || "Sin etiqueta"}
                                    </h3>
                                    <p className="text-xs text-gray-500">
                                        {(trend.total_interactions || 0).toLocaleString()} interacciones
                                    </p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-gray-500 text-sm">No hay tendencias disponibles.</p>
                    )}
                </CardContent>
            </Card>

            {/* Publicaciones Destacadas */}
            <Card className="bg-white shadow-md rounded-lg overflow-hidden">
                <CardHeader>
                    <h2 className="text-lg font-semibold text-[#d55b49]">Publicaciones Destacadas</h2>
                </CardHeader>
                <CardContent>
                    {isLoading ? (
                        <p className="text-gray-500 text-sm">Cargando publicaciones...</p>
                    ) : error ? (
                        <p className="text-red-500 text-sm">{error}</p>
                    ) : featuredPosts.length > 0 ? (
                        <ul className="space-y-4">
                            {featuredPosts.map(post => (
                                <li key={`featured-${post.post_id}`} className="flex items-center space-x-4 group">
                                    <Avatar className="ring-2 ring-[#509ca2]/10">
                                        <AvatarImage
                                            src={post.pet_picture || `/api/placeholder/40/40?text=${post.pet_name?.[0] || 'P'}`}
                                            alt={post.pet_name}
                                        />
                                        <AvatarFallback>{(post.pet_name || "P")[0]}</AvatarFallback>
                                    </Avatar>
                                    <div className="flex-1">
                                        <p className="font-semibold group-hover:text-[#509ca2] transition-colors">
                                            {post.pet_name}
                                        </p>
                                        <p className="text-sm text-gray-500">
                                            {(post.content || "").slice(0, 50)}...
                                        </p>
                                        <div className="flex space-x-2 mt-2">
                                            <Badge variant="secondary" className="bg-[#d55b49]/10 text-[#d55b49]">
                                                <Heart className="h-3 w-3 mr-1" /> {post.likes || 0}
                                            </Badge>
                                            <Badge variant="secondary" className="bg-[#509ca2]/10 text-[#509ca2]">
                                                <MessageCircle className="h-3 w-3 mr-1" /> {(post.comments || []).length}
                                            </Badge>
                                        </div>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="text-gray-500 text-sm">No hay publicaciones destacadas disponibles.</p>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}