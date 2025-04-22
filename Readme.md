# Use the correct database name
psql -U djangouser -d djangotraining -c "\d ex00_movies"


# Connect as superuser (inside the PostgreSQL container)
docker exec -it postgres-db psql -U djangouser 

# Create the formationdjango database
CREATE DATABASE formationdjango;

# Exit
\q

# Now the original command will work
psql -U djangouser -d formationdjango -c "\d ex00_movies"


# Delete a database and recreate it
psql -c "drop database formationdjango;" 
psql -c "create database formationdjango;"


# Remove migrations:

rm -rf */migrations

# Run migrations for each application as needed:

python3 manage.py makemigrations ex01
python3 manage.py migrate ex01

# Clear data from tables

## Using SQL (PostgreSQL):
psql -U djangouser -d djangotraining -c "DELETE FROM table_name;" # Delete all rows but keep the table
psql -U djangouser -d djangotraining -c "TRUNCATE TABLE table_name CASCADE;" # Faster delete with FK cascade

## Using Django ORM:
python3 manage.py shell
