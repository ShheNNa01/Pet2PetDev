// HomePage.jsx
import React, { useState } from 'react';
import { Video, Camera } from 'lucide-react';
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Card, CardContent, CardFooter } from "../ui/card";
import { Textarea } from "../ui/textarea";
import Header from '../layout/Header';
import Footer from '../layout/Footer';
import PostCard from '../ui/PostCard';
import ProfileSection from '../sections/ProfileSection';
import StoriesBar from '../sections/StoriesBar';
import NewFriends from '../sections/NewFriends';
import RightSidebar from '../sections/RightSidebar';

// Initial posts data
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
  // ... otros posts
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
          {/* Left column */}
          <div className="hidden lg:block lg:col-span-3 space-y-6">
            <ProfileSection />
            <NewFriends />
          </div>

          {/* Central column */}
          <div className="lg:col-span-6 space-y-8">
            <StoriesBar />
            
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

          {/* Right column */}
          <div className="hidden lg:block lg:col-span-3">
            <RightSidebar featuredPosts={posts.slice(0, 2)} />
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}