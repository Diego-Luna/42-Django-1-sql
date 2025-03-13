

# #!/bin/bash

# # Detener y eliminar contenedor anterior si existe
# docker rm -f django-dev-container 2>/dev/null || true

# docker build -t django-libraries-env .

# # Ejecutar contenedor nuevo con montaje del directorio completo
# docker run -it \
#     --name django-dev-container \
#     -v "$(pwd)":/app \
#     -p 8000:8000 \
#     django-libraries-env


#!/bin/bash

# Detener y eliminar contenedor anterior si existe
docker rm -f django-2-sql-container 2>/dev/null || true

docker build -t django-2-sql .

# Ejecutar contenedor nuevo con montaje del directorio completo
docker run -it \
    --name django-2-sql-container \
    -v "$(pwd)":/app \
    -p 8000:8000 \
    django-2-sql