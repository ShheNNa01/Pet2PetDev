import React from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../services/auth.service';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import '../styles/RegisterPage.css';

export default function RegisterPage() {
  const { register, handleSubmit, watch, formState: { errors } } = useForm({
    defaultValues: {
      ownerName: '',
      ownerLastName: '',
      correo: '',
      contrasena: '',
      contrasena2: '',
      terms: false
    }
  });
  
  const navigate = useNavigate();
  const contrasena = watch("contrasena");

  async function onSubmit(data) {
    try {
      await AuthService.register({
        ownerName: data.ownerName,
        ownerLastName: data.ownerLastName,
        correo: data.correo,
        contrasena: data.contrasena
      });
      alert("Registro exitoso");
      navigate('/welcome');
    } catch (error) {
      alert("Error al registrar el usuario");
    }
  }

  return (
    <div className="container-register">
      <div className="container-form">
        <form onSubmit={handleSubmit(onSubmit)} className="form-container space-y-4">
          <h1 className="text-center heading-register text-2xl font-bold">Registrarse</h1>
          
          <h3 className="text-lg font-semibold">Datos del Dueño</h3>
          
          <div className="space-y-2">
            <label className="text-sm font-medium">
              <i className="fas fa-user"></i> Nombre
            </label>
            <Input
              {...register("ownerName", {
                required: "El nombre es obligatorio"
              })}
              type="text"
              placeholder="Ingrese su nombre"
              className={errors.ownerName ? "border-red-500" : ""}
            />
            {errors.ownerName && (
              <p className="text-sm text-red-500">{errors.ownerName.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">
              <i className="fas fa-user"></i> Apellido
            </label>
            <Input
              {...register("ownerLastName", {
                required: "El apellido es obligatorio"
              })}
              type="text"
              placeholder="Ingrese su apellido"
              className={errors.ownerLastName ? "border-red-500" : ""}
            />
            {errors.ownerLastName && (
              <p className="text-sm text-red-500">{errors.ownerLastName.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">
              <i className="fas fa-envelope"></i> Correo Electrónico
            </label>
            <Input
              {...register("correo", {
                required: "El correo es obligatorio",
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: "Correo electrónico inválido"
                }
              })}
              type="email"
              placeholder="ejemplo@correo.com"
              className={errors.correo ? "border-red-500" : ""}
            />
            {errors.correo && (
              <p className="text-sm text-red-500">{errors.correo.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">
              <i className="fas fa-lock"></i> Contraseña
            </label>
            <Input
              {...register("contrasena", {
                required: "La contraseña es obligatoria",
                minLength: {
                  value: 6,
                  message: "La contraseña debe tener al menos 6 caracteres"
                }
              })}
              type="password"
              placeholder="Ingrese su contraseña"
              className={errors.contrasena ? "border-red-500" : ""}
            />
            {errors.contrasena && (
              <p className="text-sm text-red-500">{errors.contrasena.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">
              <i className="fas fa-lock"></i> Confirmar Contraseña
            </label>
            <Input
              {...register("contrasena2", {
                required: "La confirmación de contraseña es obligatoria",
                validate: value => 
                  value === contrasena || "Las contraseñas no coinciden"
              })}
              type="password"
              placeholder="Confirme su contraseña"
              className={errors.contrasena2 ? "border-red-500" : ""}
            />
            {errors.contrasena2 && (
              <p className="text-sm text-red-500">{errors.contrasena2.message}</p>
            )}
          </div>
          
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="termsCheck"
              {...register("terms", { 
                required: "Debes aceptar los términos y condiciones" 
              })}
              className="h-4 w-4 rounded border-gray-300"
            />
            <label htmlFor="termsCheck" className="text-sm text-gray-600">
              Acepto los términos y condiciones
            </label>
          </div>
          {errors.terms && (
            <p className="text-sm text-red-500">{errors.terms.message}</p>
          )}

          <Button 
            type="submit" 
            className="w-full"
          >
            Registrarse
          </Button>
        </form>
      </div>
    </div>
  );
}