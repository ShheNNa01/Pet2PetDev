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

// Sample data
const posts = [
  { id: 1, user: "CatLover", pet: "Mittens", content: "Mi gatito aprendió un nuevo truco", likes: 120, comments: 15, image: "/placeholder.svg?height=300&width=300" },
  { id: 2, user: "DogWhisperer", pet: "Firulais", content: "Paseo matutino con Firulais", likes: 89, comments: 7, image: "/placeholder.svg?height=300&width=300" },
  { id: 3, user: "BunnyMom", pet: "Fluffy", content: "¡Miren esas orejitas!", likes: 200, comments: 25, image: "/placeholder.svg?height=300&width=300" },
  { id: 4, user: "ParrotPal", pet: "Polly", content: "Hora de cantar", likes: 150, comments: 20, image: "/placeholder.svg?height=300&width=300" },
];

const newFriends = ["Max", "Luna", "Rocky", "Bella"];
const petsForAdoption = [
  { name: "Whiskers", type: "Gato", age: "2 años", image: "/placeholder.svg?height=100&width=100&text=Whiskers" },
  { name: "Buddy", type: "Perro", age: "3 años", image: "/placeholder.svg?height=100&width=100&text=Buddy" },
  { name: "Fluffy", type: "Conejo", age: "1 año", image: "/placeholder.svg?height=100&width=100&text=Fluffy" },
  { name: "Rex", type: "Iguana", age: "5 años", image: "/placeholder.svg?height=100&width=100&text=Rex" },
];

