// components/sections/RightSidebar.jsx
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Heart, MessageCircle } from 'lucide-react';

const petsForAdoption = [
    { name: "Whiskers", type: "Gato", age: "2 años", image: "/placeholder.svg?height=100&width=100&text=Whiskers" },
    { name: "Buddy", type: "Perro", age: "3 años", image: "/placeholder.svg?height=100&width=100&text=Buddy" },
    { name: "Fluffy", type: "Conejo", age: "1 año", image: "/placeholder.svg?height=100&width=100&text=Fluffy" },
    { name: "Rex", type: "Iguana", age: "5 años", image: "/placeholder.svg?height=100&width=100&text=Rex" },
];

const trending = [
    { id: 1, tag: "#PerritosJuguetones", count: 1234 },
    { id: 2, tag: "#GatitosDorados", count: 987 },
    { id: 3, tag: "#MascotasFelices", count: 765 },
];

export default function RightSidebar({ featuredPosts = [] }) {
    return (
        <div className="space-y-6">
        {/* Tendencias */}
        <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
            <CardHeader>
            <h2 className="text-lg font-semibold text-[#d55b49]">Tendencias</h2>
            </CardHeader>
            <CardContent>
            <div className="space-y-4">
                {trending.map((trend) => (
                <div key={trend.id} className="space-y-1">
                    <h3 className="text-sm font-semibold hover:text-[#509ca2] cursor-pointer transition-colors">
                    {trend.tag}
                    </h3>
                    <p className="text-xs text-gray-500">
                    {trend.count.toLocaleString()} publicaciones
                    </p>
                </div>
                ))}
            </div>
            </CardContent>
        </Card>

        {/* Tu Nueva Mascota */}
        <Card className="bg-white shadow-md rounded-lg overflow-hidden">
            <CardHeader>
            <h2 className="text-lg font-semibold text-[#d55b49]">Tu Nueva Mascota</h2>
            </CardHeader>
            <CardContent>
            <ul className="space-y-4">
                {petsForAdoption.map((pet) => (
                <li key={pet.name} className="group">
                    <div className="flex items-center space-x-4">
                    <Avatar className="h-16 w-16 ring-2 ring-[#509ca2]/10">
                        <AvatarImage src={pet.image} alt={pet.name} />
                        <AvatarFallback>{pet.name[0]}</AvatarFallback>
                    </Avatar>
                    <div>
                        <p className="font-semibold group-hover:text-[#509ca2] transition-colors">
                        {pet.name}
                        </p>
                        <p className="text-sm text-gray-500">{pet.type}, {pet.age}</p>
                        <Button 
                        size="sm" 
                        variant="outline" 
                        className="mt-2 text-[#509ca2] border-[#509ca2] hover:bg-[#509ca2]/10"
                        >
                        Conocer más
                        </Button>
                    </div>
                    </div>
                </li>
                ))}
            </ul>
            </CardContent>
        </Card>

        {/* Publicaciones Destacadas */}
        <Card className="bg-white shadow-md rounded-lg overflow-hidden">
            <CardHeader>
            <h2 className="text-lg font-semibold text-[#d55b49]">Publicaciones Destacadas</h2>
            </CardHeader>
            <CardContent>
            <ul className="space-y-4">
                {featuredPosts.map((post) => (
                <li key={post.id} className="flex items-center space-x-4 group">
                    <Avatar className="ring-2 ring-[#509ca2]/10">
                    <AvatarImage src={`/placeholder.svg?height=40&width=40&text=${post.pet}`} alt={post.pet} />
                    <AvatarFallback>{post.pet[0]}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                    <p className="font-semibold group-hover:text-[#509ca2] transition-colors">
                        {post.pet}
                    </p>
                    <p className="text-sm text-gray-500">{post.content.slice(0, 50)}...</p>
                    <div className="flex space-x-2 mt-2">
                        <Badge 
                        variant="secondary"
                        className="bg-[#d55b49]/10 text-[#d55b49]"
                        >
                        <Heart className="h-3 w-3 mr-1" /> {post.likes}
                        </Badge>
                        <Badge 
                        variant="secondary"
                        className="bg-[#509ca2]/10 text-[#509ca2]"
                        >
                        <MessageCircle className="h-3 w-3 mr-1" /> {post.comments.length}
                        </Badge>
                    </div>
                    </div>
                </li>
                ))}
            </ul>
            </CardContent>
        </Card>
        </div>
    );
}