import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardTitle } from "../ui/card";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import Label from "../ui/label";
import { Loader2 } from "lucide-react";
import { petService } from '../services/petService';
import { toast } from '../ui/use-toast';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";

const EditPet = () => {
  const navigate = useNavigate();
  const { search, state } = useLocation();
  const petId = new URLSearchParams(search).get('id') || state?.petId;

  const [form, setForm] = useState({
    name: "",
    breed: "",
    birthdate: "",
    gender: "",
    bio: "",
    pet_type: "",
    pet_picture: ""
  });
  
  const [filteredBreeds, setFilteredBreeds] = useState([]);
  const [profilePicPreview, setProfilePicPreview] = useState("");
  const [loading, setLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    const loadPetData = async () => {
      if (!petId) {
        toast({ 
          variant: "destructive", 
          description: "No se encontró la información de la mascota" 
        });
        navigate('/');
        return;
      }

      try {
        setLoading(true);
        const [petData, breedsData] = await Promise.all([
          petService.getPetById(petId),
          petService.getBreeds()
        ]);
        
        const petBreed = breedsData.find(b => b.breed_id === petData.breed_id);
        
        setForm({
          ...petData,
          breed: petData.breed_id.toString(),
          pet_type: petBreed?.pet_type?.type_name || "No especificado",
          gender: petData.gender || ""
        });
        
        setProfilePicPreview(petData.pet_picture);
        setFilteredBreeds(breedsData.filter(breed => breed.pet_type_id === petBreed?.pet_type_id));
      } catch (error) {
        toast({
          variant: "destructive",
          description: "No se pudo cargar la información de la mascota"
        });
        navigate('/pets');
      } finally {
        setLoading(false);
      }
    };

    loadPetData();
  }, [petId, navigate]);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validar tamaño (5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast({
        variant: "destructive",
        description: "La imagen no debe superar los 5MB"
      });
      return;
    }

    try {
      setLoading(true);
      // Usar el endpoint para subir la imagen
      await petService.uploadPetImage(petId, file);
      
      // Mostrar la imagen nueva
      setProfilePicPreview(URL.createObjectURL(file));
      toast({ description: "Imagen actualizada correctamente" });
    } catch (error) {
      toast({
        variant: "destructive",
        description: "No se pudo subir la imagen"
      });
    } finally {
      setLoading(false);
    }
};

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!form.name?.trim() || !form.breed || !form.birthdate || !form.gender) {
      toast({
        variant: "destructive",
        description: "Por favor complete todos los campos requeridos"
      });
      return;
    }

    try {
      setLoading(true);
      await petService.updatePet(petId, {
        name: form.name.trim(),
        breed_id: parseInt(form.breed),
        birthdate: form.birthdate,
        gender: form.gender,
        bio: form.bio?.trim() || "",
        status: true
      });
      
      toast({ description: "Mascota actualizada exitosamente" });
      navigate(`/petProfile?id=${petId}`);
    } catch (error) {
      toast({
        variant: "destructive",
        description: "Error al actualizar los datos de la mascota"
      });
    } finally {
      setLoading(false);
      setIsEditing(false);
    }
  };

  if (loading && !form.name) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#eeede8]">
        <Loader2 className="h-8 w-8 animate-spin text-[#509ca2]" />
      </div>
    );
  }

  const formFields = [
    { id: "pet_type", label: "Tipo de Mascota", disabled: true },
    { id: "name", label: "Nombre", placeholder: "Nombre de la mascota" },
    {
      id: "breed",
      label: "Raza",
      type: "select",
      options: filteredBreeds.map(breed => ({
        value: breed.breed_id.toString(),
        label: breed.breed_name
      }))
    },
    { id: "birthdate", label: "Fecha de Nacimiento", type: "date" },
    {
      id: "gender",
      label: "Género",
      type: "select",
      options: [
        { value: "male", label: "Macho" },
        { value: "female", label: "Hembra" }
      ]
    },
    { id: "bio", label: "Descripción", placeholder: "Descripción de la mascota" }
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-[#eeede8] p-8">
      <Card className="w-full md:max-w-4xl bg-white p-6 rounded-lg shadow-xl border border-gray-300">
        <CardHeader className="text-center mb-6">
          <CardTitle className="text-3xl font-semibold text-[#509ca2]">
            {isEditing ? 'Editando perfil de ' : 'Perfil de '} {form.name || "Mascota"}
          </CardTitle>
        </CardHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="flex justify-center relative">
            <div className="w-60 h-60 rounded-full border-4 border-[#509ca2] overflow-hidden shadow-lg">
              <img 
                src={profilePicPreview || "/default-pet.jpg"} 
                alt="Foto de perfil" 
                className="w-full h-full object-cover"
                onError={(e) => e.target.src = "/default-pet.jpg"}
              />
            </div>
          </div>

          {isEditing && (
            <input 
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="w-full p-4 border-2 border-gray-300 rounded-md text-lg"
            />
          )}

          {formFields.map(field => (
            <div key={field.id}>
              <Label className="block text-xl font-medium text-[#1a1a1a] mb-3">
                {field.label}
              </Label>
              {field.type === "select" ? (
                <Select
                  value={form[field.id]}
                  onValueChange={(value) => setForm(prev => ({ ...prev, [field.id]: value }))}
                  disabled={!isEditing || field.disabled}
                >
                  <SelectTrigger className="w-full p-4 border-2 border-gray-300 rounded-md text-lg">
                    <SelectValue placeholder={`Selecciona ${field.label.toLowerCase()}`} />
                  </SelectTrigger>
                  <SelectContent>
                    {field.options.map(option => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              ) : (
                <Input
                  type={field.type || "text"}
                  value={form[field.id] || ""}
                  onChange={(e) => setForm(prev => ({ ...prev, [field.id]: e.target.value }))}
                  className="w-full p-4 border-2 border-gray-300 rounded-md text-lg"
                  placeholder={field.placeholder}
                  disabled={!isEditing || field.disabled}
                  max={field.type === "date" ? new Date().toISOString().split('T')[0] : undefined}
                />
              )}
            </div>
          ))}

          <div className="flex justify-center space-x-4">
            {loading ? (
              <Loader2 className="h-8 w-8 animate-spin text-[#509ca2]" />
            ) : isEditing ? (
              <>
                <Button 
                  type="button"
                  onClick={() => setIsEditing(false)}
                  variant="outline"
                  className="bg-gray-300 text-gray-700 py-2 px-4 rounded-lg"
                >
                  Cancelar
                </Button>
                <Button 
                  type="submit"
                  className="bg-[#509ca2] text-white py-2 px-4 rounded-lg"
                >
                  Guardar Cambios
                </Button>
              </>
            ) : (
              <Button 
                type="button"
                onClick={() => setIsEditing(true)}
                className="bg-[#509ca2] text-white py-2 px-4 rounded-lg"
              >
                Editar
              </Button>
            )}
          </div>
        </form>
      </Card>
    </div>
  );
};

export default EditPet;