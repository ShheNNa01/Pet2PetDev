import React, { useState } from 'react';
import { usePet } from '../context/PetContext';
import { postService } from '../services/PostService';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
} from '../ui/dialog';
import { Textarea } from '../ui/textarea';
import { Button } from '../ui/button';
import { Alert, AlertDescription } from '../ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import { Share2, Repeat } from 'lucide-react';
import ShareButtons from '../common/ShareButtons'; 

export default function SharePostModal({ isOpen, onClose, post }) {
    const { currentPet } = usePet();
    const [content, setContent] = useState('');
    const [isSharing, setIsSharing] = useState(false);
    const [activeTab, setActiveTab] = useState('repost');

    const handleRepost = async (e) => {
        e.preventDefault();
        if (!currentPet?.pet_id) {
            alert('Por favor, selecciona una mascota antes de compartir');
            return;
        }
        setIsSharing(true);
        try {
            await postService.sharePost(post.post_id, {
                content: content || '',
                pet_id: currentPet.pet_id,
                original_post_id: post.post_id
            });
            onClose();
        } catch (error) {
            console.error('Error al compartir:', error);
            alert('Error al compartir la publicación');
        } finally {
            setIsSharing(false);
        }
    };

    const handleSocialShare = (platform) => {
        const postUrl = `${window.location.origin}/post/${post.post_id}`;
        const shareText = `¡Mira esta publicación de ${post.pet_name}!`;
        
        let shareUrl;
        switch (platform) {
            case 'facebook':
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(postUrl)}`;
                break;
            case 'twitter':
                shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(postUrl)}&text=${encodeURIComponent(shareText)}`;
                break;
            case 'whatsapp':
                shareUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(`${shareText} ${postUrl}`)}`;
                break;
            case 'telegram':
                shareUrl = `https://t.me/share/url?url=${encodeURIComponent(postUrl)}&text=${encodeURIComponent(shareText)}`;
                break;
            case 'linkedin':
                shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(postUrl)}`;
                break;
            case 'copy':
                navigator.clipboard.writeText(postUrl);
                alert('¡Enlace copiado al portapapeles!');
                return;
        }

        if (shareUrl) {
            window.open(shareUrl, '_blank', 'width=600,height=400');
        }
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-lg">
                <DialogHeader>
                    <DialogTitle className="text-[#d55b49] text-xl font-semibold">
                        Compartir publicación
                    </DialogTitle>
                </DialogHeader>

                <Tabs defaultValue={activeTab} className="w-full" onValueChange={setActiveTab}>
                    <TabsList className="grid w-full grid-cols-2">
                        <TabsTrigger value="repost" className="flex items-center gap-2">
                            <Repeat className="w-4 h-4" />
                            Repostear
                        </TabsTrigger>
                        <TabsTrigger value="share" className="flex items-center gap-2">
                            <Share2 className="w-4 h-4" />
                            Compartir
                        </TabsTrigger>
                    </TabsList>

                    <TabsContent value="repost">
                        <form onSubmit={handleRepost} className="space-y-6">
                            {/* Preview del post original */}
                            <div className="p-3 bg-gray-50 rounded-lg mb-4">
                                <div className="flex items-center space-x-3 mb-2">
                                    {post.pet_picture && (
                                        <img 
                                            src={post.pet_picture} 
                                            alt={post.pet_name}
                                            className="w-8 h-8 rounded-full object-cover"
                                        />
                                    )}
                                    <span className="font-medium">{post.pet_name}</span>
                                </div>
                                <p className="text-sm text-gray-600 line-clamp-2">
                                    {post.content}
                                </p>
                            </div>

                            <Textarea
                                value={content}
                                onChange={(e) => setContent(e.target.value)}
                                placeholder="¿Qué piensas sobre esta publicación? 🐾"
                                rows={4}
                                className="focus-visible:ring-[#509ca2]"
                            />

                            {!currentPet?.pet_id && (
                                <Alert variant="destructive">
                                    <AlertDescription>
                                        Por favor, selecciona una mascota antes de compartir
                                    </AlertDescription>
                                </Alert>
                            )}

                            <div className="flex justify-end gap-3">
                                <Button
                                    type="button"
                                    variant="outline"
                                    onClick={onClose}
                                    className="hover:text-[#509ca2] hover:border-[#509ca2]"
                                >
                                    Cancelar
                                </Button>
                                <Button
                                    type="submit"
                                    disabled={isSharing || !currentPet?.pet_id}
                                    className="bg-[#509ca2] hover:bg-[#d55b49] active:bg-[#509ca2]
                                    transition-colors duration-200 disabled:hover:bg-[#509ca2]"
                                >
                                    {isSharing ? 'Compartiendo...' : 'Repostear'}
                                </Button>
                            </div>
                        </form>
                    </TabsContent>

                    <TabsContent value="share">
                        <ShareButtons onShare={handleSocialShare} />
                    </TabsContent>
                </Tabs>
            </DialogContent>
        </Dialog>
    );
}