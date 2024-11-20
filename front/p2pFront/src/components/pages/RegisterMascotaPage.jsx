import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import Header from '../layout/header/Header';
import Footer from '../layout/Footer';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { ArrowLeft } from 'lucide-react';
import { petService } from '../services/petService';
import { usePet } from '../context/PetContext';
import GifAnimation from '../common/GifAnimation';
import { SelectField } from '../forms/SelectField';
import { InputField } from '../forms/InputField';
import { TextAreaField } from '../forms/TextAreaField';
import { PetFormHeader } from '../common/PetFormHeader';

export default function PetRegistrationForm() {
  const navigate = useNavigate();
  const { setMyPets } = usePet();
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm({
    defaultValues: {
      name: '',
      breed_id: '',
      birthdate: '',
      gender: '',
      bio: ''
    }
  });

  const [petTypes, setPetTypes] = useState([]);
  const [breeds, setBreeds] = useState([]);
  const [selectedPetType, setSelectedPetType] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPetTypes = async () => {
      try {
        setIsLoading(true);
        const response = await petService.getPetTypes();
        const formattedTypes = Array.isArray(response) ? response : response?.data || [];
        setPetTypes(formattedTypes);
      } catch (err) {
        console.error('Error al cargar tipos de mascotas:', err);
        setError('Error al cargar tipos de mascotas');
      } finally {
        setIsLoading(false);
      }
    };

    fetchPetTypes();
  }, []);

  useEffect(() => {
    const fetchBreeds = async () => {
      if (selectedPetType) {
        try {
          setIsLoading(true);
          const response = await petService.getBreeds({ 
            pet_type_id: parseInt(selectedPetType) 
          });
          const formattedBreeds = Array.isArray(response) ? response : response?.data || [];
          setBreeds(formattedBreeds);
        } catch (err) {
          console.error('Error al cargar razas:', err);
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
    setSelectedPetType(value);
    setValue('breed_id', '');
  };

  const onSubmit = async (data) => {
    setIsSubmitting(true);
    setError(null);

    try {
      const petData = {
        name: data.name,
        birthdate: data.birthdate,
        breed_id: parseInt(data.breed_id),
        gender: data.gender,
        bio: data.bio ? data.bio.trim() : null
      };

      await petService.createPet(petData);
      const updatedPets = await petService.getMyPets();
      setMyPets(Array.isArray(updatedPets) ? updatedPets : updatedPets.data || []);
      navigate('/pets');
    } catch (err) {
      setError(err.response?.data?.message || 'Error al registrar la mascota');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading && !petTypes.length) {
    return (
      <div className="min-h-screen bg-[#eeede8] flex justify-center items-center p-6">
        <div className="text-lg flex items-center space-x-2">
          <span className="animate-spin rounded-full h-6 w-6 border-b-2 border-[#509ca2]"></span>
          <span>Cargando...</span>
        </div>
      </div>
    );
  }

  const petTypeOptions = petTypes.map(type => ({
    value: type.pet_type_id,
    label: type.type_name
  }));

  const breedOptions = breeds.map(breed => ({
    value: breed.breed_id,
    label: breed.breed_name
  }));

  const genderOptions = [
    { value: 'male', label: 'Macho' },
    { value: 'female', label: 'Hembra' }
  ];

  return (
    <div className="min-h-screen bg-[#eeede8]">
      <Header />
        <div className="space-y-8">
          {/* Botón Regresar */}
          <button
            onClick={() => navigate('/pets')}
            className="flex items-center text-[#509ca2] hover:text-[#d55b49] transition-colors"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Regresar
          </button>

          {/* Formulario */}
          <Card className="bg-white/95 backdrop-blur shadow-xl rounded-xl p-8">
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-600 rounded-lg">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <PetFormHeader />

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <InputField
                  label="Nombre"
                  register={register}
                  name="name"
                  error={errors.name}
                  placeholder="Nombre de tu mascota"
                  required
                />

                <SelectField
                  label="Tipo de mascota"
                  value={selectedPetType}
                  onChange={handlePetTypeChange}
                  options={petTypeOptions}
                  placeholder="Seleccione un tipo"
                  error={errors.petType?.message}
                  required
                />

                <SelectField
                  label="Raza"
                  value={watch('breed_id')}
                  onChange={(e) => setValue('breed_id', e.target.value)}
                  options={breedOptions}
                  placeholder="Seleccione una raza"
                  error={errors.breed_id?.message}
                  disabled={!selectedPetType}
                  required
                />

                <InputField
                  label="Fecha de nacimiento"
                  type="date"
                  register={register}
                  name="birthdate"
                  error={errors.birthdate}
                  required
                />

                <SelectField
                  label="Género"
                  value={watch('gender')}
                  onChange={(e) => setValue('gender', e.target.value)}
                  options={genderOptions}
                  placeholder="Seleccione un género"
                  error={errors.gender?.message}
                  required
                />

                <div className="md:col-span-2">
                  <TextAreaField
                    label="Biografía"
                    register={register}
                    name="bio"
                    error={errors.bio}
                    placeholder="Cuéntanos sobre tu mascota..."
                  />
                </div>
              </div>

              <div className="flex justify-center pt-6">
                <Button
                  type="submit"
                  disabled={isSubmitting}
                  className={`
                    px-8 py-3 rounded-full text-lg font-semibold
                    bg-[#d55b49] hover:bg-[#509ca2] text-white
                    transform transition-all duration-200
                    hover:scale-105 active:scale-95
                    disabled:opacity-70 disabled:cursor-not-allowed
                    shadow-md hover:shadow-lg
                  `}
                >
                  {isSubmitting ? 'Registrando...' : 'Registrar Mascota'}
                </Button>
              </div>
            </form>
          </Card>
        </div>

      <Footer />
    </div>
  );
}