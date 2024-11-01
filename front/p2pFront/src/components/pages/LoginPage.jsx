// src/pages/LoginPage.jsx
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authService } from '../services/auth.service';
import '../styles/LoginPage.css';
import MesaDeTrabajo50 from '../../assets/icons/Mesa de trabajo 50.png';

const LoginPage = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        usuario: '',
        password: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    // Manejar cambios en los inputs
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.id]: e.target.value
        });
        // Limpiar error cuando el usuario empiece a escribir
        if (error) setError('');
    };

    // Manejar el envío del formulario
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        // Validaciones básicas
        if (!formData.usuario.trim() || !formData.password.trim()) {
            setError('Por favor, completa todos los campos');
            setLoading(false);
            return;
        }

        try {
            const response = await authService.login({
                email: formData.usuario, // Asumiendo que el backend espera 'email'
                password: formData.password
            });

            // Guardar datos del usuario si es necesario
            if (response.user) {
                localStorage.setItem('userData', JSON.stringify(response.user));
            }

            // Redireccionar al dashboard o página principal
            navigate('/home');
        } catch (error) {
            // Manejar diferentes tipos de errores
            if (error.response?.status === 401) {
                setError('Usuario o contraseña incorrectos');
            } else if (error.response?.status === 422) {
                setError('Por favor, verifica tus credenciales');
            } else {
                setError('Error al iniciar sesión. Por favor, intenta más tarde');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div id="contenedor">
            <div id="contenedorcentrado">
                {/* Sección de login */}
                <div id="login">
                    <h2 className="titulo">Iniciar Sesión</h2>
                    
                    {/* Mostrar mensaje de error si existe */}
                    {error && (
                        <div className="error-mensaje">
                            {error}
                        </div>
                    )}

                    <form className='form-login' onSubmit={handleSubmit}>
                        <label htmlFor="usuario">Usuario:</label>
                        <input
                            type="text"
                            id="usuario"
                            placeholder="Introduce tu usuario"
                            value={formData.usuario}
                            onChange={handleChange}
                            disabled={loading}
                        />
                        
                        <label htmlFor="password">Contraseña:</label>
                        <input
                            type="password"
                            id="password"
                            placeholder="Introduce tu contraseña"
                            value={formData.password}
                            onChange={handleChange}
                            disabled={loading}
                        />
                        
                        <button 
                            type="submit" 
                            disabled={loading}
                            className={loading ? 'button-loading' : ''}
                        >
                            {loading ? 'Ingresando...' : 'Ingresar'}
                        </button>
                    </form>

                    <div className="pie-form">
                        <Link to="/forgot-password">¿Olvidaste tu contraseña?</Link>
                        <Link to="/register">Regístrate</Link>
                    </div>
                </div>

                {/* Sección de la derecha */}
                <div id="derecho">
                    <div className="logo-empresa">
                        <img src={MesaDeTrabajo50} alt="Logo Empresa" />
                    </div>
                    <hr />
                    <div className="pie-form">
                        <p>
                            ¡Bienvenido! <br />
                            Aquí, las mejores conexiones entre mascotas y dueños comienzan. <br />
                            ¡Explora lo que tenemos para ti!
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
