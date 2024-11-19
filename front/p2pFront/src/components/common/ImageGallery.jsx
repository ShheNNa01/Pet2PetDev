import React, { useState } from 'react';
import { ImageModal } from '../ui/ImageModal';

export const ImageGallery = ({ images }) => {
    const [selectedImage, setSelectedImage] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const renderGalleryLayout = () => {
        if (!images || images.length === 0) return null;

        if (images.length === 1) {
            return (
                <div 
                    className="w-full h-[400px] cursor-pointer"
                    onClick={() => {
                        setSelectedImage(0);
                        setIsModalOpen(true);
                    }}
                >
                    <img
                        src={getNormalizedUrl(images[0])}
                        alt="Post content"
                        className="w-full h-full object-cover rounded-lg hover:opacity-95 transition-opacity"
                    />
                </div>
            );
        }

        if (images.length === 2) {
            return (
                <div className="grid grid-cols-2 gap-1 h-[400px]">
                    {images.map((url, index) => (
                        <div
                            key={index}
                            className="cursor-pointer"
                            onClick={() => {
                                setSelectedImage(index);
                                setIsModalOpen(true);
                            }}
                        >
                            <img
                                src={getNormalizedUrl(url)}
                                alt={`Content ${index + 1}`}
                                className="w-full h-full object-cover hover:opacity-95 transition-opacity"
                            />
                        </div>
                    ))}
                </div>
            );
        }

        if (images.length === 3) {
            return (
                <div className="grid grid-cols-2 gap-1 h-[400px]">
                    <div 
                        className="row-span-2 cursor-pointer"
                        onClick={() => {
                            setSelectedImage(0);
                            setIsModalOpen(true);
                        }}
                    >
                        <img
                            src={getNormalizedUrl(images[0])}
                            alt="Content 1"
                            className="w-full h-full object-cover hover:opacity-95 transition-opacity"
                        />
                    </div>
                    <div 
                        className="cursor-pointer"
                        onClick={() => {
                            setSelectedImage(1);
                            setIsModalOpen(true);
                        }}
                    >
                        <img
                            src={getNormalizedUrl(images[1])}
                            alt="Content 2"
                            className="w-full h-[200px] object-cover hover:opacity-95 transition-opacity"
                        />
                    </div>
                    <div 
                        className="cursor-pointer"
                        onClick={() => {
                            setSelectedImage(2);
                            setIsModalOpen(true);
                        }}
                    >
                        <img
                            src={getNormalizedUrl(images[2])}
                            alt="Content 3"
                            className="w-full h-[200px] object-cover hover:opacity-95 transition-opacity"
                        />
                    </div>
                </div>
            );
        }

        // 4 o más imágenes
        return (
            <div className="grid grid-cols-2 gap-1 h-[400px]">
                {images.slice(0, 4).map((url, index) => (
                    <div
                        key={index}
                        className={`relative cursor-pointer ${index === 3 && images.length > 4 ? 'overflow-hidden' : ''}`}
                        onClick={() => {
                            setSelectedImage(index);
                            setIsModalOpen(true);
                        }}
                    >
                        <img
                            src={getNormalizedUrl(url)}
                            alt={`Content ${index + 1}`}
                            className="w-full h-[200px] object-cover hover:opacity-95 transition-opacity"
                        />
                        {index === 3 && images.length > 4 && (
                            <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                                <span className="text-white text-2xl font-semibold">
                                    +{images.length - 4}
                                </span>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        );
    };

    const getNormalizedUrl = (url) => {
        const normalizedUrl = url.replace(/\\/g, '/');
        return normalizedUrl.startsWith('http')
            ? normalizedUrl
            : `${import.meta.env.VITE_API_URL}/api/v1/media/${normalizedUrl}`;
    };

    return (
        <>
            {renderGalleryLayout()}
            
            <ImageModal
                isOpen={isModalOpen}
                onClose={() => {
                    setIsModalOpen(false);
                    setSelectedImage(null);
                }}
                images={images}
                selectedIndex={selectedImage}
                onNavigate={setSelectedImage}
            />
        </>
    );
};