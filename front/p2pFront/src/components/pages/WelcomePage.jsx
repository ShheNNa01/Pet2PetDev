import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "../ui/card";
import { Button } from "../ui/button";
import { PawPrint, Search, Heart } from "lucide-react";
import logo from '../../assets/icons/Mesa de trabajo 54.png';

export default function WelcomePage() {
    return (
        <div className="min-h-screen bg-gradient-to-b from-blue-50 to-green-50 flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-6xl space-y-8">
                <div className="text-center space-y-4">
                    <div className="w-32 h-32 bg-white rounded-full mx-auto flex items-center justify-center shadow-md">
                        <img src={logo} alt="Logo de Pet2Pet" className="h-24 w-24" />
                    </div>
                    <h1 className="text-4xl font-bold text-blue-600">¡Bienvenido a PET2PET!</h1>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {/* Tarjeta para Registrar mascota */}
                    <Card className="overflow-hidden transition-all duration-300 hover:shadow-xl hover:scale-105">
                        <CardHeader className="p-0">
                            <Button
                                className="w-full h-full p-6 flex flex-col items-center justify-center space-y-4 bg-white hover:bg-blue-50 transition-colors"
                                variant="ghost"
                            >
                                <PawPrint className="w-16 h-16 text-blue-500" />
                                <div className="space-y-2 text-center">
                                    <CardTitle className="text-xl font-semibold text-gray-800">Registrar mi mascota</CardTitle>
                                    <p className="text-sm text-gray-600">
                                        Comparte el perfil de tu mascota en nuestra comunidad
                                    </p>
                                </div>
                            </Button>
                        </CardHeader>
                    </Card>
                    {/* Tarjeta para Adoptar */}
                    {/* <Card className="overflow-hidden transition-all duration-300 hover:shadow-xl hover:scale-105">
                        <CardHeader className="p-0">
                            <Button
                                className="w-full h-full p-6 flex flex-col items-center justify-center space-y-4 bg-white hover:bg-green-50 transition-colors"
                                variant="ghost"
                            >
                                <Search className="w-16 h-16 text-green-500" />
                                <div className="space-y-2 text-center">
                                    <CardTitle className="text-xl font-semibold text-gray-800">Estoy buscando adoptar</CardTitle>
                                    <p className="text-sm text-gray-600">
                                        Encuentra un nuevo compañero para tu hogar
                                    </p>
                                </div>
                            </Button>
                        </CardHeader>
                    </Card> */}
                    {/* Tarjeta para Amantes de mascotas */}
                    <Card className="overflow-hidden transition-all duration-300 hover:shadow-xl hover:scale-105">
                        <CardHeader className="p-0">
                            <Button
                                className="w-full h-full p-6 flex flex-col items-center justify-center space-y-4 bg-white hover:bg-purple-50 transition-colors"
                                variant="ghost"
                            >
                                <Heart className="w-16 h-16 text-purple-500" />
                                <div className="space-y-2 text-center">
                                    <CardTitle className="text-xl font-semibold text-gray-800">Explorar como amante de las mascotas</CardTitle>
                                    <p className="text-sm text-gray-600">
                                        Conoce nuestra comunidad
                                    </p>
                                    <p className="text-xs text-gray-500">
                                        Soy consciente de que no podré publicar ni comentar
                                    </p>
                                </div>
                            </Button>
                        </CardHeader>
                    </Card>
                </div>
            </div>
        </div>
    );
}
