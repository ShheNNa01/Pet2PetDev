import React, { useState } from 'react';
import { Heart, MessageCircle, Share2, Gift, MoreVertical, Edit2, Trash2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { usePet } from '../context/PetContext';
import { postService } from '../services/PostService';
import { useNavigate } from 'react-router-dom';
import { ImageGallery } from '../common/ImageGallery';
import { toast } from "../ui/use-toast";
import CommentInput from './CommentInput';
import Comment from './Comment';
import LikeButton from './LikeButton';
import EditPostModal from '../sections/EditPostModal';
import DeletePostModal from '../sections/DeletePostModal';
import SharePostModal from '../sections/SharePostModal';


export default function PostCard({ post: initialPost, onPostDeleted }) {
    const navigate = useNavigate();
    const { user } = useAuth();
    const { currentPet } = usePet();
    const [post, setPost] = useState(initialPost);
    const [isCommenting, setIsCommenting] = useState(false);
    const [showAllComments, setShowAllComments] = useState(false);
    const [showMenu, setShowMenu] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [isShareModalOpen, setIsShareModalOpen] = useState(false);

    const isOwner = user?.user_id === post.user_id;

    const handlePetProfileClick = () => {
        const isCurrentPet = currentPet?.pet_id === post.pet_id;
        navigate(`/petProfile?id=${post.pet_id}`, {
            state: { fromProfileSection: isCurrentPet }
        });
    };

    const handleDelete = async () => {
        setIsDeleting(true);
        try {
            await postService.deletePost(post.post_id);
            toast({
                title: "Publicación eliminada",
                description: "La publicación se ha eliminado correctamente",
            });
            if (onPostDeleted) {
                onPostDeleted(); // Sin argumentos ya que handleRefresh no espera parámetros
            }
        } catch (error) {
            console.error('Error al eliminar:', error);
            toast({
                title: "Error al eliminar",
                description: error.message || "No se pudo eliminar la publicación",
                variant: "destructive"
            });
        } finally {
            setIsDeleting(false);
            setIsDeleteModalOpen(false);
        }
    };

    const handleComment = async (commentData) => {
        if (!currentPet?.pet_id) {
            alert('Por favor, selecciona una mascota antes de comentar');
            return;
        }

        try {
            const newComment = await postService.createComment(post.post_id, {
                content: commentData.content,
                pet_id: currentPet.pet_id
            });

            setPost(prev => ({
                ...prev,
                comments: [newComment, ...prev.comments],
                comments_count: prev.comments_count + 1
            }));

            setIsCommenting(false);
        } catch (error) {
            console.error('Error al crear comentario:', error);
            alert('Error al crear el comentario');
        }
    };

    const handleDeleteComment = async (commentId) => {
        try {
            await postService.deleteComment(commentId);

            setPost(prev => ({
                ...prev,
                comments: prev.comments.filter(comment => comment.comment_id !== commentId),
                comments_count: Math.max(0, prev.comments_count - 1)
            }));
        } catch (error) {
            console.error('Error al eliminar comentario:', error);
            alert('Error al eliminar el comentario');
        }
    };

    const sortedComments = post.comments ? [...post.comments].sort((a, b) => {
        return new Date(b.created_at) - new Date(a.created_at);
    }) : [];

    const displayedComments = showAllComments ? sortedComments : sortedComments.slice(0, 3);

    // Separar videos e imágenes
    const mediaFiles = post.media_urls ? post.media_urls.reduce((acc, url) => {
        if (url.toLowerCase().endsWith('.mp4')) {
            acc.videos.push(url);
        } else {
            acc.images.push(url);
        }
        return acc;
    }, { images: [], videos: [] }) : { images: [], videos: [] };

    console.log('Post data:', post);

    return (
        <>
            <div className="bg-white shadow-md rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-200">
                {/* Header del Post */}
                <div className="px-6 py-4 border-b border-gray-100">
                    <div className="flex items-center justify-between">
                        <div
                            className="flex items-center space-x-4 cursor-pointer hover:opacity-80 transition-opacity"
                            onClick={handlePetProfileClick}
                        >
                            <div className="h-10 w-10 rounded-full bg-[#509ca2]/10 flex items-center justify-center text-[#509ca2] overflow-hidden">
                                {post.pet_picture ? (
                                    <img
                                        src={post.pet_picture}
                                        alt={`Mascota #${post.pet_id}`}
                                        className="h-full w-full object-cover"
                                    />
                                ) : (
                                    post.pet_id || 'P'
                                )}
                            </div>
                            <div>
                                <p className="font-semibold hover:text-[#509ca2] transition-colors">
                                    {post.pet_name}
                                    
                                </p>

                            </div>
                        </div>

                        {/* Menú de opciones */}
                        {isOwner && (
                            <div className="relative">
                                <button
                                    onClick={() => setShowMenu(!showMenu)}
                                    className="p-2 hover:bg-gray-100 rounded-full"
                                >
                                    <MoreVertical className="h-5 w-5 text-gray-500" />
                                </button>
                                {showMenu && (
                                    <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border">
                                        <button
                                            onClick={() => { setIsEditing(true); setShowMenu(false); }}
                                            className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center"
                                        >
                                            <Edit2 className="h-4 w-4 mr-2" /> Editar
                                        </button>
                                        <button
                                            onClick={() => { setIsDeleteModalOpen(true); setShowMenu(false); }}
                                            className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100 flex items-center"
                                        >
                                            <Trash2 className="h-4 w-4 mr-2" /> Eliminar
                                        </button>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>

                {/* Contenido del Post */}
                <div className="px-6 py-4">
                    {post.content && <p className="mb-4">{post.content}</p>}

                    {/* Galería de imágenes */}
                    {mediaFiles.images.length > 0 && (
                        <div className="mb-4">
                            <ImageGallery images={mediaFiles.images} />
                        </div>
                    )}

                    {/* Videos */}
                    {mediaFiles.videos.map((url, index) => (
                        <div key={`video-${index}`} className="mb-4">
                            <video
                                controls
                                src={url}
                                className="w-full rounded-lg"
                            />
                        </div>
                    ))}

                    {post.location && (
                        <p className="text-sm text-gray-500 mt-2">📍 {post.location}</p>
                    )}
                </div>

                {/* Acciones del Post */}
                <div className="px-6 py-4 border-t border-gray-100">
                    <div className="flex items-center justify-between">
                        <LikeButton
                            postId={post.post_id}
                            initialLikes={post.reactions_count}
                            initialPetReactionId={post.pet_reaction_id}
                        />
                        <button
                            onClick={() => {
                                if (!currentPet?.pet_id) {
                                    alert('Selecciona una mascota para comentar');
                                    return;
                                }
                                setIsCommenting(!isCommenting);
                            }}
                            className={`
                                flex items-center justify-center gap-2 text-gray-500 hover:text-[#d55b49] 
                                transition-all duration-200 min-w-[80px]
                                ${!currentPet?.pet_id ? 'cursor-not-allowed opacity-50' : ''}
                            `}
                            title={!currentPet?.pet_id ? 'Selecciona una mascota para comentar' : ''}
                        >
                            <MessageCircle className="h-5 w-5" />
                            <span>{post.comments_count}</span>
                        </button>
                        <button
                            onClick={() => setIsShareModalOpen(true)}
                            className="flex items-center justify-center gap-2 text-gray-500 hover:text-[#d55b49] transition-all duration-200 min-w-[80px]"
                        >
                            <Share2 className="h-5 w-5" />
                            <span>{post.share_count || 0}</span>
                        </button>
                    </div>

                    {/* Sección de comentarios */}
                    {isCommenting && (
                        <div className="mt-4">
                            {currentPet ? (
                                <div className="mb-2 text-sm text-gray-500">
                                    Comentando como: Mascota #{currentPet.pet_id}
                                </div>
                            ) : null}
                            <CommentInput
                                onSubmit={handleComment}
                                onCancel={() => setIsCommenting(false)}
                                postId={post.post_id}
                                disabled={!currentPet?.pet_id}
                                placeholder={
                                    currentPet?.pet_id
                                        ? "Escribe un comentario..."
                                        : "Selecciona una mascota para comentar"
                                }
                            />
                        </div>
                    )}

                    {displayedComments.length > 0 && (
                        <div className="mt-4 space-y-4">
                            {displayedComments.map(comment => (
                                <Comment
                                    key={comment.comment_id}
                                    comment={comment}
                                    onDelete={handleDeleteComment}
                                    isOwner={comment.user_id === user?.user_id}
                                />
                            ))}
                        </div>
                    )}

                    {sortedComments.length > 3 && (
                        <button
                            onClick={() => setShowAllComments(!showAllComments)}
                            className="text-sm text-[#509ca2] mt-4 hover:text-[#509ca2]/80"
                        >
                            {showAllComments ? 'Ver menos comentarios' : `Ver ${sortedComments.length - 3} comentarios más`}
                        </button>
                    )}
                </div>
            </div>

            {/* Modales */}
            <EditPostModal
                isOpen={isEditing}
                onClose={() => setIsEditing(false)}
                post={post}
                onSuccess={(updatedPost) => {
                    setPost(updatedPost);
                    setIsEditing(false);
                }}
            />

            <DeletePostModal
                isOpen={isDeleteModalOpen}
                onClose={() => setIsDeleteModalOpen(false)}
                onConfirm={handleDelete}
                isDeleting={isDeleting}
            />

            <SharePostModal
                isOpen={isShareModalOpen}
                onClose={() => setIsShareModalOpen(false)}
                post={post}
            />
        </>
    );

    
}
