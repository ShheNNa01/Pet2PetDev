// components/ui/CommentInput.jsx
import React, { useState } from 'react';
import { Image as ImageIcon, X } from 'lucide-react';
import { Button } from "./button";
import { Input } from "./input";
import { Textarea } from "./textarea";

export default function CommentInput({
    onSubmit,
    onCancel,
    placeholder = "Escribe un comentario...",
    buttonText = "Comentar",
    isReply = false,
    postId
}) {
    const [content, setContent] = useState('');
    const [image, setImage] = useState(null);
    const inputId = React.useId();

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImage(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleSubmit = () => {
        if (content.trim() || image) {
            onSubmit({ 
                content, 
                image,
                post_id: postId,
                created_at: new Date().toISOString()
            });
            setContent('');
            setImage(null);
        }
    };

    return (
        <div className={`space-y-3 ${isReply ? 'ml-11 border-l-2 border-gray-100 pl-4' : ''}`}>
            <Textarea
                placeholder={placeholder}
                value={content}
                onChange={(e) => setContent(e.target.value)}
                className={`
                    resize-none border-[#509ca2]/20 focus:border-[#509ca2] focus:ring-[#509ca2] text-sm
                    ${isReply ? 'min-h-[60px]' : 'min-h-[80px]'}
                `}
            />
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <Input
                        type="file"
                        accept="image/*"
                        onChange={handleImageUpload}
                        className="hidden"
                        id={inputId}
                    />
                    <label
                        htmlFor={inputId}
                        className="flex items-center gap-2 px-3 py-1 text-sm text-[#509ca2] hover:bg-[#509ca2]/10 rounded-md cursor-pointer transition-colors"
                    >
                        <ImageIcon className="h-4 w-4" />
                        Añadir foto
                    </label>
                    {image && (
                        <div className="relative">
                            <img src={image} alt="Preview" className="h-10 w-10 object-cover rounded" />
                            <button
                                onClick={() => setImage(null)}
                                className="absolute -top-1 -right-1 bg-[#d55b49] text-white rounded-full p-0.5 text-xs"
                            >
                                <X className="h-3 w-3" />
                            </button>
                        </div>
                    )}
                </div>
                <div className="flex gap-2">
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={onCancel}
                        className="text-sm font-medium hover:text-gray-700"
                    >
                        Cancelar
                    </Button>
                    <Button
                        size="sm"
                        onClick={handleSubmit}
                        disabled={!content.trim() && !image}
                        className="bg-[#509ca2] hover:bg-[#509ca2]/90 text-white h-8 font-medium"
                    >
                        {buttonText}
                    </Button>
                </div>
            </div>
        </div>
    );
}