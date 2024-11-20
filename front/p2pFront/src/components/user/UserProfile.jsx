import React, { useState } from "react";
import { Camera, Edit, PawPrintIcon, User } from "lucide-react";

const UserProfile = () => {
  const [coverImage, setCoverImage] = useState(null);
  const [profileImage, setProfileImage] = useState(null);

  // Información del usuario con datos adicionales
  const user = {
    name: "Sarah Johnson", 
    firstName: "Alvaro",
    lastName: "Johnson Gonzalez",
    username: "@pawsome_sarah",
    bio: "Orgullosa de ser mamá de dos perritos 🐶 y un gatito 🐱",
    city: "Medellín 🏙️", 
    country: "Colombia ✨", 
    // followers: 1234,
    // following: 856,
    coverPhoto: "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?ixlib=rb-1.2.1&auto=format&fit=crop&w=2000&q=80",
    profilePhoto: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
    pets: [
      {
        name: "Luna",
        type: "Perro",
        breed: "Pug",  
        photo: "https://images.unsplash.com/photo-1517849845537-4d257902454a?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
        followers: 856,
      },
      {
        name: "Milo",
        type: "Gato",
        breed: "Siamese", 
        photo: "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
        followers: 743,
      },
      {
        name: "Teox",
        type: "Perro",
        breed: "Pastor Collie", 
        photo: "https://images.unsplash.com/photo-1587300003388-59208cc962cb?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80",
        followers: 921,
      }
    ]
  };

  const handleCoverChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setCoverImage(URL.createObjectURL(file));
    }
  };

  const handleProfileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setProfileImage(URL.createObjectURL(file));
    }
  };

  return (
    <div className="max-w-4xl mx-auto pb-12">
      {/* Foto de portada */}
      <div className="relative h-80">
        <img
          src={coverImage || user.coverPhoto}
          alt="Foto de portada"
          className="w-full h-full object-cover"
        />
        <label className="absolute bottom-4 right-4 bg-white p-2 rounded-full shadow-lg cursor-pointer">
          <Camera size={24} className="text-[#509ca2]" />
          <input 
            type="file" 
            accept="image/*"
            onChange={handleCoverChange}
            className="absolute inset-0 opacity-0 cursor-pointer"
          />
        </label>
      </div>

      {/* Información del usuario */}
      <div className="relative px-6 -mt-24">
        <div className="flex flex-col items-center gap-6">
          {/* Foto de perfil */}
          <div className="relative">
            <img
              src={profileImage || user.profilePhoto}
              alt={user.name}
              className="w-48 h-48 rounded-full border-4 border-white object-cover shadow-lg"
            />
            <label className="absolute bottom-4 right-4 bg-white p-2 rounded-full shadow-lg cursor-pointer">
              <Camera size={20} className="text-[#509ca2]" />
              <input
                type="file"
                accept="image/*"
                onChange={handleProfileChange}
                className="absolute inset-0 opacity-0 cursor-pointer"
              />
            </label>
          </div>

          {/* Información adicional del usuario */}
          <div className="flex-1 text-center">
          <h1 className="text-3xl font-bold">{user.firstName} {user.lastName}</h1>
          <p className="text-[#509ca2] font-medium">{user.username}</p>
          <p className="mt-2 text-gray-600">{user.bio}</p>
          <p className="mt-2 text-gray-600">Ciudad: {user.city}</p>
          <p className="mt-2 text-gray-600">País: {user.country}</p>

          {/* Mostrar seguidores y seguidos
          <div className="mt-6 flex justify-center gap-10">
            <div className="text-[#d55b49] text-3xl font-bold">
              <p>{user.followers}</p>
              <p className="text-gray-600 text-lg">Seguidores</p>
            </div>
            <div className="text-[#d55b49] text-3xl font-bold">
              <p>{user.following}</p>
              <p className="text-gray-600 text-lg">Seguidos</p>
            </div>
          </div> */}
        </div>

          {/* Botón para editar perfil */}
          <div className="mt-4 w-full flex justify-center">
            <button className="btn-primary flex items-center gap-2 bg-[#509ca2] text-white py-2 px-4 rounded-lg shadow-lg hover:bg-[#4a8e97] transition-all duration-300">
              <Edit /> Editar perfil
            </button>
          </div>
        </div>
      </div>

      {/* Sección de mascotas */}
      <div className="mt-12">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
          <PawPrintIcon className="text-[#d55b49]" /> Mis mascotas
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {user.pets.map((pet, index) => (
            <div
              key={index}
              className="pet-card relative bg-white rounded-lg overflow-hidden shadow-lg transform transition-transform hover:scale-105 hover:shadow-xl cursor-pointer"
              style={{
                transition: "all 0.3s ease",
                boxShadow: "0 4px 10px rgba(213, 91, 73, 0.6)", 
                border: "2px solid #d55b49" 
              }}
              onClick={() => alert(`Hiciste clic en el perfil de ${pet.name}`)}
            >
              <img
                src={pet.photo}
                alt={pet.name}
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <h3 className="text-xl font-bold">{pet.name}</h3>
                <p className="text-[#509ca2]">{pet.type}</p>
                <p className="text-gray-600">Raza: {pet.breed}</p>
                <div className="flex items-center gap-2 mt-2 text-gray-600">
                  <User />
                  <span>{pet.followers} seguidores</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
