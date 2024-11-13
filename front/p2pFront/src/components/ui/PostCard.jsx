import React, { useState } from 'react';
import { Heart, MessageCircle, Share2, Gift, MoreVertical, Edit2, Trash2, X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { postService } from '../services/PostService';
import CommentInput from './CommentInput';
import Comment from './Comment';
import LikeButton from './LikeButton';

// Componente Modal para edición
const EditModal = ({ isOpen, onClose, post, onSave }) => {
    if (!isOpen) return null;
    const [content, setContent] = useState(post.content);
    const [files, setFiles] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async () => {
        setIsLoading(true);
        try {
            const formData = new FormData();
            formData.append('content', content);
            files.forEach(file => formData.append('files', file));
            await onSave(formData);
            onClose();
        } catch (error) {
            console.error('Error al guardar:', error);
            alert('Error al actualizar el post');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
                <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg font-semibold">Editar publicación</h3>
                    <button onClick={onClose} className="p-1 hover:bg-gray-100 rounded-full">
                        <X className="h-5 w-5" />
                    </button>
                </div>
                <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    className="w-full p-3 border rounded-lg mb-4 min-h-[100px]"
                    placeholder="¿Qué estás pensando?"
                />
                <input
                    type="file"
                    multiple
                    accept="image/*,video/*"
                    onChange={(e) => setFiles(Array.from(e.target.files))}
                    className="mb-4 w-full"
                />
                <div className="flex justify-end gap-2">
                    <button onClick={onClose} className="px-4 py-2 border rounded-lg hover:bg-gray-50" disabled={isLoading}>
                        Cancelar
                    </button>
                    <button onClick={handleSubmit} className="px-4 py-2 bg-[#509ca2] text-white rounded-lg hover:bg-[#509ca2]/90" disabled={isLoading}>
                        {isLoading ? 'Guardando...' : 'Guardar cambios'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default function PostCard({ post: initialPost, onPostDeleted }) {
    const { user } = useAuth();
    const [post, setPost] = useState(initialPost);
    const [isCommenting, setIsCommenting] = useState(false);
    const [showAllComments, setShowAllComments] = useState(false);
    const [showMenu, setShowMenu] = useState(false);
    const [isEditing, setIsEditing] = useState(false);

    // Verificar si el usuario actual es el propietario del post
    const isOwner = user?.user_id === post.user_id;

    const handleEdit = async (formData) => {
        try {
            const updatedPost = await postService.updatePost(post.post_id, formData);
            setPost(updatedPost);
            alert('Post actualizado correctamente');
        } catch (error) {
            console.error('Error al actualizar:', error);
            alert('Error al actualizar el post');
        }
    };

    const handleDelete = async () => {
        if (!window.confirm('¿Estás seguro de que quieres eliminar esta publicación?')) {
            return;
        }

        try {
            await postService.deletePost(post.post_id);
            if (onPostDeleted) {
                onPostDeleted(post.post_id);
            }
            alert('Post eliminado correctamente');
        } catch (error) {
            console.error('Error al eliminar:', error);
            alert('Error al eliminar el post');
        }
    };

    const handleLike = () => {
        setPost(prev => ({
            ...prev,
            reactions_count: prev.reactions_count + 1
        }));
    };

    const handleComment = (data) => {
        setPost(prev => ({
            ...prev,
            comments: [
                ...prev.comments,
                {
                    id: Date.now(),
                    user: "CurrentUser ",
                    content: data.content,
                    image: data.image,
                    likes: 0,
                    replies: []
                }
            ],
            comments_count: prev.comments_count + 1
        }));
        setIsCommenting(false);
    };

    const sortedComments = post.comments ? [...post.comments].sort((a, b) => b.likes - a.likes) : [];
    const displayedComments = showAllComments ? sortedComments : sortedComments.slice(0, 3);

    return (
        <div className="bg-white shadow-md rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-200">
            <div className="px-6 py-4 border-b border-gray-100">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                        <div className="h-10 w-10 rounded-full bg-[#509ca2]/10 flex items-center justify-center text-[#509ca2]">
                            {post.pet_id || 'P'}
                        </div>
                        <div>
                            <p className="font-semibold">Mascota #{post.pet_id}</p>
                            <p className="text-sm text-gray-500">Usuario #{post.user_id}</p>
                        </div>
                    </div>

                    {isOwner && (
                        <div className="relative">
                            <button onClick={() => setShowMenu(!showMenu)} className="p-2 hover:bg-gray-100 rounded-full">
                                <MoreVertical className="h-5 w-5 text-gray-500" />
                            </button>
                            {showMenu && (
                                <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border">
                                    <button onClick={() => { setIsEditing(true); setShowMenu(false); }} className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center">
                                        <Edit2 className="h-4 w-4 mr-2" /> Editar
                                    </button>
                                    <button onClick={() => { handleDelete(); setShowMenu(false); }} className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100 flex items-center">
                                        <Trash2 className="h-4 w-4 mr-2" /> Eliminar
                                    </button>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>

            <div className="px-6 py-4">
                {post.content && <p className="mb-4">{post.content}</p>}
                {post.media_urls && post.media_urls.length > 0 && (
                    <div className="grid gap-2 grid-cols-1 md:grid-cols-2">
                        {post.media_urls.map((url, index) => {
                            const normalizedUrl = url.replace(/\\/g, '/');
                            const fullUrl = normalizedUrl.startsWith('http')
                                ? normalizedUrl
                                : `${import.meta.env.VITE_API_URL}/api/v1/media/${normalizedUrl}`;

                            return url.toLowerCase().endsWith('.mp4') ? (
                                <video key={index} controls src={fullUrl} className="w-full h-64 object-cover rounded-lg" />
                            ) : (
                                <img key={index} src={fullUrl} alt={`Contenido ${index + 1}`} className="w-full h-64 object-cover rounded-lg" onError={(e) => { e.target.src = '/placeholder.svg'; }} />
                            );
                        })}
                    </div>
                )}
                {post.location && <p className="text-sm text-gray-500 mt-2">📍 {post.location}</p>}
            </div>

            <div className="px-6 py-4 border-t border-gray-100">
                <div className="flex items-center justify-between">
                    <LikeButton count={post.reactions_count} onLike={handleLike} />
                    <button onClick={() => setIsCommenting(!isCommenting)} className="flex items-center space-x-2 text-gray-500 hover:text-gray-700">
                        <MessageCircle className="h-5 w-5" /> <span>{post.comments_count}</span>
                    </button>
                    <button className="flex items-center space-x-2 text-gray-500 hover:text-gray-700">
                        <Share2 className="h-5 w-5" /> <span>Compartir</span>
                    </button>
                    <button className="flex items-center space-x-2 text-[#d55b49] hover:text-[#d55b49]/80">
                        <Gift className="h-5 w-5" /> <span>Regalar</span>
                    </button>
                </div>
                {isCommenting && <CommentInput onComment={handleComment} />}
                {displayedComments.map(comment => (
                    <Comment key={comment.id} comment={comment} />
                ))}
                {sortedComments.length > 3 && (
                    <button onClick={() => setShowAllComments(!showAllComments)} className="text-sm text-[#509ca2] mt-2">
                        {showAllComments ? 'Ver menos comentarios' : 'Ver más comentarios'}
                    </button>
                )}
            </div>

            <EditModal isOpen={isEditing} post={post} onClose={() => setIsEditing(false)} onSave={handleEdit} />
        </div>
    );
}
