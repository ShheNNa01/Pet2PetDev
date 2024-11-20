import React, { useState } from 'react';
import { usePet } from '../context/PetContext';
import { postService } from '../services/PostService';

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

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-lg w-full p-6">
                <h2 className="text-xl font-semibold mb-4">Compartir publicación</h2>
                <form onSubmit={handleShare}>
                    <textarea
                        className="w-full border rounded-lg p-3 mb-4"
                        placeholder="Agrega un comentario a tu compartido..."
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        rows={4}
                    />
                    <div className="flex justify-end gap-2">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            disabled={isSharing || !currentPet?.pet_id}
                            className="px-4 py-2 bg-[#509ca2] text-white rounded-lg hover:bg-[#509ca2]/90 disabled:opacity-50"
                        >
                            {isSharing ? 'Compartiendo...' : 'Compartir'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}