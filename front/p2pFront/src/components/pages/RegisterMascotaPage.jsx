import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { Card, CardContent } from '../ui/card';
import { Input } from '../ui/input';
import Label from '../ui/label';
import { Textarea } from '../ui/textarea';
import { Button } from '../ui/button';
import { ArrowLeft, PawPrint } from 'lucide-react';
import { petService } from '../services/petService';
import { useNavigate } from 'react-router-dom';
import { usePet } from '../context/PetContext';
import GifAnimation from '../common/GifAnimation';

export default function PetRegistrationForm() {
  const navigate = useNavigate();
  const { setMyPets } = usePet();
  const { register, handleSubmit, setValue, formState: { errors } } = useForm();
  const [petTypes, setPetTypes] = useState([]);
  const [breeds, setBreeds] = useState([]);
  const [selectedPetType, setSelectedPetType] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Cargar tipos de mascotas
  useEffect(() => {
    const fetchPetTypes = async () => {
      try {
        setIsLoading(true);
        const token = localStorage.getItem('token');
        console.log('Token actual:', token);

        const response = await petService.getPetTypes();
        console.log('Respuesta completa de tipos de mascotas:', response);

        let formattedTypes = [];
        if (Array.isArray(response)) {
          formattedTypes = response;
        } else if (response?.data) {
          formattedTypes = response.data;
        }

        console.log('Tipos de mascotas formateados:', formattedTypes);
        setPetTypes(formattedTypes);
      } catch (err) {
        console.error('Error detallado al cargar tipos de mascotas:', err);
        setError('Error al cargar tipos de mascotas');
      } finally {
        setIsLoading(false);
      }
    };

    fetchPetTypes();
  }, []);

  // Cargar razas cuando se selecciona un tipo de mascota
  useEffect(() => {
    const fetchBreeds = async () => {
      if (selectedPetType) {
        try {
          setIsLoading(true);
          console.log('Cargando razas para el tipo:', selectedPetType);
          
          const response = await petService.getBreeds({ 
            pet_type_id: parseInt(selectedPetType) 
          });
          console.log('Respuesta completa de razas:', response);

          let formattedBreeds = [];
          if (Array.isArray(response)) {
            formattedBreeds = response;
          } else if (response?.data) {
            formattedBreeds = response.data;
          }

          console.log('Razas formateadas:', formattedBreeds);
          setBreeds(formattedBreeds);
        } catch (err) {
          console.error('Error detallado al cargar razas:', err);
          setError('Error al cargar razas');
        } finally {
          setIsLoading(false);
        }
      } else {
        setBreeds([]);
      }
    };

    fetchBreeds();
  }, [selectedPetType]);

  const handlePetTypeChange = (e) => {
    const value = e.target.value;
    console.log('Tipo de mascota seleccionado:', value);
    setSelectedPetType(value);
    setValue('breed_id', '');
  };

  const onSubmit = async (data) => {
    setIsSubmitting(true);
    setError(null);

    try {
      console.log('Datos del formulario:', data);
      
      // Preparar los datos asegurando que bio se maneje correctamente
      const petData = {
        name: data.name,
        birthdate: data.birthdate,
        breed_id: parseInt(data.breed_id),
        gender: data.gender,
        bio: data.bio ? data.bio.trim() : null // Si hay contenido en bio, lo limpiamos, si no, enviamos null
      };

      console.log('Enviando datos de mascota:', petData);
      const response = await petService.createPet(petData);
      console.log('Respuesta de creación:', response);

      // Actualizar lista de mascotas
      const updatedPets = await petService.getMyPets();
      setMyPets(Array.isArray(updatedPets) ? updatedPets : updatedPets.data || []);

      navigate('/pets');
    } catch (err) {
      console.error('Error al registrar mascota:', err);
      setError(err.response?.data?.message || 'Error al registrar la mascota');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading && !petTypes.length) {
    return (
      <div className="min-h-screen bg-[#eeede8] p-6 flex justify-center items-center">
        <div className="text-lg">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#eeede8] p-6">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="flex justify-between items-center">
          <a
            href="/pets"
            className="inline-flex items-center text-[#509ca2] hover:text-[#d55b49] transition-colors"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Regresar
          </a>
        </div>

        {/* GIF and Quote Section */}
        <div className="text-center space-y-4">
          <div className="rounded-lg overflow-hidden shadow-xl bg-white h-[200px] flex items-center justify-center">
            <GifAnimation />
          </div>
        </div>

        {/* Form Card */}
        <Card className="bg-white shadow-xl rounded-2xl">
          <CardContent className="p-6">
            {error && (
              <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div className="text-center mb-6">
                <h1 className="text-3xl font-bold text-[#d55b49]">Registrar Mascota</h1>
                <div className="mt-1 flex justify-center">
                  <PawPrint className="text-[#509ca2] h-6 w-6" />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="name">Nombre</Label>
                  <Input
                    id="name"
                    {...register('name', { 
                      required: 'El nombre es requerido',
                      minLength: { value: 2, message: 'El nombre debe tener al menos 2 caracteres' }
                    })}
                    className="border-[#509ca2] focus:ring-[#d55b49]"
                    placeholder="Nombre de la mascota"
                  />
                  {errors.name && (
                    <span className="text-sm text-red-500">{errors.name.message}</span>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="petType">Tipo de mascota</Label>
                  <select
                    id="petType"
                    value={selectedPetType}
                    onChange={handlePetTypeChange}
                    className="w-full rounded-md border border-[#509ca2] p-2 focus:ring-[#d55b49] bg-white"
                  >
                    <option key="default-type" value="">Seleccione un tipo</option>
                    {petTypes && petTypes.map((type) => (
                      <option 
                        key={`pet-type-${type.pet_type_id}`} 
                        value={type.pet_type_id}
                      >
                        {type.type_name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="breed">Raza</Label>
                  <select
                    id="breed"
                    {...register('breed_id', { required: 'La raza es requerida' })}
                    disabled={!selectedPetType}
                    className="w-full rounded-md border border-[#509ca2] p-2 focus:ring-[#d55b49] bg-white"
                  >
                    <option key="default-breed" value="">Seleccione una raza</option>
                    {breeds && breeds.map((breed) => (
                      <option 
                        key={`breed-${breed.breed_id}`} 
                        value={breed.breed_id}
                      >
                        {breed.breed_name}
                      </option>
                    ))}
                  </select>
                  {errors.breed_id && (
                    <span className="text-sm text-red-500">{errors.breed_id.message}</span>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="birthdate">Fecha de nacimiento</Label>
                  <Input
                    type="date"
                    id="birthdate"
                    {...register('birthdate', { required: 'La fecha de nacimiento es requerida' })}
                    className="border-[#509ca2] focus:ring-[#d55b49] bg-white"
                  />
                  {errors.birthdate && (
                    <span className="text-sm text-red-500">{errors.birthdate.message}</span>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="gender">Género</Label>
                  <select
                    id="gender"
                    {...register('gender', { required: 'El género es requerido' })}
                    className="w-full rounded-md border border-[#509ca2] p-2 focus:ring-[#d55b49] bg-white"
                  >
                    <option key="default-gender" value="">Seleccione un género</option>
                    <option key="male" value="male">Macho</option>
                    <option key="female" value="female">Hembra</option>
                  </select>
                  {errors.gender && (
                    <span className="text-sm text-red-500">{errors.gender.message}</span>
                  )}
                </div>

                <div className="space-y-2 md:col-span-2">
                  <Label htmlFor="bio">Biografía</Label>
                  <Textarea
                    id="bio"
                    {...register('bio', {
                      setValueAs: (value) => value ? value.trim() : null
                    })}
                    className="border-[#509ca2] focus:ring-[#d55b49] min-h-[120px]"
                    placeholder="Cuéntanos sobre tu mascota..."
                  />
                </div>
              </div>

              <div className="flex justify-center pt-4">
                <Button
                  type="submit"
                  disabled={isSubmitting}
                  className="bg-[#d55b49] hover:bg-[#509ca2] text-white px-8 py-2 rounded-full transition-colors duration-300"
                >
                  {isSubmitting ? 'Registrando...' : 'Registrar Mascota'}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}