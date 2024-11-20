import React, { useState, useCallback } from 'react';
import { Reply, ChevronDown, ChevronUp, MoreVertical, Trash2 } from 'lucide-react';
import { Button } from "./button";
import { Avatar, AvatarFallback, AvatarImage } from "./avatar";
import CommentInput from './CommentInput';
import LikeButton from './LikeButton';

export default function Comment({
    comment,
    onLike,
    onReply,
    onDelete,
    isOwner,
    className = ''
}) {
    const [isReplying, setIsReplying] = useState(false);
    const [showReplies, setShowReplies] = useState(false);
    const [showMenu, setShowMenu] = useState(false);

    // Usar pet_id en lugar de user_id para el avatar ya que los comentarios son de mascotas
    const petInitial = comment.pet_id ? `P${comment.pet_id}` : 'P';

    const handleDelete = useCallback(async () => {
        if (window.confirm('¿Estás seguro de que quieres eliminar este comentario?')) {
            try {
                await onDelete(comment.comment_id);
                setShowMenu(false);
            } catch (error) {
                console.error('Error al eliminar comentario:', error);
                alert('No se pudo eliminar el comentario');
            }
        }
    }, [comment.comment_id, onDelete]);

    const handleReply = useCallback(async (replyData) => {
        try {
            await onReply(comment.comment_id, replyData);
            setIsReplying(false);
        } catch (error) {
            console.error('Error al responder comentario:', error);
            alert('No se pudo enviar la respuesta');
        }
    }, [comment.comment_id, onReply]);

    return (
        <div className={`space-y-2 ${className}`}>
            <div className="flex items-start gap-3">
                <Avatar className="h-8 w-8 rounded-full ring-2 ring-[#509ca2]/10">
                    <AvatarImage
                        src={`/placeholder.svg?height=32&width=32&text=${petInitial}`}
                        alt={`Mascota ${comment.pet_id}`}
                        className="rounded-full"
                    />
                    <AvatarFallback className="rounded-full">{petInitial}</AvatarFallback>
                </Avatar>

                <div className="flex-1 min-w-0">
                    <div className="space-y-1">
                        <div className="bg-[#f8f9fa] rounded-lg p-3">
                            <div className="flex justify-between items-start">
                                <div>
                                    <p className="font-medium text-sm">
                                        {comment.pet_name}
                                    </p>
                                    {comment.created_at && (
                                        <p className="text-xs text-gray-500">
                                            {new Date(comment.created_at).toLocaleDateString()}
                                        </p>
                                    )}
                                </div>

                                {isOwner && (
                                    <div className="relative">
                                        <button
                                            onClick={() => setShowMenu(!showMenu)}
                                            className="p-1 hover:bg-gray-200 rounded-full"
                                        >
                                            <MoreVertical className="h-4 w-4 text-gray-500" />
                                        </button>

                                        {showMenu && (
                                            <div className="absolute right-0 mt-1 w-32 bg-white rounded-md shadow-lg z-10 border">
                                                <button
                                                    onClick={handleDelete}
                                                    className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100 flex items-center"
                                                >
                                                    <Trash2 className="h-4 w-4 mr-2" /> Eliminar
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>

                            <p className="text-sm text-gray-600 break-words mt-1">
                                {comment.comment} {/* Cambio principal: usando comment.comment en lugar de content */}
                            </p>

                            {comment.media_urls?.length > 0 && (
                                <img
                                    src={comment.media_urls[0]}
                                    alt="Comment media"
                                    className="mt-2 max-h-40 rounded-md hover:scale-[1.02] transition-transform duration-200"
                                />
                            )}
                        </div>

                        <div className="flex items-center gap-4 px-1">
                            <LikeButton
                                count={comment.reactions_count || 0} // Cambiado de likes_count a reactions_count para mantener consistencia
                                onLike={() => onLike?.(comment.comment_id)}
                                size="small"
                            />

                            <Button
                                variant="ghost"
                                size="sm"
                                className="h-6 text-xs text-gray-600 hover:bg-[#509ca2]/10"
                                onClick={() => setIsReplying(!isReplying)}
                            >
                                <Reply className="mr-1 h-3 w-3" /> Responder
                            </Button>

                            {comment.replies?.length > 0 && (
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    className="h-6 text-xs text-gray-600 hover:bg-[#509ca2]/10"
                                    onClick={() => setShowReplies(!showReplies)}
                                >
                                    {showReplies ? (
                                        <>
                                            <ChevronUp className="mr-1 h-3 w-3" />
                                            Ocultar respuestas
                                        </>
                                    ) : (
                                        <>
                                            <ChevronDown className="mr-1 h-3 w-3" />
                                            {comment.replies.length} Respuestas
                                        </>
                                    )}
                                </Button>
                            )}
                        </div>
                    </div>

                    {isReplying && (
                        <div className="pl-5 pt-2">
                            <CommentInput
                                onSubmit={handleReply}
                                onCancel={() => setIsReplying(false)}
                                isReply
                                placeholder="Escribe una respuesta..."
                                buttonText="Responder"
                            />
                        </div>
                    )}

                    {showReplies && comment.replies?.length > 0 && (
                        <div className="pl-5 pt-3 space-y-3">
                            {comment.replies.map((reply) => (
                                <Comment
                                    key={reply.comment_id}
                                    comment={reply}
                                    onLike={onLike}
                                    onReply={onReply}
                                    onDelete={onDelete}
                                    isOwner={reply.user_id === comment.user_id}
                                    className="border-b border-gray-100 last:border-0 pb-2"
                                />
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}