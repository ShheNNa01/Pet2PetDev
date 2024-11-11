import React, { useState } from 'react';
import { Heart, MessageCircle, Share2, Gift } from 'lucide-react';
import { Button } from "./button";
import { Avatar, AvatarFallback, AvatarImage } from "./avatar";
import { Card, CardContent, CardFooter, CardHeader } from "./card";
import CommentInput from './CommentInput';
import Comment from './Comment';
import LikeButton from './LikeButton';

export default function PostCard({ post: initialPost }) {
    const [post, setPost] = useState(initialPost);
    const [isCommenting, setIsCommenting] = useState(false);
    const [showAllComments, setShowAllComments] = useState(false);

    const handleLike = () => {
        setPost(prev => ({
            ...prev,
            reactions_count: prev.reactions_count + 1
        }));
    };

    const handleCommentLike = (commentId) => {
        setPost(prev => ({
            ...prev,
            comments: prev.comments.map(comment => 
                comment.id === commentId 
                    ? { ...comment, likes: comment.likes + 1 }
                    : comment
            )
        }));
    };

    const handleReply = (commentId, data) => {
        setPost(prev => ({
            ...prev,
            comments: prev.comments.map(comment => 
                comment.id === commentId 
                    ? {
                        ...comment,
                        replies: [
                            ...(comment.replies || []),
                            {
                                id: Date.now(),
                                user: "CurrentUser ",
                                content: data.content,
                                image: data.image,
                                likes: 0
                            }
                        ]
                    }
                    : comment
            )
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

    const placeholderText = post.pet_id || 'P';

    return (
        <Card className="bg-white shadow-md rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-200">
            <CardHeader className="px-6 py-4 border-b border-gray-100">
                <div className="flex items-center space-x-4">
                    <Avatar className="ring-2 ring-[#509ca2]/10">
                        <AvatarImage src={`/placeholder.svg?height=40&width=40&text=${placeholderText}`} alt="Pet Profile" />
                        <AvatarFallback className="bg-[#509ca2]/10 text-[#509ca2]">{placeholderText}</AvatarFallback>
                    </Avatar>
                    <div>
                        <p className="font-semibold text-[#1a1a1a]">Mascota #{post.pet_id}</p>
                        <p className="text-sm text-gray-500">Usuario #{post.user_id}</p>
                    </div>
                </div>
            </CardHeader>

            <CardContent className="px-6 py-4">
                {/* Mostrar solo contenido si hay texto o media */}
                {(post.content || (post.media_urls && post.media_urls.length > 0)) && (
                    <>
                        {/* Solo muestra el contenido si hay texto */}
                        {post.content && <p className="mb-4 text-[#1a1a1a]">{post.content}</p>}

                        {/* Mostrar archivos multimedia */}
                        {post.media_urls && post.media_urls.length > 0 && (
                            <div className="relative rounded-lg overflow-hidden">
                                {post.media_urls.map((url, index) => (
                                    url.endsWith(".mp4") ? (
                                        <video 
                                            key={index}
                                            controls 
                                            src={url} 
                                            className="w-full rounded-lg transform hover:scale-[1.02] transition-transform duration-200"
                                        />
                                    ) : (
                                        <img 
                                            key={index}
                                            src={url} 
                                            alt="Contenido de la publicación" 
                                            className="w-full rounded-lg transform hover:scale-[1.02] transition-transform duration-200"
                                        />
                                    )
                                ))}
                            </div>
                        )}

                        {post.location && (
                            < p className="text-sm text-gray-500 mt-2">📍 {post.location}</p>
                        )}
                    </>
                )}
            </CardContent>

            <CardFooter className="flex flex-col items-start px-6 py-4">
                <div className="flex items-center justify-between w-full border-y border-gray-100 py-2">
                    <LikeButton 
                        count={post.reactions_count} 
                        onLike={handleLike}
                    />
                    <Button 
                        variant="ghost" 
                        size="sm" 
                        className="text-[#509ca2] hover:bg-[#509ca2]/10"
                        onClick={() => setIsCommenting(!isCommenting)}
                    >
                        <MessageCircle className="h-4 w-4 mr-2" />
                        {post.comments_count}
                    </Button>
                    <Button 
                        variant="ghost" 
                        size="sm" 
                        className="text-[#509ca2] hover:bg-[#509ca2]/10"
                    >
                        <Share2 className="h-4 w-4 mr-2" />
                        Compartir
                    </Button>
                    <Button 
                        variant="ghost" 
                        size="sm" 
                        className="text-[#d55b49] hover:bg-[#d55b49]/10"
                    >
                        <Gift className="h-4 w-4 mr-2" />
                        Regalo
                    </Button>
                </div>

                {isCommenting && (
                    <div className="w-full pt-3">
                        <CommentInput
                            onSubmit={handleComment}
                            onCancel={() => setIsCommenting(false)}
                            postId={post.post_id}
                        />
                    </div>
                )}

                {post.comments?.length > 0 && (
                    <div className="w-full pt-3 space-y-3">
                        {displayedComments.map((comment) => (
                            <Comment
                                key={comment.id || comment.comment_id} 
                                comment={comment}
                                onLike={handleCommentLike}
                                onReply={handleReply}
                                className="border-b border-gray-100 last:border-0 pb-3"
                            />
                        ))}

                        {post.comments.length > 3 && (
                            <Button
                                variant="ghost"
                                size="sm"
                                className="text-[#509ca2] hover:bg-[#509ca2]/10 text-sm px-0"
                                onClick={() => setShowAllComments(!showAllComments)}
                            >
                                {showAllComments ? (
                                    "Mostrar menos comentarios"
                                ) : (
                                    `Ver ${post.comments.length - 3} comentarios más`
                                )}
                            </Button>
                        )}
                    </div>
                )}
            </CardFooter>
        </Card>
    );
}