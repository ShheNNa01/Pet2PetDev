// src/utils/passwordValidation.js

// Lista de caracteres especiales permitidos
const SPECIAL_CHARS = '!@#$%^&*()-_=+[]{}|;:,.<>?';

// Mensaje con los caracteres especiales permitidos
const getSpecialCharsMessage = () => {
    return `Caracteres especiales permitidos: ${SPECIAL_CHARS.split('').join(' ')}`;
};

export const passwordRequirements = [
    { 
        label: "Al menos 8 caracteres", 
        test: (pass) => pass.length >= 8 
    },
    { 
        label: "Al menos una mayúscula (A-Z)", 
        test: (pass) => /[A-Z]/.test(pass) 
    },
    { 
        label: "Al menos una minúscula (a-z)", 
        test: (pass) => /[a-z]/.test(pass) 
    },
    { 
        label: "Al menos un número (0-9)", 
        test: (pass) => /\d/.test(pass) 
    },
    { 
        label: `Al menos un carácter especial (${SPECIAL_CHARS})`, 
        test: (pass) => new RegExp(`[${SPECIAL_CHARS.replace(/[-[\]{}()*+?.,\\^$|]/g, '\\$&')}]`).test(pass)
    }
];

export const validatePassword = (value) => {
    const errors = [];
    
    if (value.length < 8) {
        errors.push("La contraseña debe tener al menos 8 caracteres");
    }
    if (!/[A-Z]/.test(value)) {
        errors.push("La contraseña debe contener al menos una mayúscula");
    }
    if (!/[a-z]/.test(value)) {
        errors.push("La contraseña debe contener al menos una minúscula");
    }
    if (!/\d/.test(value)) {
        errors.push("La contraseña debe contener al menos un número");
    }
    if (!new RegExp(`[${SPECIAL_CHARS.replace(/[-[\]{}()*+?.,\\^$|]/g, '\\$&')}]`).test(value)) {
        errors.push(`La contraseña debe contener al menos uno de los siguientes caracteres especiales: ${SPECIAL_CHARS}`);
    }
    
    return {
        isValid: errors.length === 0,
        errors,
        strength: calculatePasswordStrength(value)
    };
};

export const calculatePasswordStrength = (password) => {
    let strength = 0;
    
    // Longitud
    if (password.length >= 8) strength += 20;
    
    // Mayúsculas
    if (/[A-Z]/.test(password)) strength += 20;
    
    // Minúsculas
    if (/[a-z]/.test(password)) strength += 20;
    
    // Números
    if (/\d/.test(password)) strength += 20;
    
    // Caracteres especiales
    if (new RegExp(`[${SPECIAL_CHARS.replace(/[-[\]{}()*+?.,\\^$|]/g, '\\$&')}]`).test(password)) strength += 20;

    return strength;
};

// Función auxiliar para verificar si un carácter es especial
export const isSpecialChar = (char) => {
    return SPECIAL_CHARS.includes(char);
};