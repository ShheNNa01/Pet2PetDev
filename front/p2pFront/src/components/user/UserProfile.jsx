import React, { useState, useEffect } from "react";
import { Camera, Edit, MapPin, Settings, PawPrintIcon as Paw, User } from "lucide-react";

const backgroundEmojis = ["🐶", "🐱", "🐰", "🐦", "🐹", "🐠", "🦜", "🐢"];

export default function UserProfile() {
  const [bgEmoji, setBgEmoji] = useState(backgroundEmojis[0]);

  useEffect(() => {
    const interval = setInterval(() => {
      setBgEmoji(
        backgroundEmojis[Math.floor(Math.random() * backgroundEmojis.length)]
      );
    }, 5000); // Cambia cada 5 segundos

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-[#eeede8] p-4 md:p-8 relative overflow-hidden">
      {/* Fondo dinámico */}
      <div
        className="absolute inset-0 opacity-10 flex flex-wrap justify-center items-center overflow-hidden"
        aria-hidden="true"
      >
        {Array.from({ length: 100 }).map((_, i) => (
          <span
            key={i}
            className="text-6xl m-4 animate-float"
            style={{ animationDelay: `${i * 0.1}s` }}
          >
            {bgEmoji}
          </span>
        ))}
      </div>

      {/* Tarjeta de Perfil */}
      <div className="mx-auto max-w-4xl bg-white relative z-10 rounded-lg shadow-lg overflow-hidden">
        <div className="relative h-48 md:h-64 bg-[#509be2]">
          <img
            alt="Cover"
            className="h-full w-full object-cover mix-blend-overlay"
            src="/placeholder.svg?height=300&width=800"
          />
          <button className="absolute bottom-4 right-4 bg-white/80 hover:bg-white p-2 rounded-full shadow">
            <Camera className="h-4 w-4 text-[#d55b49]" />
          </button>
        </div>

        <div className="relative px-4 pb-4 md:px-6">
          <div className="absolute -top-12 h-24 w-24 border-4 border-white rounded-full overflow-hidden">
            <img
              alt="User"
              src="/placeholder.svg?height=120&width=120"
              className="h-full w-full object-cover"
            />
          </div>
          <div className="ml-24 mt-4 md:ml-36">
            <div className="flex items-start justify-between">
              <div>
                <h1 className="text-2xl font-bold text-[#1a1a1a]">
                  María González
                </h1>
                <div className="flex items-center gap-2 text-sm text-[#509be2]">
                  <MapPin className="h-4 w-4" />
                  <span>Barcelona, España</span>
                </div>
              </div>
              <div className="flex gap-2">
                <button className="border-[#d55b49] text-[#d55b49] hover:bg-[#d55b49] hover:text-white px-4 py-2 rounded shadow">
                  <Edit className="mr-2 h-4 w-4" />
                  Editar Perfil
                </button>
                <button className="text-[#509be2] hover:bg-[#509be2]/10 p-2 rounded-full shadow">
                  <Settings className="h-4 w-4" />
                </button>
              </div>
            </div>

            <p className="mt-4 text-gray-600">
              Amante de los animales 🐾 | Voluntaria en refugio local | Madre de
              3 perritos adorables
            </p>

            <div className="mt-4 flex gap-4">
              <div className="text-center">
                <div className="font-bold text-[#d55b49] text-xl">128</div>
                <div className="text-sm text-[#509be2]">Seguidores</div>
              </div>
              <div className="text-center">
                <div className="font-bold text-[#d55b49] text-xl">84</div>
                <div className="text-sm text-[#509be2]">Siguiendo</div>
              </div>
              <div className="text-center">
                <div className="font-bold text-[#d55b49] text-xl">3</div>
                <div className="text-sm text-[#509be2]">Mascotas</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="mx-auto max-w-4xl mt-6 bg-white relative z-10 rounded-lg shadow-lg overflow-hidden">
        <div className="p-4">
          <div className="grid w-full grid-cols-2 gap-4">
            <button className="bg-[#d55b49] text-white px-4 py-2 rounded shadow">
              <Paw className="mr-2 h-4 w-4" />
              Mis Mascotas
            </button>
            <button className="bg-[#509be2] text-white px-4 py-2 rounded shadow">
              <User className="mr-2 h-4 w-4" />
              Información Completa
            </button>
          </div>

          {/* Contenido de mascotas */}
          <div className="mt-4 grid gap-4 md:grid-cols-3">
            {[1, 2, 3].map((pet) => (
              <div
                key={pet}
                className="overflow-hidden bg-white hover:shadow-lg transition-shadow duration-300 rounded-lg"
              >
                <img
                  alt={`Pet ${pet}`}
                  className="h-48 w-full object-cover"
                  src="/placeholder.svg?height=200&width=300"
                />
                <div className="p-4">
                  <h3 className="font-bold text-[#1a1a1a]">Luna {pet}</h3>
                  <p className="mt-2 text-sm text-[#d55b49]">
                    {pet} años • Golden Retriever
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
