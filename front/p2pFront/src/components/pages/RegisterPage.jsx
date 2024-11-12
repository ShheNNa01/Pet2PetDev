import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../services/auth.service';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Alert, AlertTitle, AlertDescription } from '../ui/alert';
import { XCircle } from 'lucide-react';
import EmailVerificationPage from './EmailVerificationPage';
import '../styles/RegisterPage.css';

export default function RegisterPage() {
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [error, setError] = useState('');
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
      setError(''); // Limpiar error anterior
      await AuthService.register({
        ownerName: data.ownerName,
        ownerLastName: data.ownerLastName,
        correo: data.correo,
        contrasena: data.contrasena
      });
      setShowConfirmation(true);
    } catch (error) {
      setError(error.message || "Error al registrar el usuario");
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  if (showConfirmation) {
    return <EmailVerificationPage email={watch("correo")} />;
  }

  return (
    <div className="container-register">
      <div className="container-form max-w-md mx-auto">
        {error && (
          <Alert variant="destructive" className="mb-4">
            <XCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="form-container space-y-6 bg-white p-6 rounded-lg shadow-sm">
          <h1 className="text-center text-2xl font-bold text-primary">Registrarse</h1>
          
          <h3 className="text-lg font-semibold text-foreground">Datos del Dueño</h3>
          
          <div className="space-y-2">
            <label className="text-sm font-medium text-foreground">
              Nombre
            </label>
            <Input
              {...register("ownerName", {
                required: "El nombre es obligatorio"
              })}
              type="text"
              placeholder="Ingrese su nombre"
              className={errors.ownerName ? "border-destructive" : ""}
            />
            {errors.ownerName && (
              <p className="text-sm text-destructive">{errors.ownerName.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-foreground">
              Apellido
            </label>
            <Input
              {...register("ownerLastName", {
                required: "El apellido es obligatorio"
              })}
              type="text"
              placeholder="Ingrese su apellido"
              className={errors.ownerLastName ? "border-destructive" : ""}
            />
            {errors.ownerLastName && (
              <p className="text-sm text-destructive">{errors.ownerLastName.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-foreground">
              Correo Electrónico
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
              className={errors.correo ? "border-destructive" : ""}
            />
            {errors.correo && (
              <p className="text-sm text-destructive">{errors.correo.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-foreground">
              Contraseña
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
              className={errors.contrasena ? "border-destructive" : ""}
            />
            {errors.contrasena && (
              <p className="text-sm text-destructive">{errors.contrasena.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-foreground">
              Confirmar Contraseña
            </label>
            <Input
              {...register("contrasena2", {
                required: "La confirmación de contraseña es obligatoria",
                validate: value => 
                  value === contrasena || "Las contraseñas no coinciden"
              })}
              type="password"
              placeholder="Confirme su contraseña"
              className={errors.contrasena2 ? "border-destructive" : ""}
            />
            {errors.contrasena2 && (
              <p className="text-sm text-destructive">{errors.contrasena2.message}</p>
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
            <label htmlFor="termsCheck" className="text-sm text-muted-foreground">
              Acepto los términos y condiciones
            </label>
          </div>
          {errors.terms && (
            <p className="text-sm text-destructive">{errors.terms.message}</p>
          )}

          <Button 
            type="submit" 
            className="w-full bg-primary hover:bg-primary/90"
          >
            Registrarse
          </Button>
        </form>
      </div>
    </div>
  );
}