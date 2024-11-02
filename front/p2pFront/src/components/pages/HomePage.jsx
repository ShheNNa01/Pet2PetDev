import React, { useState } from 'react';
import { Video, Heart, MessageCircle, Share2, Send, UserPlus, Camera, Gift, ExternalLink } from 'lucide-react';
import { Button } from "../ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "../ui/dropdown-menu";
import { Input } from "../ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Card, CardContent, CardFooter, CardHeader } from "../ui/card";
import { Textarea } from "../ui/textarea";
import { Tabs, TabsList, TabsTrigger } from "../ui/tabs";
import { Badge } from "../ui/badge";
import Header from '../layout/Header';
import PostCard from '../ui/PostCard';

// Initial posts data with comments structure
const initialPosts = [
  { 
    id: 1, 
    user: "CatLover", 
    pet: "Mittens", 
    content: "Mi gatito aprendió un nuevo truco", 
    likes: 120, 
    comments: [
      { id: 1, user: "DogFan", content: "¡Qué lindo! ¿Qué truco aprendió?", likes: 15, replies: [
        { id: 11, user: "CatLover", content: "¡Aprendió a dar la pata!", likes: 8 }
      ] },
      { id: 2, user: "PetLover", content: "¡Necesitamos un video!", likes: 10, replies: [] }
    ], 
    image: "/placeholder.svg?height=300&width=300" 
  },
  { 
    id: 2, 
    user: "DogWhisperer", 
    pet: "Firulais", 
    content: "Paseo matutino con Firulais", 
    likes: 89, 
    comments: [], 
    image: "/placeholder.svg?height=300&width=300" 
  },
  { 
    id: 3, 
    user: "BunnyMom", 
    pet: "Fluffy", 
    content: "¡Miren esas orejitas!", 
    likes: 200, 
    comments: [], 
    image: "/placeholder.svg?height=300&width=300" 
  },
  { 
    id: 4, 
    user: "ParrotPal", 
    pet: "Polly", 
    content: "Hora de cantar", 
    likes: 150, 
    comments: [], 
    image: "/placeholder.svg?height=300&width=300" 
  }
];

const newFriends = ["Max", "Luna", "Rocky", "Bella"];
const petsForAdoption = [
  { name: "Whiskers", type: "Gato", age: "2 años", image: "/placeholder.svg?height=100&width=100&text=Whiskers" },
  { name: "Buddy", type: "Perro", age: "3 años", image: "/placeholder.svg?height=100&width=100&text=Buddy" },
  { name: "Fluffy", type: "Conejo", age: "1 año", image: "/placeholder.svg?height=100&width=100&text=Fluffy" },
  { name: "Rex", type: "Iguana", age: "5 años", image: "/placeholder.svg?height=100&width=100&text=Rex" },
];

