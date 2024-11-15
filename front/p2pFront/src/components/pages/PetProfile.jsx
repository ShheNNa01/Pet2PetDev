import React, { useState, useEffect } from 'react';
import { MessageCircle, Edit, Grid, Settings, Share2, User, Info, PawPrint, Calendar, Camera, Heart } from 'lucide-react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { usePet } from '../context/PetContext';
import { petService } from '../services/petService';
import { postService } from '../services/PostService';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar';
import { Card } from '../ui/card';
import { Button } from '../ui/button';

const PetProfile = () => {
  const { id: paramsId } = useParams();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const queryId = queryParams.get('id');
  const petId = paramsId || queryId;
  
  const navigate = useNavigate();
  const { user } = useAuth();
  const { currentPet } = usePet();
  const [pet, setPet] = useState(null);
  const [posts, setPosts] = useState([]);
  const [breeds, setBreeds] = useState([]);
  const [isFollowing, setIsFollowing] = useState(false);
  const [activeTab, setActiveTab] = useState('posts');
  const [counters, setCounters] = useState({
    followersCount: 0,
    followingCount: 0,
    postsCount: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const isFromProfileSection = location.state?.fromProfileSection;
  const isOwner = currentPet?.pet_id === parseInt(petId) || 
                  (isFromProfileSection && currentPet?.pet_id === parseInt(petId));

  useEffect(() => {
    const loadData = async () => {
      try {
        if (!petId) {
          throw new Error('ID de mascota no proporcionado');
        }

        setLoading(true);
        setError(null);

        // Cargar datos necesarios
        const [petData, breedsData, counts, followers] = await Promise.all([
          petService.getPetById(petId),
          petService.getBreeds(),
          petService.getFollowCounts(petId),
          currentPet?.pet_id !== parseInt(petId) ? petService.getPetFollowers(petId) : null
        ]);

        setPet(petData);
        setBreeds(breedsData);
        setCounters(prev => ({
          ...prev,
          followersCount: counts.followersCount,
          followingCount: counts.followingCount
        }));

        // Verificar si está siguiendo
        if (followers && currentPet) {
          setIsFollowing(followers.followers.some(f => f.pet_id === currentPet.pet_id));
        }

        // Cargar posts
        const postsData = await postService.getMyPosts({ pet_id: petId });
        setPosts(postsData);
        setCounters(prev => ({
          ...prev,
          postsCount: postsData.length
        }));

      } catch (error) {
        console.error('Error cargando datos:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [petId, currentPet]);

  const handleFollow = async () => {
    if (!currentPet) {
      navigate('/login');
      return;
    }

    try {
      if (isFollowing) {
        await petService.unfollowPet(parseInt(petId), currentPet.pet_id);
      } else {
        await petService.followPet(parseInt(petId), currentPet.pet_id);
      }
      setIsFollowing(!isFollowing);
      
      const counts = await petService.getFollowCounts(petId);
      setCounters(prev => ({
        ...prev,
        followersCount: counts.followersCount
      }));
    } catch (error) {
      console.error('Error al seguir/dejar de seguir:', error);
    }
  };

  const getBreedName = (breedId) => {
    const breed = breeds.find(b => b.breed_id === breedId);
    return breed ? breed.breed_name : 'No especificada';
  };

  if (loading) {
    return (
      <div className="min-h-screen w-full bg-[#eeede8] p-4 flex items-center justify-center">
        <p>Cargando...</p>
      </div>
    );
  }

  if (error || !pet) {
    return (
      <div className="min-h-screen w-full bg-[#eeede8] p-4 flex items-center justify-center">
        <p className="text-red-500">{error || 'No se encontró la mascota'}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full bg-[#eeede8] p-4">
      {/* Huellas decorativas */}
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

      <main className="mx-auto max-w-lg relative z-10">
        <Card className="bg-white rounded-xl shadow-md overflow-hidden">
          {/* Sección del perfil */}
          <div className="p-6">
            <div className="flex flex-col items-center">
              {/* Avatar */}
              <div className="relative mb-6">
                <Avatar className="w-28 h-28 ring-4 ring-[#d55b49]">
                  <AvatarImage 
                    src={pet.pet_picture}
                    alt={pet.name}
                    className="object-cover"
                  />
                  <AvatarFallback className="bg-[#d55b49]/10 text-[#d55b49] text-2xl font-bold">
                    {pet.name[0]?.toUpperCase() || <PawPrint className="w-8 h-8" />}
                  </AvatarFallback>
                </Avatar>
                {isOwner && (
                  <button 
                    className="absolute bottom-0 right-0 bg-white rounded-full p-2 shadow-md hover:bg-gray-50 transition-colors"
                    onClick={() => navigate(`/pets/${pet.pet_id}/edit`)}
                  >
                    <Camera className="w-4 h-4 text-[#d55b49]" />
                  </button>
                )}
              </div>

              {/* Información básica */}
              <div className="text-center space-y-3 w-full max-w-sm mb-6">
                <div className="flex items-center justify-center gap-2">
                  <h1 className="text-2xl font-bold text-[#1a1a1a]">{pet.name}</h1>
                  {isOwner && (
                    <button 
                      onClick={() => navigate(`/pets/${pet.pet_id}/edit`)}
                      className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <Settings className="w-5 h-5 text-[#d55b49]" />
                    </button>
                  )}
                </div>
                <p className="text-[#1a1a1a]/70 flex items-center justify-center gap-2">
                  <PawPrint className="w-4 h-4" />
                  {getBreedName(pet.breed_id)} • {pet.gender === 'M' ? 'Macho ♂️' : 'Hembra ♀️'}
                </p>
                {pet.bio && (
                  <p className="text-sm text-[#1a1a1a]/70">{pet.bio}</p>
                )}
              </div>

              {/* Estadísticas */}
              <div className="w-full bg-[#eeede8] rounded-xl p-4 mb-6">
                <div className="grid grid-cols-3 gap-8">
                  <div className="text-center">
                    <p className="text-2xl font-bold text-[#1a1a1a]">{counters.postsCount}</p>
                    <p className="text-sm text-[#1a1a1a]/70">Aventuras</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-[#1a1a1a]">{counters.followersCount}</p>
                    <p className="text-sm text-[#1a1a1a]/70">Amigos peludos</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-[#1a1a1a]">{counters.followingCount}</p>
                    <p className="text-sm text-[#1a1a1a]/70">Siguiendo</p>
                  </div>
                </div>
              </div>

              {/* Botones de acción */}
              <div className="w-full space-y-3">
                {isOwner ? (
                  <Button 
                    onClick={() => navigate(`/pets/${pet.pet_id}/edit`)}
                    className="w-full bg-[#d55b49] hover:bg-[#d55b49]/90"
                  >
                    <Edit className="w-4 h-4 mr-2" />
                    Editar Perfil
                  </Button>
                ) : (
                  <div className="flex gap-2">
                    <Button 
                      onClick={handleFollow}
                      className={`flex-1 ${
                        isFollowing 
                          ? 'bg-[#509ca2] hover:bg-[#509ca2]/90' 
                          : 'bg-[#d55b49] hover:bg-[#d55b49]/90'
                      }`}
                    >
                      <Heart className={`w-4 h-4 mr-2 ${isFollowing ? 'fill-current' : ''}`} />
                      {isFollowing ? 'Siguiendo' : 'Seguir'}
                    </Button>
                    <Button variant="outline" size="icon">
                      <MessageCircle className="w-5 h-5" />
                    </Button>
                    <Button variant="outline" size="icon">
                      <Share2 className="w-5 h-5" />
                    </Button>
                  </div>
                )}

                <Button
                  variant="outline"
                  onClick={() => navigate(`/userProfile/${pet.user_id}`)}
                  className="w-full"
                >
                  <User className="w-4 h-4 mr-2" />
                  Perfil del humano
                </Button>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="border-t border-[#eeede8]">
            <div className="flex">
              <button 
                onClick={() => setActiveTab('posts')}
                className={`flex-1 py-3 font-medium text-sm inline-flex items-center justify-center gap-2
                  ${activeTab === 'posts' 
                    ? 'border-b-2 border-[#d55b49] text-[#d55b49]' 
                    : 'text-[#1a1a1a]/70 hover:bg-[#eeede8]'
                  }`}
              >
                <Grid className="w-4 h-4" />
                Momentos Peludos
              </button>
              <button 
                onClick={() => setActiveTab('about')}
                className={`flex-1 py-3 font-medium text-sm inline-flex items-center justify-center gap-2
                  ${activeTab === 'about' 
                    ? 'border-b-2 border-[#d55b49] text-[#d55b49]' 
                    : 'text-[#1a1a1a]/70 hover:bg-[#eeede8]'
                  }`}
              >
                <Info className="w-4 h-4" />
                Sobre Mí
              </button>
            </div>

            {activeTab === 'posts' ? (
              <div className="p-4">
                {posts.length > 0 ? (
                  <div className="grid grid-cols-3 gap-1">
                    {posts.map((post) => (
                      <div 
                        key={post.post_id} 
                        className="aspect-square group relative overflow-hidden bg-[#eeede8] rounded-lg cursor-pointer"
                        onClick={() => navigate(`/posts/${post.post_id}`)}
                      >
                        {post.media_urls && post.media_urls[0] ? (
                          <>
                            <img
                              src={post.media_urls[0]}
                              alt="Momento peludo"
                              className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                            />
                            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors" />
                          </>
                        ) : (
                          <div className="w-full h-full flex flex-col items-center justify-center p-2 group-hover:bg-[#eeede8]/70 transition-colors">
                            <PawPrint className="w-6 h-6 text-[#1a1a1a]/30 mb-2" />
                            <p className="text-xs text-[#1a1a1a]/70 text-center line-clamp-3">
                              {post.content}
                            </p>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="py-12 text-center">
                    <PawPrint className="w-12 h-12 mx-auto mb-4 text-[#1a1a1a]/30" />
                    <p className="text-[#1a1a1a]/70">Aún no hay momentos peludos</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="p-6">
                <div className="space-y-6">
                  <div className="space-y-4">
                    <h3 className="font-semibold text-[#1a1a1a]">Información básica</h3>
                    <div className="grid gap-4">
                      <InfoItem  
                        icon={PawPrint}
                        label="Raza"
                        value={getBreedName(pet.breed_id)}
                        iconColor="text-[#d55b49]"
                      />
                      <InfoItem 
                        icon={Calendar}
                        label="Edad"
                        value={`${calculateAge(pet.birthdate)} • ${format(new Date(pet.birthdate), "d 'de' MMMM yyyy", { locale: es })}`}
                        iconColor="text-[#d55b49]"
                      />
                      <InfoItem 
                        icon={Heart}
                        label="Género"
                        value={pet.gender === 'M' ? 'Macho ♂️' : 'Hembra ♀️'}
                        iconColor="text-[#d55b49]"
                      />
                      {pet.weight && (
                        <InfoItem 
                          icon={PawPrint}
                          label="Peso"
                          value={`${pet.weight} kg`}
                          iconColor="text-[#d55b49]"
                        />
                      )}
                    </div>
                  </div>

                  {/* Características especiales */}
                  {(pet.special_needs || pet.allergies || pet.favorite_activities || pet.favorite_toys) && (
                    <div className="space-y-4">
                      <h3 className="font-semibold text-[#1a1a1a]">Características especiales</h3>
                      <div className="grid gap-4">
                        {pet.special_needs && (
                          <InfoItem 
                            icon={Heart}
                            label="Necesidades especiales"
                            value={pet.special_needs}
                            iconColor="text-[#509ca2]"
                          />
                        )}
                        {pet.allergies && (
                          <InfoItem 
                            icon={AlertCircle}
                            label="Alergias"
                            value={pet.allergies}
                            iconColor="text-[#509ca2]"
                          />
                        )}
                        {pet.favorite_activities && (
                          <InfoItem 
                            icon={PawPrint}
                            label="Actividades favoritas"
                            value={pet.favorite_activities}
                            iconColor="text-[#509ca2]"
                          />
                        )}
                        {pet.favorite_toys && (
                          <InfoItem 
                            icon={Heart}
                            label="Juguetes favoritos"
                            value={pet.favorite_toys}
                            iconColor="text-[#509ca2]"
                          />
                        )}
                      </div>
                    </div>
                  )}

                  {/* Información médica */}
                  {(pet.vaccinations || pet.last_checkup || pet.veterinary_contact) && (
                    <div className="space-y-4">
                      <h3 className="font-semibold text-[#1a1a1a]">Información médica</h3>
                      <div className="grid gap-4">
                        {pet.vaccinations && (
                          <InfoItem 
                            icon={Shield}
                            label="Vacunas"
                            value={pet.vaccinations}
                            iconColor="text-[#d55b49]"
                          />
                        )}
                        {pet.last_checkup && (
                          <InfoItem 
                            icon={Calendar}
                            label="Último chequeo"
                            value={format(new Date(pet.last_checkup), "d 'de' MMMM yyyy", { locale: es })}
                            iconColor="text-[#d55b49]"
                          />
                        )}
                        {pet.veterinary_contact && (
                          <InfoItem 
                            icon={Phone}
                            label="Contacto veterinario"
                            value={pet.veterinary_contact}
                            iconColor="text-[#d55b49]"
                          />
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </Card>
      </main>
    </div>
  );
};

// Componente auxiliar para mostrar items de información
const InfoItem = ({ icon: Icon, label, value, iconColor = "text-[#d55b49]" }) => (
  <div className="flex items-start gap-3">
    <div className={`mt-1 ${iconColor}`}>
      <Icon className="w-5 h-5" />
    </div>
    <div>
      <p className="text-sm font-medium text-[#1a1a1a]">{label}</p>
      <p className="text-sm text-[#1a1a1a]/70">{value}</p>
    </div>
  </div>
);

// Función auxiliar para calcular la edad
const calculateAge = (birthdate) => {
  if (!birthdate) return '';
  const birth = new Date(birthdate);
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  
  return `${age} años`;
};

export default PetProfile;