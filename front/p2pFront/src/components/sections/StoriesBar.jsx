// StoriesBar.jsx
"use client";
import React, { useState } from "react";
import { PlusIcon } from "@heroicons/react/24/solid";
import { ScrollArea } from "../ui/scroll-area"; // Importa el ScrollArea desde el archivo separado

const StoriesBar = () => {
    // Estado inicial de las historias con el campo `seen`
    const [stories, setStories] = useState([
        { id: 1, name: "Rocky", initial: "R", seen: false },
        { id: 2, name: "Bella", initial: "B", seen: true },
        { id: 3, name: "Charlie", initial: "C", seen: false },
        { id: 4, name: "Lucy", initial: "L", seen: true },
        { id: 5, name: "Max", initial: "M", seen: false },
    ]);

    // Función para marcar una historia como vista y moverla al final
    const handleStoryClick = (id) => {
        setStories((prevStories) => {
            const updatedStories = prevStories.map((story) =>
                story.id === id ? { ...story, seen: true } : story
            );
            return [
                ...updatedStories.filter((story) => !story.seen),
                ...updatedStories.filter((story) => story.seen),
            ];
        });
    };

    return (
        <div className="p-4 bg-white rounded-lg shadow-md">
            <h2 className="text-lg font-bold mb-2">Historias</h2>
            <ScrollArea className="overflow-x-auto">
                <div className="flex gap-4 px-2 py-4 items-center">
                    {/* Sección de "Tu historia" */}
                    <div className="relative flex flex-col items-center">
                        <div className="relative flex items-center justify-center w-16 h-16 rounded-full border-2 border-teal-500">
                            {/* Foto de perfil en el centro */}
                            <img
                                src="/path/to/profile-picture.jpg" // Cambia esta ruta a la foto del perfil del usuario
                                alt="Tu historia"
                                className="w-full h-full rounded-full"
                            />
                            {/* Icono de "+" pequeño en la esquina inferior derecha */}
                            <PlusIcon className="absolute bottom-0 right-0 w-4 h-4 text-teal-500 bg-white rounded-full" />
                        </div>
                        <span className="text-sm mt-1">Tu historia</span>
                    </div>

                    {/* Historias de otros usuarios */}
                    {stories.map((story) => (
                        <div
                            key={story.id}
                            className="relative flex flex-col items-center cursor-pointer"
                            onClick={() => handleStoryClick(story.id)}
                        >
                            <div
                                className={`relative flex items-center justify-center w-16 h-16 rounded-full border-2 ${
                                    story.seen ? "border-gray-400" : "border-teal-500"
                                }`}
                            >
                                <span className="font-bold text-lg text-gray-700">
                                    {story.initial}
                                </span>
                                {/* Punto verde o gris según el estado de visto */}
                                {!story.seen && (
                                    <div className="absolute bottom-1 right-1 w-3 h-3 rounded-full bg-teal-500"></div>
                                )}
                            </div>
                            <span className="text-sm mt-1">{story.name}</span>
                        </div>
                    ))}
                </div>
            </ScrollArea>
        </div>
    );
};

export default StoriesBar;
