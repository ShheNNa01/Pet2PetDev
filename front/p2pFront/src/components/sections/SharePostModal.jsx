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

export default function SharePostModal({ isOpen, onClose, post }) {
    const { currentPet } = usePet();
    const [content, setContent] = useState('');
    const [isSharing, setIsSharing] = useState(false);

    const handleShare = async (e) => {
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

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-lg">
                <DialogHeader>
                    <DialogTitle className="text-[#d55b49] text-xl font-semibold">
                        Compartir publicación
                    </DialogTitle>
                </DialogHeader>

                <form onSubmit={handleShare} className="space-y-6">
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
                            {isSharing ? 'Compartiendo...' : 'Compartir'}
                        </Button>
                    </div>
                </form>
            </DialogContent>
        </Dialog>
    );
}