#!/bin/bash

# Detener todos los contenedores activos
docker stop $(docker ps -aq) 2>/dev/null || true

# Eliminar todos los contenedores
docker rm $(docker ps -aq) 2>/dev/null || true

# Eliminar los contenedores y volúmenes del proyecto
docker compose down -v

# Eliminar imágenes no utilizadas
docker image prune -f

# Eliminar volúmenes no utilizados
docker volume prune -f

# Limpieza general del sistema Docker
docker system prune -f