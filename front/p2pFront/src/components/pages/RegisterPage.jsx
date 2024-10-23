import React from 'react';
import { useForm } from 'react-hook-form';
import { registerUser } from '../services/userService';
import Button from '../common/Button';
import Input from '../common/Input';
import '../styles/RegisterPage.css'; // Importar el archivo CSS

export default function RegisterPage() {
  const { register, handleSubmit, formState: { errors } } = useForm();

  async function onSubmit(data) {
    try {
      const response = await registerUser(data);
      alert("Registro exitoso: " + response.nombre);
    } catch (error) {
      alert("Error al registrar el usuario");
    }
  }

  return (
    <div className="container-register">
      <div className='container-form'>
        <h1 className='text-center heading-register'>Registrarse</h1>
        <div className='container'>
          <div className='row justify-content-center'>
            <div className='col-sm-6'>
              <form onSubmit={handleSubmit(onSubmit)} className='form-container'>
                
                {/* Datos del dueño */}
                <h3>Datos del Dueño</h3>
                <Input
                  label="Nombre"
                  name="ownerName"
                  type="text"
                  register={register}
                  required
                  errorMessage="El nombre es obligatorio"
                />
                <Input
                  label="Apellido"
                  name="ownerLastName"
                  type="text"
                  register={register}
                  required
                  errorMessage="El apellido es obligatorio"
                />
                <Input
                  label="Correo Electrónico"
                  name="correo"
                  type="email"
                  register={register}
                  required
                  errorMessage="El correo es obligatorio"
                />
                <Input
                  label="Contraseña"
                  name="contrasena"
                  type="password"
                  register={register}
                  required
                  errorMessage="La contraseña es obligatoria"
                />
                
                {/* Datos de la mascota */}
                <h3>Datos de la Mascota</h3>
                <Input
                  label="Nombre de la Mascota"
                  name="petName"
                  type="text"
                  register={register}
                  required
                  errorMessage="El nombre de la mascota es obligatorio"
                />
                <Input
                  label="Especie"
                  name="petSpecies"
                  type="text"
                  register={register}
                  required
                  errorMessage="La especie es obligatoria"
                />
                <Input
                  label="Raza"
                  name="petBreed"
                  type="text"
                  register={register}
                  required
                  errorMessage="La raza es obligatoria"
                />
                <Input
                  label="Edad"
                  name="petAge"
                  type="number"
                  register={register}
                  required
                  errorMessage="La edad de la mascota es obligatoria"
                />
                
                {/* Aceptación de términos */}
                <div className="mb-3 form-check">
                  <input
                    type="checkbox"
                    className="form-check-input"
                    id="termsCheck"
                    {...register("terms", { required: true })}
                  />
                  <label className="form-check-label" htmlFor="termsCheck">Acepto los términos y condiciones</label>
                  {errors.terms && <p className="text-danger">Debes aceptar los términos</p>}
                </div>

                <Button type="submit" text="Submit" />
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
