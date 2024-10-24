import React from 'react';
import { useForm } from 'react-hook-form';
import { registerUser } from '../services/userService';
import Button from '../common/Button';
import Input from '../common/Input';
import '../styles/RegisterPage.css';

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
        <form onSubmit={handleSubmit(onSubmit)} className='form-container'>
          <h1 className='text-center heading-register'>Registrarse</h1>
          
          <h3>Datos del Dueño</h3>
          <Input
            label={<><i className="fas fa-user"></i> Nombre</>}
            name="ownerName"
            type="text"
            register={register}
            required
            errorMessage="El nombre es obligatorio"
          />
          <Input
            label={<><i className="fas fa-user"></i> Apellido</>}
            name="ownerLastName"
            type="text"
            register={register}
            required
            errorMessage="El apellido es obligatorio"
          />
          <Input
            label={<><i className="fas fa-envelope"></i> Correo Electrónico</>}
            name="correo"
            type="email"
            register={register}
            required
            errorMessage="El correo es obligatorio"
          />
          <Input
            label={<><i className="fas fa-lock"></i> Contraseña</>}
            name="contrasena"
            type="password"
            register={register}
            required
            errorMessage="La contraseña es obligatoria"
          />
          
          <h3>Datos de la Mascota</h3>
          <Input
            label={<><i className="fas fa-paw"></i> Nombre de la Mascota</>}
            name="petName"
            type="text"
            register={register}
            required
            errorMessage="El nombre de la mascota es obligatorio"
          />
          <Input
            label={<><i className="fas fa-dog"></i> Especie</>}
            name="petSpecies"
            type="text"
            register={register}
            required
            errorMessage="La especie es obligatoria"
          />
          <Input
            label={<><i className="fas fa-bone"></i> Raza</>}
            name="petBreed"
            type="text"
            register={register}
            required
            errorMessage="La raza es obligatoria"
          />
          <Input
            label={<><i className="fas fa-calendar-alt"></i> Edad</>}
            name="petAge"
            type="number"
            register={register}
            required
            errorMessage="La edad de la mascota es obligatoria"
          />
          
          <div className="mb-3 form-check">
            <input
              type="checkbox"
              className="form-check-input"
              id="termsCheck"
              {...register("terms", { required: true })}
            />
            <label className="form-check-label" htmlFor="termsCheck">
              <i className="fas fa-check-square"></i> Acepto los términos y condiciones
            </label>
            {errors.terms && <p className="text-danger">Debes aceptar los términos</p>}
          </div>

          <Button type="submit" text="Submit" />
        </form>
      </div>
    </div>
  );
}
