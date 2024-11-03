    // Footer.jsx
    import React from 'react';
    import { 
    Heart, 
    PawPrint, 
    Mail, 
    Phone, 
    MapPin, 
    Instagram, 
    Facebook, 
    Twitter, 
    Youtube,
    ShieldCheck,
    Users,
    HelpCircle,
    Star
    } from 'lucide-react';

    export default function Footer() {
    return (
        <footer className="bg-white mt-12">
        {/* Top section with main content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* About section */}
            <div className="space-y-4">
                <h3 className="text-lg font-semibold text-[#d55b49] flex items-center gap-2">
                <PawPrint className="h-5 w-5" />
                Sobre Pet2Pet
                </h3>
                <p className="text-sm text-gray-600">
                Conectando mascotas y sus humanos desde 2024. Creando una comunidad global de amantes de las mascotas.
                </p>
                <div className="flex space-x-4">
                <a href="#" className="text-[#509ca2] hover:text-[#d55b49] transition-colors">
                    <Instagram className="h-5 w-5" />
                </a>
                <a href="#" className="text-[#509ca2] hover:text-[#d55b49] transition-colors">
                    <Facebook className="h-5 w-5" />
                </a>
                <a href="#" className="text-[#509ca2] hover:text-[#d55b49] transition-colors">
                    <Twitter className="h-5 w-5" />
                </a>
                <a href="#" className="text-[#509ca2] hover:text-[#d55b49] transition-colors">
                    <Youtube className="h-5 w-5" />
                </a>
                </div>
            </div>

            {/* Features & Services */}
            <div className="space-y-4">
                <h3 className="text-lg font-semibold text-[#d55b49] flex items-center gap-2">
                <Star className="h-5 w-5" />
                Servicios
                </h3>
                <ul className="space-y-2 text-sm">
                <li>
                    <a href="#" className="text-gray-600 hover:text-[#509ca2] transition-colors flex items-center gap-2">
                    <Users className="h-4 w-4" />
                    Comunidad de Mascotas
                    </a>
                </li>
                <li>
                    <a href="#" className="text-gray-600 hover:text-[#509ca2] transition-colors flex items-center gap-2">
                    <Heart className="h-4 w-4" />
                    Adopciones Responsables
                    </a>
                </li>
                <li>
                    <a href="#" className="text-gray-600 hover:text-[#509ca2] transition-colors flex items-center gap-2">
                    <ShieldCheck className="h-4 w-4" />
                    Veterinarios Certificados
                    </a>
                </li>
                <li>
                    <a href="#" className="text-gray-600 hover:text-[#509ca2] transition-colors flex items-center gap-2">
                    <HelpCircle className="h-4 w-4" />
                    Consejos y Cuidados
                    </a>
                </li>
                </ul>
            </div>

            {/* Contact Info */}
            <div className="space-y-4">
                <h3 className="text-lg font-semibold text-[#d55b49] flex items-center gap-2">
                <Mail className="h-5 w-5" />
                Contáctanos
                </h3>
                <ul className="space-y-2 text-sm">
                <li className="flex items-center gap-2 text-gray-600">
                    <Phone className="h-4 w-4 text-[#509ca2]" />
                    +57 (123) 456-7890
                </li>
                <li className="flex items-center gap-2 text-gray-600">
                    <Mail className="h-4 w-4 text-[#509ca2]" />
                    contacto@pet2pet.com
                </li>
                <li className="flex items-center gap-2 text-gray-600">
                    <MapPin className="h-4 w-4 text-[#509ca2]" />
                    Bogotá, Colombia
                </li>
                </ul>
            </div>

            {/* Newsletter */}
            <div className="space-y-4">
                <h3 className="text-lg font-semibold text-[#d55b49]">Mantente Conectado</h3>
                <p className="text-sm text-gray-600">
                Recibe las últimas novedades sobre mascotas y eventos.
                </p>
                <div className="flex gap-2">
                <input 
                    type="email" 
                    placeholder="Tu correo electrónico"
                    className="flex-1 px-3 py-2 text-sm border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-[#509ca2] focus:border-transparent"
                />
                <button className="px-4 py-2 bg-[#509ca2] text-white rounded-md text-sm hover:bg-[#509ca2]/90 transition-colors">
                    Suscribir
                </button>
                </div>
            </div>
            </div>
        </div>

        {/* Bottom section with copyright */}
        <div className="border-t border-gray-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex flex-col md:flex-row justify-between items-center">
                <div className="text-sm text-gray-500 mb-4 md:mb-0">
                © 2024 Pet2Pet. Todos los derechos reservados.
                </div>
                <div className="flex space-x-6">
                <a href="#" className="text-sm text-gray-500 hover:text-[#509ca2] transition-colors">
                    Privacidad
                </a>
                <a href="#" className="text-sm text-gray-500 hover:text-[#509ca2] transition-colors">
                    Términos
                </a>
                <a href="#" className="text-sm text-gray-500 hover:text-[#509ca2] transition-colors">
                    Cookies
                </a>
                <a href="#" className="text-sm text-gray-500 hover:text-[#509ca2] transition-colors">
                    Contacto
                </a>
                </div>
            </div>
            </div>
        </div>
        </footer>
    );
    }