import React, { useState } from 'react';
import { Reply, ChevronDown, ChevronUp } from 'lucide-react';
import { Button } from "./button";
import { Avatar, AvatarFallback, AvatarImage } from "./avatar";
import CommentInput from './CommentInput';
import LikeButton from './LikeButton';

export default function Comment({ comment, onLike, onReply, className = '' }) {
    const [isReplying, setIsReplying] = useState(false);
    const [showReplies, setShowReplies] = useState(false);

    const userInitial = comment.user_id ? `U${comment.user_id}` : 'U';

    return (
        <div className={`space-y-2 ${className}`}>
            <div className="flex items-start gap-3">
                <div className="flex-shrink-0">
                    <Avatar className="h-8 w-8 rounded-full ring-2 ring-[#509ca2]/10">
                        <AvatarImage 
                            src={`/placeholder.svg?height=32&width=32&text=${userInitial}`} 
                            alt={`Usuario ${comment.user_id}`}
                            className="rounded-full"
                        />
                        <AvatarFallback className="rounded-full">{userInitial}</AvatarFallback>
                    </Avatar>
                </div>

                <div className="flex-1 min-w-0">
                    <div className="space-y-1">
                        <div className="bg-[#f8f9fa] rounded-lg p-3">
                            <div className="mb-1">
                                <p className="font-medium text-sm">Usuario #{comment.user_id}</p>
                                {comment.created_at && (
                                    <p className="text-xs text-gray-500">
                                        {new Date(comment.created_at).toLocaleDateString()}
                                    </p>
                                )}
                            </div>
                            <p className="text-sm text-gray-600 break-words">{comment.content}</p>
                            {comment.media_urls?.length > 0 && (
                                <img 
                                    src={comment.media_urls[0]} 
                                    alt="Comment" 
                                    className="mt-2 max-h-40 rounded-md hover:scale-[1.02] transition-transform duration-200" 
                                />
                            )}
                        </div>

                        <div className="flex items-center gap-4 px-1">
                            <LikeButton 
                                count={comment.likes_count || 0} 
                                onLike={() => onLike(comment.comment_id || comment.id)}
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
                                            <ChevronUp className="mr-1 h-3 w-3" /> Ocultar respuestas
                                        </>
                                    ) : (
                                        <>
                                            <ChevronDown className="mr-1 h-3 w-3" /> {comment.replies.length} Respuestas
                                        </>
                                    )}
                                </Button>
                            )}
                        </div>
                    </div>

                    {isReplying && (
                        <div className="pl-5 pt-2">
                            <CommentInput
                                onSubmit={(data) => {
                                    onReply(comment.comment_id || comment.id, data);
                                    setIsReplying(false);
                                }}
                                onCancel={() => setIsReplying(false)}
                                isReply
                            />
                        </div>
                    )}

                    {showReplies && comment.replies?.length > 0 && (
                        <div className="pl-5 pt-3 space-y-3">
                            {comment.replies.map((reply) => (
                                <Comment
                                    key={reply.id || reply.comment_id} // Se asegura de que cada respuesta tenga un `key` único
                                    comment={reply}
                                    onLike={onLike}
                                    onReply={onReply}
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
