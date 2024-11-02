import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import GifAnimation from '../common/GifAnimation'; // Asegúrate de que la ruta sea correcta
import logo from '../../assets/images/ImagenesMarca/1x/Mesa de trabajo 57.png';

const RegisterMascotaPage = () => {
  const { register, handleSubmit, setValue } = useForm();
  const [petTypes, setPetTypes] = useState([]);
  const [breeds, setBreeds] = useState([]);
  const [selectedPetType, setSelectedPetType] = useState('');

  useEffect(() => {
    const fetchPetTypes = async () => {
      const response = await fetch('/api/pet-types');
      const data = await response.json();
      setPetTypes(data);
    };
    fetchPetTypes();
  }, []);

  useEffect(() => {
    const fetchBreeds = async () => {
      if (selectedPetType) {
        const response = await fetch(`/api/breeds?petType=${selectedPetType}`);
        const data = await response.json();
        setBreeds(data);
      }
    };
    fetchBreeds();
  }, [selectedPetType]);

  const handlePetTypeChange = (e) => {
    setSelectedPetType(e.target.value);
    setValue("breed_id", ""); // Reset breed_id when pet type changes
  };

  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <div className="bg-[#ffffff] min-h-screen flex flex-col">



      {/* Contenido principal */}
      <div className="flex-grow p-6">

             {/* Header */}
      <header className="bg-[rgba(80,156,162,0.8)] p-4 flex justify-between items-center shadow-lg">
        <img src={logo} alt="Logo" className="h-10" />
       
        <nav className="space-x-4">
          <a href="/" className="text-white hover:underline">Inicio</a>
          <a href="/about" className="text-white hover:underline">iniciar sesion</a>
          <a href="/contact" className="text-white hover:underline">Contacto</a>
        </nav>
      </header>
        <div className="rounded-lg shadow-lg flex flex-row w-full h-full">
          {/* GIF Animation */}
          <div className="flex-none w-1/2 mr-4">
            <GifAnimation />
          </div>

          <div className="p-6 rounded-lg shadow-custom flex-grow m-[100px]">
            <form>
              <h1 className="text-2xl font-bold text-[#d55b49] mb-4">Registrar Mascota</h1>
              <div className="mb-4">
                <label htmlFor="name" className="block text-[#1a1a1a] mb-1">
                  <i className="fas fa-paw text-[#509ca2]"></i> Nombre:
                </label>
                <input
                  type="text"
                  id="name"
                  {...register("name", { required: true })}
                  required
                  className="shadow appearance-none border border-[#509ca2] rounded w-full py-2 px-3 text-[#1a1a1a] leading-tight focus:outline-none focus:shadow-outline"
                />
              </div>

              <div className="mb-4">
                <label htmlFor="petType" className="block text-[#1a1a1a] mb-1">
                  <i className="fas fa-paw text-[#509ca2]"></i> Tipo de mascota:
                </label>
                <select
                  id="petType"
                  value={selectedPetType}
                  onChange={handlePetTypeChange}
                  required
                  className="shadow appearance-none border border-[#509ca2] rounded w-full py-2 px-3 text-[#1a1a1a] leading-tight focus:outline-none focus:shadow-outline"
                >
                  <option value="">Seleccione un tipo de mascota</option>
                  {petTypes.map((type) => (
                    <option key={type.id} value={type.id}>
                      {type.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="mb-4">
                <label htmlFor="breed_id" className="block text-[#1a1a1a] mb-1">
                  <i className="fas fa-paw text-[#509ca2]"></i> Raza:
                </label>
                <select
                  id="breed_id"
                  {...register("breed_id", { required: true })}
                  required
                  disabled={!selectedPetType}
                  className="shadow appearance-none border border-[#509ca2] rounded w-full py-2 px-3 text-[#1a1a1a] leading-tight focus:outline-none focus:shadow-outline"
                >
                  <option value="">Seleccione una raza</option>
                  {breeds.map((breed) => (
                    <option key={breed.id} value={breed.id}>
                      {breed.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="mb-4">
                <label htmlFor="birthdate" className="block text-[#1a1a1a] mb-1">
                  <i className="fas fa-calendar-alt text-[#509ca2]"></i> Fecha de nacimiento:
                </label>
                <input
                  type="date"
                  id="birthdate"
                  {...register("birthdate", { required: true })}
                  required
                  className="shadow appearance-none border border-[#509ca2] rounded w-full py-2 px-3 text-[#1a1a1a] leading-tight focus:outline-none focus:shadow-outline"
                />
              </div>

              <div className="mb-4">
                <label htmlFor="gender" className="block text-[#1a1a1a] mb-1">
                  <i className="fas fa-venus-mars text-[#509ca2]"></i> Género:
                </label>
                <select
                  id="gender"
                  {...register("gender", { required: true })}
                  required
                  className="shadow appearance-none border border-[#509ca2] rounded w-full py-2 px-3 text-[#1a1a1a] leading-tight focus:outline-none focus:shadow-outline"
                >
                  <option value="">Seleccione un género</option>
                  <option value="male">Macho</option>
                  <option value="female">Hembra</option>
                </select>
              </div>

              <div className="mb-4">
                <label htmlFor="bio" className="block text-[#1a1a1a] mb-1">
                  <i className="fas fa-info-circle text-[#509ca2]"></i> Biografía:
                </label>
                <textarea
                  id="bio"
                  {...register("bio", { required: true })}
                  required
                  className="shadow appearance-none border border-[#509ca2] rounded w-full py-2 px-3 text-[#1a1a1a] leading-tight focus:outline-none focus:shadow-outline"
                ></textarea>
              </div>

              <button
                type="submit"
                className="bg-[#d55b49] hover:bg-[#509ca2] text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              >
                Registrar Mascota
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterMascotaPage;
