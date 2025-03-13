#!/bin/bash

python3 -m venv django_venv

# * Activar el entorno virtual
source django_venv/bin/activate

# * Instalar los requisitos desde el archivo requirement.txt
# ? se nesesita tener inataldo "postgresql"
pip install -r requirements.txt


# * Mantener el entorno virtual activado
echo "The django_venv virtual environment is now enabled."
echo "--> To deactivate it, type 'deactivate'"

echo "\n- Django version:"
python -c "import django; print(django.__version__)"

echo "\n- psycopg2 version:"
python -c "import psycopg2; print('psycopg2 versión:', psycopg2.__version__)"

exec $SHELL