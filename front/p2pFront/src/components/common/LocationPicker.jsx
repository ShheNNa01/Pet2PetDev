import React, { useState } from 'react';
import { MapPin } from 'lucide-react';

export default function LocationPicker({ onLocationSelect }) {
    const [location, setLocation] = useState('');
    const [coordinates, setCoordinates] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const getCurrentLocation = () => {
        if (!navigator.geolocation) {
            alert('La geolocalización no está soportada en tu navegador');
            return;
        }

        setIsLoading(true);
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const coords = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                setCoordinates(coords);
                
                try {
                    const locationName = await reverseGeocode(coords.latitude, coords.longitude);
                    setLocation(locationName);
                    onLocationSelect({
                        ...coords,
                        location_name: locationName
                    });
                } catch (error) {
                    console.error('Error getting location:', error);
                } finally {
                    setIsLoading(false);
                }
            },
            (error) => {
                console.error('Error getting location:', error);
                alert('No se pudo obtener tu ubicación');
                setIsLoading(false);
            }
        );
    };

    const reverseGeocode = async (lat, lon) => {
        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`
            );
            const data = await response.json();
            return data.display_name || '';
        } catch (error) {
            console.error('Error en geocoding:', error);
            return '';
        }
    };

    return (
        <div className="flex items-center space-x-2 mt-2">
            <button
                type="button"
                onClick={getCurrentLocation}
                disabled={isLoading}
                className="flex items-center space-x-2 text-[#509ca2] hover:text-[#509ca2]/80 disabled:opacity-50"
            >
                <MapPin className="h-5 w-5" />
                <span>{isLoading ? 'Obteniendo ubicación...' : 'Añadir ubicación'}</span>
            </button>
            {location && (
                <span className="text-sm text-gray-500">
                    📍 {location}
                </span>
            )}
        </div>
    );
}