import React, { useState } from 'react';
import { MessageCircle, Edit, Grid, Settings, Share2, User } from 'lucide-react';

const PetProfile = () => {
  const [isFollowing, setIsFollowing] = useState(false);
  const isOwner = false;
  const isLoggedIn = true;

  return (
    <div className="min-h-screen w-full bg-[#eeede8] p-4">
      {/* Decorative paw prints with reduced opacity */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <div 
            key={i} 
            className="absolute text-[#d55b49]/5 text-4xl md:text-6xl"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              transform: `rotate(${Math.random() * 360}deg)`
            }}
          >
            🐾
          </div>
        ))}
      </div>
      
      <main className="mx-auto max-w-2xl">
        <div className="bg-white rounded-lg shadow-lg">
          <div className="p-4 md:p-6 space-y-4 md:space-y-6">
            <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
              <div className="flex flex-col md:flex-row gap-4 items-center md:items-start">
                <div className="w-20 h-20 md:w-24 md:h-24 rounded-full border-4 border-[#d55b49] overflow-hidden">
                  <img src="/api/placeholder/96/96" alt="Pet avatar" className="w-full h-full object-cover" />
                </div>
                <div className="text-center md:text-left">
                  <h1 className="text-2xl md:text-3xl font-bold text-[#1a1a1a]">Max</h1>
                  <p className="text-[#1a1a1a]/70">Golden Retriever • 3 años</p>
                  <p className="text-sm text-[#1a1a1a]/60">Viviendo mi mejor vida en Miami 🐾</p>
                </div>
              </div>
              {isOwner && (
                <button className="p-2 rounded-full hover:bg-[#eeede8]/50 transition-colors">
                  <Settings className="w-5 h-5 text-[#1a1a1a]" />
                </button>
              )}
            </div>
            
            <div className="bg-[#509ca2]/5 rounded-lg p-4">
              <div className="grid grid-cols-3 gap-2 md:gap-4">
                <div className="text-center">
                  <div className="text-xl md:text-2xl font-semibold text-[#1a1a1a]">156</div>
                  <div className="text-xs md:text-sm text-[#1a1a1a]/70">Aventuras</div>
                </div>
                <div className="text-center">
                  <div className="text-xl md:text-2xl font-semibold text-[#1a1a1a]">2.5k</div>
                  <div className="text-xs md:text-sm text-[#1a1a1a]/70">Amigos peludos</div>
                </div>
                <div className="text-center">
                  <div className="text-xl md:text-2xl font-semibold text-[#1a1a1a]">1.2k</div>
                  <div className="text-xs md:text-sm text-[#1a1a1a]/70">Siguiendo</div>
                </div>
              </div>
            </div>

            <div className="flex flex-col space-y-2">
              {isOwner ? (
                <button className="flex-1 bg-[#d55b49] text-white hover:bg-[#d55b49]/90 h-10 px-4 rounded-full inline-flex items-center justify-center transition-colors">
                  <Edit className="w-4 h-4 mr-2" />
                  Editar Perfil
                </button>
              ) : (
                <div className="flex justify-center md:justify-start items-center gap-2">
                  <button 
                    className={`h-10 px-8 md:px-12 rounded-full text-white inline-flex items-center justify-center transition-colors ${
                      isFollowing 
                        ? 'bg-[#509ca2] hover:bg-[#509ca2]/90' 
                        : 'bg-[#d55b49] hover:bg-[#d55b49]/90'
                    }`}
                    onClick={() => setIsFollowing(!isFollowing)}
                  >
                    {isFollowing ? 'Siguiendo' : 'Seguir'}
                  </button>
                  <button 
                    className="h-10 w-10 rounded-full inline-flex items-center justify-center hover:bg-[#eeede8]/50 disabled:opacity-50 transition-colors"
                    disabled={!isLoggedIn}
                    title={isLoggedIn ? "Enviar mensaje" : "Inicia sesión para enviar un mensaje"}
                  >
                    <MessageCircle className="w-5 h-5 text-[#1a1a1a]" />
                  </button>
                  <button 
                    className="h-10 w-10 rounded-full inline-flex items-center justify-center hover:bg-[#eeede8]/50 transition-colors"
                  >
                    <Share2 className="w-5 h-5 text-[#1a1a1a]" />
                  </button>
                </div>
              )}
              <div className="flex justify-center">
                <a 
                  href="/owner-profile" 
                  className="inline-flex items-center px-6 h-10 bg-[#eeede8]/50 rounded-full hover:bg-[#eeede8] transition-colors text-[#1a1a1a]"
                >
                  <User className="w-4 h-4 mr-2" />
                  Perfil del humano
                </a>
              </div>
            </div>
          </div>

          <div className="border-t border-[#eeede8]">
            <div className="flex">
              <button className="flex-1 h-12 px-4 font-medium inline-flex items-center justify-center border-b-2 border-[#d55b49] text-[#1a1a1a] bg-white transition-colors">
                <Grid className="w-4 h-4 mr-2" />
                Momentos Peludos
              </button>
              <button className="flex-1 h-12 px-4 font-medium inline-flex items-center justify-center text-[#1a1a1a]/70 hover:bg-[#eeede8]/30 transition-colors">
                Sobre Mí
              </button>
            </div>
            <div className="p-4">
              <div className="grid grid-cols-2 md:grid-cols-3 gap-1">
                {[...Array(9)].map((_, i) => (
                  <div key={i} className="aspect-square relative group overflow-hidden rounded-md bg-[#eeede8]">
                    <img
                      src={`/api/placeholder/300/300?text=Foto ${i + 1}`}
                      alt={`Momento Peludo ${i + 1}`}
                      className="object-cover w-full h-full transition-transform duration-300 group-hover:scale-105"
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PetProfile;