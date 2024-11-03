    // Comment.jsx
    import React, { useState } from 'react';
    import { Reply, ChevronDown, ChevronUp } from 'lucide-react';
    import { Button } from "./button";
    import { Avatar, AvatarFallback, AvatarImage } from "./avatar";
    import CommentInput from './CommentInput';
    import LikeButton from './LikeButton';

    export default function Comment({ comment, onLike, onReply }) {
    const [isReplying, setIsReplying] = useState(false);
    const [showReplies, setShowReplies] = useState(false);

    return (
        <div className="space-y-2">
        <div className="flex items-start gap-3">
            {/* Avatar a la izquierda */}
            <div className="flex-shrink-0">
            <Avatar className="h-8 w-8 rounded-full ring-2 ring-[#509ca2]/10">
                <AvatarImage 
                src={`/placeholder.svg?height=32&width=32&text=${comment.user[0]}`} 
                alt={comment.user}
                className="rounded-full"
                />
                <AvatarFallback className="rounded-full">{comment.user[0]}</AvatarFallback>
            </Avatar>
            </div>

            {/* Contenido principal */}
            <div className="flex-1 min-w-0">
            <div className="space-y-1">
                {/* Información del usuario y contenido */}
                <div className="bg-[#f8f9fa] rounded-lg p-3">
                <div className="mb-1">
                    <p className="font-medium text-sm">{comment.user}</p>
                </div>
                <p className="text-sm text-gray-600 break-words">{comment.content}</p>
                {comment.image && (
                    <img 
                    src={comment.image} 
                    alt="Comment" 
                    className="mt-2 max-h-40 rounded-md hover:scale-[1.02] transition-transform duration-200" 
                    />
                )}
                </div>

                {/* Botones de acción */}
                <div className="flex items-center gap-4 px-1">
                <LikeButton 
                    count={comment.likes} 
                    onLike={() => onLike(comment.id)}
                    size="small"
                />
                <Button 
                    variant="ghost" 
                    size="sm" 
                    className="h-6 text-xs font-medium text-gray-500 hover:text-[#509ca2] p-0"
                    onClick={() => setIsReplying(!isReplying)}
                >
                    <Reply className="h-3 w-3 mr-1" />
                    Responder
                </Button>
                {comment.replies?.length > 0 && (
                    <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowReplies(!showReplies)}
                    className="h-6 text-xs font-medium text-[#509ca2] p-0 hover:text-[#509ca2]/80"
                    >
                    {showReplies ? (
                        <>
                        <ChevronUp className="h-3 w-3 mr-1" />
                        Ocultar respuestas
                        </>
                    ) : (
                        <>
                        <ChevronDown className="h-3 w-3 mr-1" />
                        Ver {comment.replies.length} {comment.replies.length === 1 ? 'respuesta' : 'respuestas'}
                        </>
                    )}
                    </Button>
                )}
                </div>
            </div>

            {/* Área de respuesta usando CommentInput */}
            {isReplying && (
                <div className="mt-2 border-l-2 border-[#509ca2]/20 pl-4">
                <CommentInput
                    onSubmit={(data) => {
                    onReply(comment.id, data);
                    setIsReplying(false);
                    }}
                    onCancel={() => setIsReplying(false)}
                    placeholder="Escribe una respuesta..."
                    buttonText="Responder"
                    isReply={true}
                />
                </div>
            )}

            {/* Respuestas */}
            {showReplies && comment.replies?.length > 0 && (
                <div className="mt-2 space-y-2 border-l-2 border-[#509ca2]/20 pl-4">
                {comment.replies.map(reply => (
                    <div key={reply.id} className="flex items-start gap-2 group">
                    <Avatar className="h-6 w-6 rounded-full flex-shrink-0 ring-2 ring-[#509ca2]/10">
                        <AvatarImage 
                        src={`/placeholder.svg?height=24&width=24&text=${reply.user[0]}`} 
                        alt={reply.user}
                        className="rounded-full"
                        />
                        <AvatarFallback className="rounded-full">{reply.user[0]}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                        <div className="bg-[#f8f9fa] rounded-lg p-2 group-hover:bg-[#f8f9fa]/80 transition-colors duration-200">
                        <p className="font-medium text-xs mb-0.5">{reply.user}</p>
                        <p className="text-xs text-gray-600 break-words">{reply.content}</p>
                        {reply.image && (
                            <img 
                            src={reply.image} 
                            alt="Reply" 
                            className="mt-2 max-h-32 rounded-md hover:scale-[1.02] transition-transform duration-200" 
                            />
                        )}
                        </div>
                        <div className="mt-1">
                        <LikeButton 
                            count={reply.likes} 
                            onLike={() => onLike(reply.id)}
                            size="small"
                        />
                        </div>
                    </div>
                    </div>
                ))}
                </div>
            )}
            </div>
        </div>
        </div>
    );
    }