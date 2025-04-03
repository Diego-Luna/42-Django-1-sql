from django.shortcuts import HttpResponse
from django.shortcuts import render
import psycopg2

# from .addTable import TableValue, ErrorInDatabase

name_table_1 = "ex08_planets"
name_table_2 = "ex08_people"

#  todo: create the init view and 
def init(request):
    try:
        conn = psycopg2.connect(
            dbname="ex00",
            user="user",
            password="queso",
            host="database",
            port="5432"
        )
        cur = conn.cursor()
        
        cur.execute("""CREATE TABLE IF NOT EXISTS {} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            climate VARCHAR(255),
            diameter INTEGER,
            orbital_period INTEGER,
            population BIGINT,
            rotation_period INTEGER,
            surface_water REAL,
            terrain VARCHAR(128)
        )
        """.format(name_table_1))

        cur.execute("""CREATE TABLE IF NOT EXISTS {} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            birth_year VARCHAR(32),
            gender VARCHAR(32),
            eye_color VARCHAR(32),
            hair_color VARCHAR(32),
            height INTEGER,
            mass REAL,
            homeworld VARCHAR(64),
            FOREIGN KEY (homeworld) REFERENCES {}(name)
        )
        """.format(name_table_2, name_table_1))

        conn.commit()
        cur.close()
        conn.close()

        return HttpResponse('Ok')
    except Exception as e:
        return HttpResponse("Error: {}".format(e))
    
def populate(request):
    try:
        conn = psycopg2.connect(
            dbname="ex00",
            user="user",
            password="queso",
            host="database",
            port="5432"
        )
        cur = conn.cursor()
        
        cur.execute("DELETE FROM {};".format(name_table_2))
        cur.execute("DELETE FROM {};".format(name_table_1))
        conn.commit()
        
        result_text = ""
        
        try:
            with open('planets.csv', 'r') as f:
                for line in f:
                    values = line.strip().split('\t')
                    
                    for i in range(len(values)):
                        if values[i] == "NULL":
                            values[i] = None
                    
                    #  * Asegurarse de que hay suficientes valores
                    while len(values) < 8:
                        values.append(None)
                    
                    try:
                        cur.execute("""
                            INSERT INTO {} (name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (name) DO NOTHING;
                        """.format(name_table_1), values[:8])
                        
                        conn.commit()
                        result_text += f"OK - Planeta {values[0]}<br>"
                    except Exception as e:
                        result_text += f"Error inserting planet {values[0]}: {str(e)}<br>"
        except Exception as e:
            result_text += f"Error reading planets.csv file: {str(e)}<br>"
        
        # * Contar planetas insertados
        cur.execute("SELECT COUNT(*) FROM {}".format(name_table_1))
        planet_count = cur.fetchone()[0]
        result_text += f"Total number of planets inserting: {planet_count}<br>"
        
        try:
            with open('people.csv', 'r') as f:
                for line in f:
                    values = line.strip().split('\t')
                    
                    # * Convertir "NULL" a None
                    for i in range(len(values)):
                        if values[i] == "NULL":
                            values[i] = None

                    while len(values) < 8:
                        values.append(None)
                    
                    try:
                        # * Insertar persona
                        cur.execute("""
                            INSERT INTO {} (name, birth_year, gender, eye_color, hair_color, height, mass, homeworld)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (name) DO NOTHING;
                        """.format(name_table_2), values[:8])
                        
                        conn.commit()
                        result_text += f"OK - Person: {values[0]}<br>"
                    except Exception as e:
                        result_text += f"Error inserting persons: {values[0]}: {str(e)}<br>"
        except Exception as e:
            result_text += f"Error reading people.csv file: {str(e)}<br>"
        
        cur.execute("SELECT COUNT(*) FROM {}".format(name_table_2))
        people_count = cur.fetchone()[0]
        result_text += f"Total number of persons inserting: {people_count}<br>"
        
        cur.close()
        conn.close()
        
        return HttpResponse(result_text)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

def display(request):
    try:
        conn = psycopg2.connect(
            dbname="ex00",
            user="user",
            password="queso",
            host="database",
            port="5432"
        )
        cur = conn.cursor()
        
        # * Verificar si hay planetas con clima "windy"
        cur.execute("SELECT name, climate FROM {} WHERE climate LIKE %s OR climate LIKE %s".format(name_table_1), 
                   ('%windy%', '%moderately windy%'))
        windy_planets = cur.fetchall()
        print("Planetas con clima windy:", windy_planets)
        
        if not windy_planets:
            return HttpResponse("No data available")
        
        cur.execute("""
            SELECT p.name, p.homeworld, pl.climate 
            FROM {} p
            JOIN {} pl ON p.homeworld = pl.name
            WHERE pl.climate LIKE %s OR pl.climate LIKE %s
            ORDER BY p.name ASC;
        """.format(name_table_2, name_table_1), ('%windy%', '%moderately windy%'))
        
        results = cur.fetchall()
        print("Resultados finales:", results)
        
        cur.close()
        conn.close()
        
        if not results:
            return HttpResponse("No data available")
        
        # * Crear tabla HTML con los resultados
        
        result = "<table border='1'>"
        result += """<tr>
            <th>Name</th>
            <th>Homeworld</th>
            <th>Climate</th>
        </tr>"""
        
        for row in results:
            result += "<tr>"
            for col in row:
                result += "<td>{}</td>".format(col if col is not None else 'N/A')
            result += "</tr>"
        
        result += "</table>"
        
        return HttpResponse(result)
    except Exception as e:
        print("Error en display:", e)
        return HttpResponse("No data available")