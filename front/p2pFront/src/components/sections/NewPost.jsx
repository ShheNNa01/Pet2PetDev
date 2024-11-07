// components/sections/NewPost.jsx
import React from 'react';
import { Video, Camera } from 'lucide-react';
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Card, CardContent, CardFooter } from "../ui/card";
import { Textarea } from "../ui/textarea";

export default function NewPost({ newPost, setNewPost, postType, setPostType, onSubmit }) {
    return (
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
            onClick={onSubmit}
            size="sm"
            className="h-8 px-5 bg-[#509ca2] hover:bg-[#509ca2]/90 text-white rounded-full"
            >
            Publicar
            </Button>
        </CardFooter>
        </Card>
    );
}