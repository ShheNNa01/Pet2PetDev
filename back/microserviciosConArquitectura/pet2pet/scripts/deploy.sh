#!/bin/bash
# scripts/deploy.sh

# Colores para los logs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
PROJECT_NAME="pet2pet"
DEPLOY_PATH="/var/www/pet2pet"  # Ajusta esta ruta según tu servidor
BACKUP_PATH="/var/backups/pet2pet"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
GIT_BRANCH="main"  # O el branch que uses para producción

# Funciones de utilidad
log() {
    echo -e "[$(date +'%Y-%m-%d %H:%M:%S')] ${GREEN}$1${NC}"
}

warn() {
    echo -e "[$(date +'%Y-%m-%d %H:%M:%S')] ${YELLOW}WARNING: $1${NC}"
}

error() {
    echo -e "[$(date +'%Y-%m-%d %H:%M:%S')] ${RED}ERROR: $1${NC}"
    exit 1
}

# Verificar permisos de root
check_root() {
    if [ "$(id -u)" != "0" ]; then
        error "Este script debe ejecutarse como root"
    fi
}

# Verificar dependencias
check_dependencies() {
    log "Verificando dependencias..."
    command -v docker >/dev/null 2>&1 || error "Docker no está instalado"
    command -v docker-compose >/dev/null 2>&1 || error "Docker Compose no está instalado"
    command -v git >/dev/null 2>&1 || error "Git no está instalado"
}

# Crear backup
create_backup() {
    log "Creando backup..."
    
    # Crear directorio de backup
    mkdir -p "$BACKUP_PATH/$TIMESTAMP"
    
    # Backup de configuraciones
    if [ -f "$DEPLOY_PATH/.env" ]; then
        cp "$DEPLOY_PATH/.env" "$BACKUP_PATH/$TIMESTAMP/"
    fi
    
    # Backup de archivos de media
    if [ -d "$DEPLOY_PATH/uploads" ]; then
        cp -r "$DEPLOY_PATH/uploads" "$BACKUP_PATH/$TIMESTAMP/"
    fi
    
    # Backup de la base de datos
    if docker-compose ps | grep -q postgres; then
        docker-compose exec -T postgres pg_dump -U postgres pet2pet > "$BACKUP_PATH/$TIMESTAMP/database.sql" || \
            error "Error al crear backup de la base de datos"
    fi
    
    log "Backup creado en $BACKUP_PATH/$TIMESTAMP"
}

# Actualizar código
update_code() {
    log "Actualizando código..."
    
    # Si es la primera vez, clonar el repositorio
    if [ ! -d "$DEPLOY_PATH" ]; then
        git clone -b $GIT_BRANCH https://github.com/ShheNNa01/Pet2PetDevWeb.git $DEPLOY_PATH || \
            error "Error al clonar el repositorio"
    else
        cd $DEPLOY_PATH
        git fetch --all || error "Error al fetch del repositorio"
        git reset --hard origin/$GIT_BRANCH || error "Error al reset del código"
    fi
}

# Configurar entorno
setup_environment() {
    log "Configurando entorno..."
    
    # Crear directorios necesarios
    mkdir -p $DEPLOY_PATH/uploads
    mkdir -p $DEPLOY_PATH/logs
    
    # Configurar permisos
    chown -R www-data:www-data $DEPLOY_PATH/uploads
    chown -R www-data:www-data $DEPLOY_PATH/logs
    
    # Verificar existencia de .env
    if [ ! -f "$DEPLOY_PATH/.env" ]; then
        warn "Archivo .env no encontrado. Copiando de ejemplo..."
        cp "$DEPLOY_PATH/.env.example" "$DEPLOY_PATH/.env"
    fi
}

# Construir y levantar contenedores
deploy_containers() {
    log "Desplegando contenedores..."
    
    cd $DEPLOY_PATH
    
    # Detener contenedores existentes
    docker-compose down || warn "Error al detener contenedores existentes"
    
    # Construir imágenes
    docker-compose build --no-cache || error "Error al construir contenedores"
    
    # Levantar contenedores
    docker-compose up -d || error "Error al levantar contenedores"
}

# Ejecutar migraciones
run_migrations() {
    log "Ejecutando migraciones..."
    
    cd $DEPLOY_PATH
    docker-compose exec -T api_gateway alembic upgrade head || \
        error "Error al ejecutar migraciones"
}

# Limpiar caché
clear_cache() {
    log "Limpiando caché..."
    
    if docker-compose ps | grep -q redis; then
        docker-compose exec -T redis redis-cli FLUSHALL || \
            warn "Error al limpiar caché de Redis"
    fi
}

# Verificar salud de los servicios
check_health() {
    log "Verificando salud de los servicios..."
    
    # Esperar a que los servicios estén disponibles
    sleep 10
    
    # Verificar API Gateway
    curl -f http://localhost:8000/health || error "API Gateway no responde"
    
    # Verificar otros servicios críticos
    docker-compose ps | grep -q "Up" || error "Algunos contenedores no están corriendo"
    
    log "Todos los servicios están funcionando correctamente"
}

# Limpiar recursos antiguos
cleanup() {
    log "Limpiando recursos antiguos..."
    
    # Eliminar imágenes antiguas
    docker image prune -f
    
    # Eliminar backups antiguos (más de 30 días)
    find $BACKUP_PATH/* -type d -mtime +30 -exec rm -rf {} \;
}

# Función principal
main() {
    log "Iniciando despliegue de $PROJECT_NAME..."
    
    check_root
    check_dependencies
    create_backup
    update_code
    setup_environment
    deploy_containers
    run_migrations
    clear_cache
    check_health
    cleanup
    
    log "¡Despliegue completado exitosamente!"
}

# Manejo de errores
trap 'error "Se produjo un error en la línea $LINENO. Abortando..."' ERR

# Ejecutar
main