import React from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../services/auth.service';
import Button from '../common/Button';
import Input from '../common/Input';
import '../styles/RegisterPage.css';

export default function RegisterPage() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const navigate = useNavigate();

  async function onSubmit(data) {
    try {
      await AuthService.register({
        ownerName: data.ownerName,
        ownerLastName: data.ownerLastName,
        correo: data.correo,
        contrasena: data.contrasena
      });
      alert("Registro exitoso");
      navigate('/welcome'); // Redirige a la página de bienvenida
    } catch (error) {
      alert("Error al registrar el usuario");
    }
  }

  return (
    <div className="container-register">
      <div className="container-form">
        <form onSubmit={handleSubmit(onSubmit)} className="form-container">
          <h1 className="text-center heading-register">Registrarse</h1>
          
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

          <div className="mb-3 form-check">
            <input
              type="checkbox"
              className="form-check-input"
              id="termsCheck"
              {...register("terms", { required: true })}
            />
            <label className="form-check-label" htmlFor="termsCheck">
              Acepto los términos y condiciones
            </label>
            {errors.terms && <p className="text-danger">Debes aceptar los términos</p>}
          </div>

          <Button type="submit" text="Registrarse" />
        </form>
      </div>
    </div>
  );
}
