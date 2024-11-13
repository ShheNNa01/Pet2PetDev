import React, { useState } from 'react';
import '../styles/PasswordRecovery.css';

const PasswordRecovery = () => {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        setTimeout(() => {
            setMessage(`Se ha enviado un enlace de recuperación a ${email}`);
            setEmail(''); // Limpia el campo después de enviar
        }, 1000);
    };

    return (
        <div className="background">
            <div className="container">
                <h2>Recuperación de Contraseña</h2>
                <form onSubmit={handleSubmit} className="form">
                    <label className="label">Correo Electrónico:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        className="input"
                        placeholder="Ingresa tu correo"
                    />
                    <button type="submit" className="button">Enviar Enlace</button>
                </form>
                {message && <p className="message">{message}</p>}
            </div>
        </div>
    );
};

export default PasswordRecovery;