export default function HomePage() {
  const [newPost, setNewPost] = useState("");
  const [postType, setPostType] = useState("photo");

  return (
    <div className="min-h-screen bg-yellow-50 text-gray-800 font-sans">
      <Header />

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Left column - New Friends */}
          <div className="hidden md:block">
            <Card>
              <CardHeader>
                <h2 className="text-2xl font-semibold text-pink-600">Nuevos Amigos</h2>
              </CardHeader>
              <CardContent>
                <ul className="space-y-4">
                  {newFriends.map((friend) => (
                    <li key={friend} className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <Avatar>
                          <AvatarImage src={`/placeholder.svg?height=32&width=32&text=${friend}`} alt={friend} />
                          <AvatarFallback>{friend[0]}</AvatarFallback>
                        </Avatar>
                        <span>{friend}</span>
                      </div>
                      <Button size="sm" variant="outline">
                        <UserPlus className="h-4 w-4 mr-2" />
                        <span className="sr-only md:not-sr-only">Seguir</span>
                      </Button>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>

          {/* Central column - Feed of posts */}
          <div className="md:col-span-2 space-y-8">
            {/* New post area */}
            <Card>
              <CardContent className="pt-6">
                <div className="flex space-x-4">
                  <Avatar>
                    <AvatarImage src="/placeholder.svg?height=40&width=40" alt="Tu avatar" />
                    <AvatarFallback>TU</AvatarFallback>
                  </Avatar>
                  <div className="flex-grow space-y-4">
                    <Textarea
                      placeholder="¿Qué está haciendo tu peludo?"
                      value={newPost}
                      onChange={(e) => setNewPost(e.target.value)}
                      className="w-full"
                    />
                    <Input
                      placeholder="Etiquetar amigos o mascotas"
                      className="w-full"
                    />
                  </div>
                </div>
              </CardContent>
              <CardFooter className="flex justify-between">
                <Tabs defaultValue="photo" onValueChange={(value) => setPostType(value)}>
                  <TabsList>
                    <TabsTrigger value="photo">
                      <Camera className="h-4 w-4 mr-2" />
                      <span className="sr-only md:not-sr-only">Foto</span>
                    </TabsTrigger>
                    <TabsTrigger value="video">
                      <Video className="h-4 w-4 mr-2" />
                      <span className="sr-only md:not-sr-only">Video</span>
                    </TabsTrigger>
                  </TabsList>
                </Tabs>
                <Button>
                  <Send className="h-4 w-4 mr-2" />
                  <span className="sr-only md:not-sr-only">Publicar</span>
                </Button>
              </CardFooter>
            </Card>

            {/* Posts */}
            <div className="space-y-8">
              {posts.map((post) => (
                <Card key={post.id} className="overflow-hidden">
                  <CardHeader>
                    <div className="flex items-center space-x-4">
                      <Avatar>
                        <AvatarImage src={`/placeholder.svg?height=40&width=40&text=${post.pet}`} alt={post.pet} />
                        <AvatarFallback>{post.pet[0]}</AvatarFallback>
                      </Avatar>
                      <div>
                        <p className="font-semibold">{post.pet}</p>
                        <p className="text-sm text-gray-500">Publicado por {post.user}</p>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="mb-4">{post.content}</p>
                    <img src={post.image} alt="Contenido de la publicación" className="w-full rounded-lg" />
                  </CardContent>
                  <CardFooter className="flex flex-wrap justify-between gap-2">
                    <Button variant="ghost" size="sm" className="flex-1">
                      <Heart className="mr-2 h-4 w-4 text-red-500" />
                      <span className="sr-only md:not-sr-only">{post.likes}</span>
                    </Button>
                    <Button variant="ghost" size="sm" className="flex-1">
                      <MessageCircle className="mr-2 h-4 w-4 text-blue-500" />
                      <span className="sr-only md:not-sr-only">{post.comments}</span>
                    </Button>
                    <Button variant="ghost" size="sm" className="flex-1">
                      <Share2 className="mr-2 h-4 w-4 text-green-500" />
                      <span className="sr-only md:not-sr-only">Compartir</span>
                    </Button>
                    <Button variant="ghost" size="sm" className="flex-1">
                      <Gift className="mr-2 h-4 w-4 text-purple-500" />
                      <span className="sr-only md:not-sr-only">Regalo</span>
                    </Button>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="sm" className="flex-1">
                          <ExternalLink className="mr-2 h-4 w-4" />
                          <span className="sr-only md:not-sr-only">Compartir en</span>
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent>
                        <DropdownMenuItem>Facebook</DropdownMenuItem>
                        <DropdownMenuItem>Twitter</DropdownMenuItem>
                        <DropdownMenuItem>Instagram</DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </CardFooter>
                </Card>
              ))}
            </div>
          </div>

          {/* Right column - Your New Pet and Featured Posts */}
          <div className="hidden md:block space-y-8">
            <Card>
              <CardHeader>
                <h2 className="text-2xl font-semibold text-pink-600">Tu Nueva Mascota</h2>
              </CardHeader>
              <CardContent>
                <ul className="space-y-4">
                  {petsForAdoption.map((pet) => (
                    <li key={pet.name} className="flex items-center space-x-4">
                      <Avatar className="h-16 w-16">
                        <AvatarImage src={pet.image} alt={pet.name} />
                        <AvatarFallback>{pet.name[0]}</AvatarFallback>
                      </Avatar>
                      <div>
                        <p className="font-semibold">{pet.name}</p>
                        <p className="text-sm text-gray-500">{pet.type}, {pet.age}</p>
                        <Button size="sm" variant="outline" className="mt-2">
                          Conocer más
                        </Button>
                      </div>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <h2 className="text-2xl font-semibold text-pink-600">Publicaciones Destacadas</h2>
              </CardHeader>
              <CardContent>
                <ul className="space-y-4">
                  {posts.slice(0, 2).map((post) => (
                    <li key={post.id} className="flex items-center space-x-4">
                      <Avatar>
                        <AvatarImage src={`/placeholder.svg?height=40&width=40&text=${post.pet}`} alt={post.pet} />
                        <AvatarFallback>{post.pet[0]}</AvatarFallback>
                      </Avatar>
                      <div>
                        <p className="font-semibold">{post.pet}</p>
                        <p className="text-sm text-gray-500">{post.content.slice(0, 50)}...</p>
                        <div className="flex space-x-2 mt-2">
                          <Badge variant="secondary">
                            <Heart className="h-3 w-3 mr-1" /> {post.likes}
                          </Badge>
                          <Badge variant="secondary">
                            <MessageCircle className="h-3 w-3 mr-1" /> {post.comments}
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

      {/* Footer */}
      <footer className="bg-white mt-12 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-sm text-gray-500 mb-4 md:mb-0">
              © 2023 Pet2Pet. Todos los derechos reservados.
            </div>
            <div className="flex space-x-4">
              <a href="#" className="text-sm text-gray-500 hover:text-gray-700">Privacidad</a>
              <a href="#" className="text-sm text-gray-500 hover:text-gray-700">Términos</a>
              <a href="#" className="text-sm text-gray-500 hover:text-gray-700">Contacto</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
