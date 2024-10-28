# Guía de Uso: Pet2Pet Virtual Pet Service

## Introducción

El servicio de mascotas virtuales de Pet2Pet proporciona una capa adicional de gamificación a la red social. Cada mascota real puede tener una contraparte virtual que evoluciona basada en las interacciones del usuario en la plataforma.

## Configuración Inicial

1. Crear una nueva mascota virtual:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/virtual-pets",
    json={
        "pet_id": 1,
        "level": 1,
        "experience_points": 0,
        "happiness": 100.0,
        "energy": 100.0,
        "attributes": {
            "food": 100.0,
            "health": 100.0,
            "happiness": 100.0,
            "social_skill": 100.0
        }
    }
)
```

## Acciones Principales

### 1. Realizar una Acción

```python
response = requests.post(
    "http://localhost:8000/api/v1/virtual-pets/1/actions/post_creation",
    json={
        "content": "Nueva publicación",
        "location": "Pet Park"
    }
)
```

### 2. Obtener Tareas Diarias

```python
response = requests.get(
    "http://localhost:8000/api/v1/virtual-pets/1/daily-tasks"
)
```

### 3. Verificar Estadísticas

```python
response = requests.get(
    "http://localhost:8000/api/v1/virtual-pets/1/stats"
)
```

## Sistema de Niveles

- Nivel 1-10: 100-500 XP por nivel
- Nivel 11-25: 500-1500 XP por nivel
- Nivel 26-50: 1500-5000 XP por nivel
- Nivel 51-75: 5000-12000 XP por nivel
- Nivel 76-100: 12000-25000 XP por nivel

## Puntos por Actividad

- Crear publicación: 50 XP + 20 Comida
- Interactuar con mascota: 30 XP + 15 Salud
- Completar desafío: 100 XP + 25 Felicidad
- Participar en grupo: 40 XP + 10 Destreza Social

## Logros Disponibles

### Logros Sociales
- Mariposa Social: 50 interacciones
- Líder Comunitario: 10 grupos

### Logros de Tiempo
- Amigo Fiel: 30 días activo

### Logros de Contenido
- Creador de Contenido: 100 publicaciones

## Consideraciones

1. Las estadísticas disminuyen con el tiempo:
   - Comida: -5% por hora
   - Felicidad: -3% por hora
   - Energía: -4% por hora

2. Bonificaciones por nivel:
   - Al subir de nivel, todas las estadísticas se restauran al 100%
   - Desbloqueo de nuevas características cada 10 niveles

3. Consejos de optimización:
   - Mantener interacciones regulares
   - Balancear diferentes tipos de actividades
   - Completar tareas diarias para maximizar ganancias

## Integración con Otros Servicios

El servicio de mascotas virtuales se integra con:
- Servicio de Posts
- Servicio de Grupos
- Servicio de Notificaciones
- Servicio de Logros

## Manejo de Errores

Los errores comunes incluyen:
- 404: Mascota virtual no encontrada
- 400: Acción inválida o parámetros incorrectos
- 429: Demasiadas solicitudes (rate limiting)

## Soporte y Recursos Adicionales

- Documentación API: `/api/v1/docs`
- Documentación ReDoc: `/api/v1/redoc`
- Colección Postman: [enlace pendiente]