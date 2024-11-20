import React, { useState } from 'react';
import { Alert, AlertTitle, AlertDescription } from '../ui/alert';
import { AuthService } from '../services/auth.service';
import { AlertTriangle, CheckCircle } from 'lucide-react';
import '../styles/PasswordRecovery.css';

const PasswordRecovery = () => {
    const [email, setEmail] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [alert, setAlert] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        
        try {
            await AuthService.requestPasswordReset(email);
            setAlert({
                type: 'success',
                title: '¡Correo enviado!',
                description: `Te hemos enviado un correo electrónico a ${email} con las instrucciones para restablecer tu contraseña. Por favor revisa tu bandeja de entrada y la carpeta de spam.`
            });
            setEmail('');
        } catch (error) {
            setAlert({
                type: 'destructive',
                title: 'Error',
                description: error.detail || 'Ocurrió un error al procesar tu solicitud. Por favor intenta nuevamente.'
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="background">
            <div className="container">
                <h2 className="text-2xl font-bold mb-6">Recuperación de Contraseña</h2>
                
                {alert && (
                    <Alert 
                        variant={alert.type}
                    >
                        {alert.type === 'destructive' ? (
                            <AlertTriangle className="h-4 w-4" />
                        ) : (
                            <CheckCircle className="h-4 w-4" />
                        )}
                        <AlertTitle>{alert.title}</AlertTitle>
                        <AlertDescription>
                            {alert.description}
                        </AlertDescription>
                    </Alert>
                )}

                <form onSubmit={handleSubmit} className="form">
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        className="input"
                        placeholder="Ingresa tu correo electrónico"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        className="button"
                        disabled={isLoading}
                    >
                        {isLoading ? 'Enviando...' : 'Enviar Enlace'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default PasswordRecovery;