export default function HomePage() {
  const [posts, setPosts] = useState(initialPosts);
  const [newPost, setNewPost] = useState("");
  const [postType, setPostType] = useState("photo");

  const handleNewPost = () => {
    if (newPost.trim() === "") return;
    
    const newPostObj = {
      id: Date.now(),
      user: "CurrentUser",
      pet: "TuMascota",
      content: newPost,
      likes: 0,
      comments: [],
      image: "/placeholder.svg?height=300&width=300&text=Nueva+Publicación"
    };

    setPosts([newPostObj, ...posts]);
    setNewPost("");
  };

  return (
    <div className="min-h-screen bg-[#eeede8] text-[#1a1a1a] font-sans">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left column - New Friends */}
          <div className="hidden lg:block lg:col-span-3">
          <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
            <CardHeader>
              <h2 className="text-[#d55b49] text-xl font-semibold">Nuevos Amigos</h2>
            </CardHeader>
            <CardContent>
              <ul className="space-y-4">
                {newFriends.map((friend) => (
                  <li key={friend} className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Avatar className="h-8 w-8">
                        <AvatarImage src={`/placeholder.svg?height=32&width=32&text=${friend[0]}`} />
                        <AvatarFallback className="bg-gray-100">
                          {friend[0]}
                        </AvatarFallback>
                      </Avatar>
                      <span className="text-sm">{friend}</span>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      className="h-7 px-3 border-[#509ca2] text-[#509ca2] hover:bg-[#509ca2]/5 text-xs font-normal"
                    >
                      <UserPlus className="h-3.5 w-3.5 mr-1.5" />
                      Seguir
                    </Button>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
          </div>

          {/* Central column - Feed */}
          <div className="lg:col-span-6 space-y-8">
            {/* New post area */}
            <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
              <CardContent className="pt-6 px-6">
                <div className="flex space-x-4 mb-4">
                  <Avatar className="h-10 w-10 rounded-full">
                    <AvatarImage src="/placeholder.svg?height=40&width=40" alt="Tu avatar" />
                    <AvatarFallback>TU</AvatarFallback>
                  </Avatar>
                  <div className="flex-grow space-y-3">
                    <Textarea
                      placeholder="¿Qué está haciendo tu peludo?"
                      value={newPost}
                      onChange={(e) => setNewPost(e.target.value)}
                      className="w-full resize-none min-h-[100px] border-0 focus:ring-0 p-0 text-sm"
                    />
                    <Input
                      placeholder="Etiquetar amigos o mascotas"
                      className="w-full border-0 focus:ring-0 text-sm text-muted-foreground"
                    />
                  </div>
                </div>
              </CardContent>
              <CardFooter className="flex items-center justify-between px-6 py-3 bg-gray-50">
              <div className="flex gap-2">
                <Button 
                  variant="ghost"
                  size="sm"
                  className={`h-8 gap-2 text-sm font-normal ${postType === 'photo' ? 'bg-[#509ca2]/10 text-[#509ca2]' : 'text-gray-600 hover:bg-gray-100'}`}
                  onClick={() => setPostType('photo')}
                >
                  <Camera className="h-4 w-4" />
                  Foto
                </Button>
                <Button 
                  variant="ghost"
                  size="sm"
                  className={`h-8 gap-2 text-sm font-normal ${postType === 'video' ? 'bg-[#509ca2]/10 text-[#509ca2]' : 'text-gray-600 hover:bg-gray-100'}`}
                  onClick={() => setPostType('video')}
                >
                  <Video className="h-4 w-4" />
                  Video
                </Button>
              </div>
                <Button
                  onClick={handleNewPost}
                  size="sm"
                  className="h-8 px-5 bg-[#509ca2] hover:bg-[#509ca2]/90 text-white rounded-full"
                >
                  Publicar
                </Button>
              </CardFooter>
            </Card>

            {/* Posts */}
            <div className="space-y-8">
              {posts.map((post) => (
                <PostCard key={post.id} post={post} />
              ))}
            </div>
          </div>

          {/* Right column - Your New Pet */}
          <div className="hidden lg:block lg:col-span-3 space-y-8">
            <Card className="bg-white shadow-md rounded-lg overflow-hidden">
              <CardHeader>
                <h2 className="text-2xl font-semibold text-[#d55b49]">Tu Nueva Mascota</h2>
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

            <Card className="bg-white shadow-md rounded-lg overflow-hidden">
              <CardHeader>
                <h2 className="text-2xl font-semibold text-[#d55b49]">Publicaciones Destacadas</h2>
              </CardHeader>
              <CardContent>
                <ul className="space-y-4">
                  {posts.slice(0, 2).map((post) => (
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
        </div>
      </main>

      <footer className="bg-white mt-12 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-sm text-gray-500 mb-4 md:mb-0">
              © 2024 Pet2Pet. Todos los derechos reservados.
            </div>
            <div className="flex space-x-4">
              <a href="#" className="text-sm text-gray-500 hover:text-[#509ca2]">
                Privacidad
              </a>
              <a href="#" className="text-sm text-gray-500 hover:text-[#509ca2]">
                Términos
              </a>
              <a href="#" className="text-sm text-gray-500 hover:text-[#509ca2]">
                Contacto
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}