import React, { useEffect, useState } from "react";
import { Card, CardContent, CardHeader } from "../ui/card";
import { Badge } from "../ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Heart, MessageCircle } from "lucide-react";
import { postService } from "../services/PostService";

export default function RightSidebar() {
    const [trendingPosts, setTrendingPosts] = useState([]);
    const [featuredPosts, setFeaturedPosts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadPosts = async () => {
            try {
                setIsLoading(true);
                
                // Cargar tendencias
                console.log('Cargando trending posts...');
                const trends = await postService.fetchTrendingPosts();
                console.log('Trending posts recibidos:', trends);
                setTrendingPosts(trends || []);

                // Cargar posts destacados
                console.log('Cargando featured posts...');
                // Asumiendo que usamos getPosts con un parámetro para filtrar destacados
                const featured = await postService.getPosts({ featured: true });
                console.log('Featured posts recibidos:', featured);
                setFeaturedPosts(featured || []);

            } catch (error) {
                console.error("Error al cargar los posts:", error);
                setError("Error al cargar el contenido");
            } finally {
                setIsLoading(false);
            }
        };

        loadPosts();
    }, []);

    // Log para ver el estado actual
    console.log('Estado actual:', {
        trendingPosts,
        featuredPosts,
        isLoading,
        error
    });

    return (
        <div className="space-y-6">
            {/* Tendencias */}
            <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
                <CardHeader>
                    <h2 className="text-lg font-semibold text-[#d55b49]">Tendencias</h2>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {isLoading ? (
                            <p className="text-gray-500 text-sm">Cargando tendencias...</p>
                        ) : error ? (
                            <p className="text-red-500 text-sm">{error}</p>
                        ) : trendingPosts.length > 0 ? (
                            trendingPosts.map((trend, index) => (
                                <div key={trend.id || index} className="space-y-1">
                                    <h3 className="text-sm font-semibold hover:text-[#509ca2] cursor-pointer transition-colors">
                                        {trend.tag || "Sin etiqueta"}
                                    </h3>
                                    <p className="text-xs text-gray-500">
                                        {(trend.total_interactions || 0).toLocaleString()} interacciones
                                    </p>
                                </div>
                            ))
                        ) : (
                            <p className="text-gray-500 text-sm">No hay tendencias disponibles.</p>
                        )}
                    </div>
                </CardContent>
            </Card>

            {/* Publicaciones Destacadas */}
            <Card className="bg-white shadow-md rounded-lg overflow-hidden">
                <CardHeader>
                    <h2 className="text-lg font-semibold text-[#d55b49]">Publicaciones Destacadas</h2>
                </CardHeader>
                <CardContent>
                    <ul className="space-y-4">
                        {isLoading ? (
                            <p className="text-gray-500 text-sm">Cargando publicaciones...</p>
                        ) : error ? (
                            <p className="text-red-500 text-sm">{error}</p>
                        ) : featuredPosts.length > 0 ? (
                            featuredPosts.map((post) => (
                                <li key={post.id} className="flex items-center space-x-4 group">
                                    <Avatar className="ring-2 ring-[#509ca2]/10">
                                        <AvatarImage
                                            src={post.pet?.avatar || `/placeholder.svg?height=40&width=40&text=${post.pet_name || 'P'}`}
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
                                            <Badge
                                                variant="secondary"
                                                className="bg-[#d55b49]/10 text-[#d55b49]"
                                            >
                                                <Heart className="h-3 w-3 mr-1" /> {post.likes || 0}
                                            </Badge>
                                            <Badge
                                                variant="secondary"
                                                className="bg-[#509ca2]/10 text-[#509ca2]"
                                            >
                                                <MessageCircle className="h-3 w-3 mr-1" /> {(post.comments || []).length}
                                            </Badge>
                                        </div>
                                    </div>
                                </li>
                            ))
                        ) : (
                            <p className="text-gray-500 text-sm">No hay publicaciones destacadas disponibles.</p>
                        )}
                    </ul>
                </CardContent>
            </Card>
        </div>
    );
}