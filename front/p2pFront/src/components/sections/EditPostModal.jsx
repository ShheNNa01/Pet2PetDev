import React, { useState, useRef } from 'react';
import { Video, Camera, X, Loader2 } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../ui/dialog';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { Input } from '../ui/input';
import { postService } from '../services/PostService';
import { toast } from "../ui/use-toast";

const EditPostModal = ({ isOpen, onClose, post, onSuccess }) => {
    const [content, setContent] = useState(post?.content || '');
    const [location, setLocation] = useState(post?.location || '');
    const [files, setFiles] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [previewUrls, setPreviewUrls] = useState([]);
    const fileInputRef = useRef(null);

    // Inicializar las previsualizaciones con las imágenes existentes
    React.useEffect(() => {
        if (post?.media_urls) {
            setPreviewUrls(
                post.media_urls.map(url => {
                    // Asegurarse de que la URL sea la URL completa
                    return {
                        url: url, // Ya debería estar procesada por el servicio
                        type: url.toLowerCase().endsWith('.mp4') ? 'video/mp4' : 'image/jpeg',
                        isExisting: true
                    };
                })
            );
        } else {
            setPreviewUrls([]);
        }
        // Limpiar los archivos nuevos al abrir el modal
        setFiles([]);
    }, [post]);

    const handleFileSelect = (event) => {
        const selectedFiles = Array.from(event.target.files);
        
        try {
            selectedFiles.forEach(file => {
                postService.validateFile(file);
            });

            // Solo agregar los archivos nuevos
            setFiles(prev => [...prev, ...selectedFiles]);
            
            // Crear previsualizaciones para los archivos nuevos
            const newPreviewUrls = selectedFiles.map(file => ({
                url: URL.createObjectURL(file),
                type: file.type,
                isExisting: false
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
        const fileToRemove = previewUrls[index];
        if (!fileToRemove.isExisting) {
            // Solo revocar URL y eliminar archivo si es nuevo
            URL.revokeObjectURL(fileToRemove.url);
            setFiles(prev => prev.filter((_, i) => 
                i !== previewUrls.filter(p => !p.isExisting).findIndex((_, fi) => fi === index)
            ));
        }
        setPreviewUrls(prev => prev.filter((_, i) => i !== index));
    };

   const handleSubmit = async () => {
    if (!content.trim() && previewUrls.length === 0) {
        toast({
            variant: "destructive",
            title: "Error",
            description: "Debes incluir contenido o archivos en tu publicación"
        });
        return;
    }

    setIsLoading(true);
    let contentUpdateSuccess = false;

    try {
        // 1. Primero actualizamos contenido y ubicación
        let updatedPost = await postService.updatePost(post.post_id, {
            content: content.trim(),
            location: location.trim()
        });
        contentUpdateSuccess = true;

        // 2. Si hay archivos nuevos, intentamos subirlos uno por uno
        let mediaSuccess = true;
        if (files.length > 0) {
            for (const file of files) {
                try {
                    await postService.addMediaToPost(post.post_id, file);
                } catch (mediaError) {
                    console.error(`Error al subir archivo ${file.name}:`, mediaError);
                    mediaSuccess = false;
                    // Continuamos con el siguiente archivo
                }
            }
            
            // Mostrar mensaje según el resultado
            if (mediaSuccess) {
                toast({
                    title: "¡Éxito!",
                    description: "Publicación y archivos actualizados correctamente"
                });
            } else {
                toast({
                    variant: "warning",
                    title: "Actualización parcial",
                    description: "Se actualizó el contenido pero algunos archivos no se pudieron subir"
                });
            }
        } else if (contentUpdateSuccess) {
            toast({
                title: "¡Éxito!",
                description: "Publicación actualizada correctamente"
            });
        }

        if (onSuccess) {
            // Recargamos el post actualizado para obtener las últimas URLs de medios
            const refreshedPost = await postService.getPosts({ post_id: post.post_id });
            onSuccess(refreshedPost[0]);
        }
        onClose();
    } catch (error) {
        console.error('Error al actualizar el post:', error);
        
        if (contentUpdateSuccess) {
            // Si al menos el contenido se actualizó
            toast({
                variant: "warning",
                title: "Actualización parcial",
                description: "Se actualizó el contenido pero hubo problemas con los archivos"
            });
        } else {
            toast({
                variant: "destructive",
                title: "Error",
                description: error.message || "Error al actualizar la publicación"
            });
        }
    } finally {
        setIsLoading(false);
    }
};

    // Limpiar las URLs de previsualización al cerrar el modal
    const handleClose = () => {
        previewUrls.forEach(preview => {
            if (!preview.isExisting) {
                URL.revokeObjectURL(preview.url);
            }
        });
        onClose();
    };

    return (
        <Dialog open={isOpen} onOpenChange={handleClose}>
            <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle className="text-xl font-semibold text-gray-900 mb-4">
                        Editar publicación
                    </DialogTitle>
                </DialogHeader>

                <div className="space-y-4">
                    <div className="space-y-2">
                        <Textarea
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            placeholder="¿Qué estás pensando?"
                            className="min-h-[120px] resize-none border-gray-200 focus:border-[#509ca2] focus:ring-[#509ca2]"
                        />
                    </div>

                    <div className="space-y-2">
                        <Input
                            value={location}
                            onChange={(e) => setLocation(e.target.value)}
                            placeholder="Agrega una ubicación"
                            className="border-gray-200 focus:border-[#509ca2] focus:ring-[#509ca2]"
                        />
                    </div>

                    {/* Previsualización de medios */}
                    {previewUrls.length > 0 && (
                        <div className="grid grid-cols-2 gap-2 mt-2">
                            {previewUrls.map((preview, index) => (
                                <div key={index} className="relative group">
                                    <div className="relative rounded-lg overflow-hidden h-32">
                                        {preview.type.includes('video') ? (
                                            <video
                                                src={preview.url}
                                                className="w-full h-32 object-cover"
                                                controls
                                            />
                                        ) : (
                                            <img
                                                src={preview.url}
                                                alt={`Preview ${index + 1}`}
                                                className="w-full h-32 object-cover"
                                            />
                                        )}
                                        <Button
                                            type="button"
                                            variant="destructive"
                                            size="icon"
                                            className="absolute top-1 right-1 h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                                            onClick={() => removeFile(index)}
                                        >
                                            <X className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Botones para agregar medios */}
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
                </div>

                <div className="flex justify-end gap-3 pt-4">
                    <Button
                        variant="outline"
                        onClick={handleClose}
                        disabled={isLoading}
                        className="hover:bg-gray-100"
                    >
                        Cancelar
                    </Button>
                    <Button
                        onClick={handleSubmit}
                        disabled={isLoading || (!content.trim() && !previewUrls.length)}
                        className="bg-[#509ca2] hover:bg-[#509ca2]/90"
                    >
                        {isLoading ? (
                            <>
                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                Guardando...
                            </>
                        ) : (
                            'Guardar cambios'
                        )}
                    </Button>
                </div>
            </DialogContent>
        </Dialog>
    );
};

export default EditPostModal;