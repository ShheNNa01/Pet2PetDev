import React, { useState, useRef } from 'react';
import { Video, Camera, X, Loader2 } from 'lucide-react';
import { Button } from "../ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Card, CardContent, CardFooter } from "../ui/card";
import { Textarea } from "../ui/textarea";
import { postService } from '../services/PostService';
import { toast } from "../ui/use-toast";
import { usePet } from '../context/PetContext';
import { useAuth } from '../context/AuthContext';
import LocationPicker from '../common/LocationPicker';

export default function NewPost({ onPostCreated, activePetId, petAvatar, petName }) {
    const { currentPet } = usePet();
    const { user } = useAuth();
    const [content, setContent] = useState('');
    const [files, setFiles] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [previewUrls, setPreviewUrls] = useState([]);
    const fileInputRef = useRef(null);
    const [locationData, setLocationData] = useState(null);

    const handleFileSelect = (event) => {
        const selectedFiles = Array.from(event.target.files);

        try {
            selectedFiles.forEach(file => {
                postService.validateFile(file);
            });

            setFiles(prev => [...prev, ...selectedFiles]);

            const newPreviewUrls = selectedFiles.map(file => ({
                url: URL.createObjectURL(file),
                type: file.type
            }));

            setPreviewUrls(prev => [...prev, ...newPreviewUrls]);
        } catch (error) {
            console.error('Error al seleccionar archivo:', error);
            toast({
                variant: "destructive",
                title: "Error",
                description: error.message
            });
        }
    };

    const removeFile = (index) => {
        URL.revokeObjectURL(previewUrls[index].url);
        setPreviewUrls(prev => prev.filter((_, i) => i !== index));
        setFiles(prev => prev.filter((_, i) => i !== index));
    };

    const clearForm = () => {
        setContent('');
        setFiles([]);
        previewUrls.forEach(preview => URL.revokeObjectURL(preview.url));
        setPreviewUrls([]);
    };

    const handleLocationSelect = (data) => {
        setLocationData(data);
    };

    const handleSubmit = async () => {
        if (!currentPet?.pet_id) {
            toast({
                variant: "destructive",
                title: "Error",
                description: "Necesitas seleccionar una mascota para publicar"
            });
            return;
        }

        if (!content.trim() && files.length === 0) {
            toast({
                variant: "destructive",
                title: "Error",
                description: "Debes incluir contenido o archivos en tu publicación"
            });
            return;
        }

        setIsLoading(true);
        try {
            const postData = {
                content: content.trim(),
                location: locationData?.location_name || user?.city,
                latitude: locationData?.latitude,
                longitude: locationData?.longitude,
                pet_id: currentPet.pet_id,
                files
            };

            await postService.createPost(postData);

            toast({
                title: "¡Éxito!",
                description: "Publicación creada correctamente"
            });

            clearForm();

            if (onPostCreated) {
                onPostCreated();
            }

        } catch (error) {
            console.error('Error al crear post:', error);
            toast({
                variant: "destructive",
                title: "Error",
                description: error.response?.data?.message || "Error al crear la publicación"
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Card className="bg-white shadow-sm rounded-lg overflow-hidden">
            <CardContent className="pt-6 px-6">
                <div className="flex space-x-4 mb-4">
                    <Avatar className="h-10 w-10 rounded-full ring-2 ring-[#509ca2]/10">
                        <AvatarImage
                            src={currentPet?.pet_picture || "/placeholder.svg"}
                            alt={currentPet?.name}
                        />
                        <AvatarFallback>{currentPet?.name?.[0]?.toUpperCase()}</AvatarFallback>
                    </Avatar>
                    <div className="flex-grow space-y-3">
                        <Textarea
                            placeholder={`¿Qué está haciendo ${currentPet?.name}?`}
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            className="w-full resize-none min-h-[100px] border-0 focus:ring-0 p-0 text-sm"
                        />

                        {previewUrls.length > 0 && (
                            <div className="grid grid-cols-2 gap-2 mt-2">
                                {previewUrls.map((preview, index) => (
                                    <div key={index} className="relative">
                                        {preview.type.startsWith('video/') ? (
                                            <video
                                                src={preview.url}
                                                className="w-full h-32 object-cover rounded-lg"
                                                controls
                                            />
                                        ) : (
                                            <img
                                                src={preview.url}
                                                alt={`Preview ${index + 1}`}
                                                className="w-full h-32 object-cover rounded-lg"
                                            />
                                        )}
                                        <Button
                                            type="button"
                                            variant="destructive"
                                            size="icon"
                                            className="absolute top-1 right-1 h-6 w-6"
                                            onClick={() => removeFile(index)}
                                        >
                                            <X className="h-4 w-4" />
                                        </Button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
                <div className="mt-4">
                    <LocationPicker onLocationSelect={handleLocationSelect} />
                </div>
            </CardContent>

            <CardFooter className="flex items-center justify-between px-6 py-3 bg-gray-50">
                <div className="flex gap-2">
                    <input
                        type="file"
                        ref={fileInputRef}
                        className="hidden"
                        accept="image/*, video/*"
                        multiple
                        onChange={handleFileSelect}
                    />
                    <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="h-8 gap-2 text-sm font-normal text-[#509ca2] hover:bg-[#509ca2]/10"
                        onClick={() => fileInputRef.current?.click()}
                    >
                        <Camera className="h-4 w-4" />
                        Foto
                    </Button>
                    <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="h-8 gap-2 text-sm font-normal text-[#509ca2] hover:bg-[#509ca2]/10"
                        onClick={() => fileInputRef.current?.click()}
                    >
                        <Video className="h-4 w-4" />
                        Video
                    </Button>
                </div>

                <Button
                    type="button"
                    onClick={handleSubmit}
                    size="sm"
                    className="h-8 px-5 bg-[#509ca2] hover:bg-[#509ca2]/90 text-white rounded-full"
                    disabled={isLoading || (!content.trim() && files.length === 0)}
                >
                    {isLoading ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                        'Publicar'
                    )}
                </Button>
            </CardFooter>
        </Card>
    );
}