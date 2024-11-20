import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../services/auth.service';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Alert, AlertTitle, AlertDescription } from '../ui/alert';
import { XCircle, User, Mail, Check } from 'lucide-react';
import { PasswordInput } from '../common/PasswordInput';
import { validatePassword } from '../utils/passwordValidation';
import EmailVerificationPage from './EmailVerificationPage';
import '../styles/RegisterPage.css';

// Componente reutilizable para los inputs
const FormInput = ({ label, error, register, name, type = "text", placeholder, validation }) => {
  return (
    <div className="space-y-2 w-full">
      <label className="text-sm font-medium text-gray-700">
        {label}
      </label>
      <div className="relative">
        <Input
          {...register(name, validation)}
          type={type}
          placeholder={placeholder}
          className={`w-full px-4 py-3 rounded-lg border 
                    ${error ? 'border-[#d55b49]' : 'border-gray-300'} 
                    focus:ring-2 focus:ring-[#509ca2] focus:border-transparent 
                    transition-all bg-white/50 backdrop-blur-sm`}
        />
      </div>
      {error && (
        <p className="text-sm text-[#d55b49]">{error.message}</p>
      )}
    </div>
  );
};

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
      setError('');
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
    <div className="container-register min-h-screen py-8">
      <div className="container-form max-w-md mx-auto">
        {error && (
          <Alert variant="destructive" className="mb-4 bg-[#d55b49]/10 border-[#d55b49]">
            <XCircle className="h-4 w-4 text-[#d55b49]" />
            <AlertTitle className="text-[#d55b49]">Error</AlertTitle>
            <AlertDescription className="text-[#d55b49]">{error}</AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 bg-white/90 backdrop-blur-sm p-8 rounded-xl shadow-lg">
          <h1 className="text-center text-3xl font-bold text-[#d55b49] mb-6">Registrarse</h1>
          
          <h3 className="text-xl font-semibold text-[#509ca2] w-full text-left border-b border-[#509ca2]/20 pb-2">
            Datos del Dueño
          </h3>
          
          <FormInput
            label="Nombre"
            name="ownerName"
            error={errors.ownerName}
            register={register}
            placeholder="Ingrese su nombre"
            validation={{
              required: "El nombre es obligatorio"
            }}
          />

          <FormInput
            label="Apellido"
            name="ownerLastName"
            error={errors.ownerLastName}
            register={register}
            placeholder="Ingrese su apellido"
            validation={{
              required: "El apellido es obligatorio"
            }}
          />

          <FormInput
            label="Correo Electrónico"
            name="correo"
            type="email"
            error={errors.correo}
            register={register}
            placeholder="ejemplo@correo.com"
            validation={{
              required: "El correo es obligatorio",
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: "Correo electrónico inválido"
              }
            }}
          />

          <PasswordInput
            register={register}
            name="contrasena"
            label="Contraseña"
            error={errors.contrasena}
            placeholder="Ingrese su contraseña"
            validate={{
              required: "La contraseña es obligatoria",
              validate: (value) => {
                const validation = validatePassword(value);
                return validation.isValid || validation.errors[0];
              }
            }}
          />

          <PasswordInput
            register={register}
            name="contrasena2"
            label="Confirmar Contraseña"
            error={errors.contrasena2}
            placeholder="Confirme su contraseña"
            validate={{
              required: "La confirmación de contraseña es obligatoria",
              validate: value => 
                value === contrasena || "Las contraseñas no coinciden"
            }}
            showRequirements={false}
          />
          
          <div className="flex items-center space-x-3 bg-gray-50 p-3 rounded-lg">
            <input
              type="checkbox"
              id="termsCheck"
              {...register("terms", { 
                required: "Debes aceptar los términos y condiciones" 
              })}
              className="h-4 w-4 rounded border-gray-300 text-[#509ca2] 
                        focus:ring-[#509ca2] transition-colors"
            />
            <label htmlFor="termsCheck" className="text-sm text-gray-600">
              Acepto los términos y condiciones
            </label>
          </div>
          {errors.terms && (
            <p className="text-sm text-[#d55b49] mt-1">{errors.terms.message}</p>
          )}

          <Button 
            type="submit" 
            className="w-full py-3 bg-[#d55b49] hover:bg-[#509ca2] text-white rounded-lg 
                      transition-all transform hover:scale-[1.02] active:scale-[0.98]
                      text-lg font-semibold shadow-md"
          >
            Registrarse
          </Button>
        </form>
      </div>
    </div>
  );
}