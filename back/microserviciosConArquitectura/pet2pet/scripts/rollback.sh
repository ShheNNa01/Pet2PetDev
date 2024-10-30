#!/bin/bash
# scripts/rollback.sh

source $(dirname "$0")/deploy.sh

rollback() {
    local backup_dir="$1"
    
    if [ -z "$backup_dir" ]; then
        # Si no se especifica directorio, usar el más reciente
        backup_dir=$(ls -td $BACKUP_PATH/* | head -1)
    fi
    
    log "Iniciando rollback usando backup: $backup_dir"
    
    # Restaurar configuraciones
    if [ -f "$backup_dir/.env" ]; then
        cp "$backup_dir/.env" "$DEPLOY_PATH/"
    fi
    
    # Restaurar archivos de media
    if [ -d "$backup_dir/uploads" ]; then
        rm -rf "$DEPLOY_PATH/uploads"
        cp -r "$backup_dir/uploads" "$DEPLOY_PATH/"
    fi
    
    # Restaurar base de datos
    if [ -f "$backup_dir/database.sql" ]; then
        docker-compose exec -T postgres psql -U postgres pet2pet < "$backup_dir/database.sql"
    fi
    
    # Reiniciar servicios
    deploy_containers
    clear_cache
    check_health
    
    log "Rollback completado exitosamente"
}

# Ejecutar rollback
if [ -n "$1" ]; then
    rollback "$1"
else
    rollback
fi