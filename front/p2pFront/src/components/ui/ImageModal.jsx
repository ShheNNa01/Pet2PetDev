import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Dialog, DialogContent } from './dialog';
import { cn } from '../../lib/utils';

export const ImageModal = ({
    isOpen,
    onClose,
    images,
    selectedIndex,
    onNavigate
}) => {
    const handlePrevious = (e) => {
        e.stopPropagation();
        if (selectedIndex > 0) {
            onNavigate(selectedIndex - 1);
        }
    };

    const handleNext = (e) => {
        e.stopPropagation();
        if (selectedIndex < images.length - 1) {
            onNavigate(selectedIndex + 1);
        }
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="relative max-w-screen max-h-screen p-0 bg-black/95 border-none overflow-hidden">
                <div className="absolute inset-0 flex items-center justify-center">
                    {/* Contenedor de imagen centrado */}
                    <div className="relative flex items-center justify-center w-full h-full">
                        {/* Botones de navegación */}
                        {selectedIndex > 0 && (
                            <button
                                onClick={handlePrevious}
                                className="absolute left-4 z-50 w-10 h-10 flex items-center justify-center
                                            rounded-full bg-white/90 hover:bg-white 
                                            transition-all duration-200 shadow-lg"
                                aria-label="Anterior imagen"
                            >
                                <ChevronLeft className="h-6 w-6 text-gray-800" />
                            </button>
                        )}

                        {/* Imagen Principal */}
                        <img
                            src={images[selectedIndex]}
                            alt={`Imagen ${selectedIndex + 1}`}
                            className="max-w-[85vw] max-h-[85vh] w-auto h-auto object-contain
                                        transition-all duration-300 select-none"
                            loading="lazy"
                        />

                        {/* Botón Siguiente */}
                        {selectedIndex < images.length - 1 && (
                            <button
                                onClick={handleNext}
                                className="absolute right-4 z-50 w-10 h-10 flex items-center justify-center
                                            rounded-full bg-white/90 hover:bg-white 
                                            transition-all duration-200 shadow-lg"
                                aria-label="Siguiente imagen"
                            >
                                <ChevronRight className="h-6 w-6 text-gray-800" />
                            </button>
                        )}
                    </div>

                    {/* Indicadores de Imagen */}
                    {images.length > 1 && (
                        <div className="absolute bottom-6 left-0 right-0">
                            <div className="flex justify-center gap-2">
                                {images.map((_, index) => (
                                    <button
                                        key={index}
                                        onClick={() => onNavigate(index)}
                                        className={cn(
                                            "w-2 h-2 rounded-full transition-all duration-200",
                                            selectedIndex === index 
                                                ? "bg-white scale-110" 
                                                : "bg-white/50 hover:bg-white/75"
                                        )}
                                        aria-label={`Ir a imagen ${index + 1}`}
                                    />
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </DialogContent>
        </Dialog>
    );
};