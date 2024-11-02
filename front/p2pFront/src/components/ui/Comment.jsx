    // Comment.jsx
    import React, { useState } from 'react';
    import { Heart, Reply, ChevronDown, ChevronUp } from 'lucide-react';
    import { Button } from "./button";
    import { Avatar, AvatarFallback, AvatarImage } from "./avatar";
    import { Textarea } from "./textarea";

    export default function Comment({ comment, onLike, onReply }) {
    const [isReplying, setIsReplying] = useState(false);
    const [showReplies, setShowReplies] = useState(false);
    const [replyContent, setReplyContent] = useState('');

    const handleSubmitReply = () => {
        if (replyContent.trim()) {
        onReply(comment.id, { content: replyContent });
        setReplyContent('');
        setIsReplying(false);
        }
    };

    return (
        <div className="space-y-2">
        <div className="flex items-start gap-3">
            {/* Avatar a la izquierda */}
            <div className="flex-shrink-0">
            <Avatar className="h-8 w-8 rounded-full">
                <AvatarImage 
                src={`/placeholder.svg?height=32&width=32&text=${comment.user[0]}`} 
                alt={comment.user}
                />
                <AvatarFallback>{comment.user[0]}</AvatarFallback>
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
                    <img src={comment.image} alt="Comment" className="mt-2 max-h-40 rounded-md" />
                )}
                </div>

                {/* Botones de acción */}
                <div className="flex items-center gap-4 px-1">
                <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={() => onLike(comment.id)}
                    className="h-6 text-xs text-gray-500 hover:text-[#d55b49] p-0"
                >
                    <Heart className="h-3 w-3 mr-1" />
                    {comment.likes}
                </Button>
                <Button 
                    variant="ghost" 
                    size="sm" 
                    className="h-6 text-xs text-gray-500 hover:text-[#509ca2] p-0"
                    onClick={() => setIsReplying(!isReplying)}
                >
                    Responder
                </Button>
                {comment.replies?.length > 0 && (
                    <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowReplies(!showReplies)}
                    className="h-6 text-xs text-[#509ca2] p-0"
                    >
                    {showReplies ? "Ocultar respuestas" : `Ver ${comment.replies.length} respuestas`}
                    </Button>
                )}
                </div>
            </div>

            {/* Área de respuesta */}
            {isReplying && (
                <div className="mt-2 space-y-2">
                <Textarea
                    placeholder="Escribe una respuesta..."
                    value={replyContent}
                    onChange={(e) => setReplyContent(e.target.value)}
                    className="min-h-[80px] resize-none border-[#509ca2]/20 focus:border-[#509ca2] focus:ring-[#509ca2] text-sm"
                />
                <div className="flex justify-end gap-2">
                    <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setIsReplying(false)}
                    className="h-8 text-sm"
                    >
                    Cancelar
                    </Button>
                    <Button
                    size="sm"
                    onClick={handleSubmitReply}
                    className="h-8 bg-[#509ca2] hover:bg-[#509ca2]/90 text-white"
                    >
                    Responder
                    </Button>
                </div>
                </div>
            )}

            {/* Respuestas */}
            {showReplies && comment.replies?.length > 0 && (
                <div className="mt-2 space-y-2">
                {comment.replies.map(reply => (
                    <div key={reply.id} className="flex items-start gap-2">
                    <Avatar className="h-6 w-6 rounded-full flex-shrink-0">
                        <AvatarImage 
                        src={`/placeholder.svg?height=24&width=24&text=${reply.user[0]}`} 
                        alt={reply.user}
                        />
                        <AvatarFallback>{reply.user[0]}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                        <div className="bg-[#f8f9fa] rounded-lg p-2">
                        <p className="font-medium text-xs mb-0.5">{reply.user}</p>
                        <p className="text-xs text-gray-600 break-words">{reply.content}</p>
                        {reply.image && (
                            <img src={reply.image} alt="Reply" className="mt-2 max-h-32 rounded-md" />
                        )}
                        </div>
                        <Button 
                        variant="ghost" 
                        size="sm" 
                        onClick={() => onLike(reply.id)}
                        className="h-5 text-xs text-gray-500 hover:text-[#d55b49] mt-0.5 p-0"
                        >
                        <Heart className="h-3 w-3 mr-1" />
                        {reply.likes}
                        </Button>
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