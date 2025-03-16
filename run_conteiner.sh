
# * Run the docker-compose file
docker-compose up --build -d


# * run the docker container
docker exec -it 42-django-1-sql-backend-1 /bin/zsh


# ? Run the postgresql container
docker exec -it postgres-db /bin/sh 

# ? run informacion de la base de datos
# psql -U user -d ex00
# \dt -> show tables
# \d table_name -> show columns of table 
# \c ex00 -> connect to database ex00
