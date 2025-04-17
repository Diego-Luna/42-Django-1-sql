from django.shortcuts import HttpResponse
from django.shortcuts import render
import psycopg2

from .addTable import TableValue, ErrorInDatabase

# Create your views here.

name_table = "ex06_movies"

#  todo: create the init view and 
def init(request):
    try:

        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="database",
            port="5432"
            )

        cur = conn.cursor()
        
        cur.execute("""CREATE TABLE IF NOT EXISTS {} (
            title varchar(64) UNIQUE NOT NULL,
            episode_nb serial PRIMARY KEY,
            opening_crawl text, 
            director varchar(32) NOT NULL,
            producer varchar(128) NOT NULL,
            release_date date NOT NULL,
            created timestamp DEFAULT current_timestamp,
            updated timestamp DEFAULT current_timestamp
        )
        """.format(name_table))

        print("Table created")

        # * add crete trigger
        cur.execute("""
            CREATE OR REPLACE FUNCTION update_changetimestamp_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated = now();
                NEW.created = OLD.created;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
            """)
        print("Trigger created")
        # * 
        cur.execute("""DROP TRIGGER IF EXISTS update_films_changetimestamp ON {};""".format(name_table))

        print("Trigger dropped")

        cur.execute("""
        CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
        ON {} FOR EACH ROW EXECUTE PROCEDURE
        update_changetimestamp_column();
        """.format(name_table))

        print("Trigger created")

        conn.commit()
        cur.close()
        conn.close()

        return HttpResponse('Ok')
    except Exception as e:
        return HttpResponse("Error: {}".format(e))
    
def populate(request):

    data = [
        TableValue(
            episode_nb= 1,
            title= "The Phantom Menace",
            director= "George Lucas",
            producer= "Rick McCallum",
            release_date= "1999-05-19",
        ),
        TableValue(
            episode_nb= 2,
            title= "Attack of the Clones",
            director= "George Lucas",
            producer= "Rick McCallum",
            release_date= "2002-05-16",
        ),
        TableValue(
            episode_nb= 3,
            title= "Revenge of the Sith",
            director= "George Lucas",
            producer= "Rick McCallum",
            release_date= "2005-05-19",
        ),
        TableValue(
            episode_nb= 4,
            title= "A New Hope",
            director= "George Lucas",
            producer= "Gary Kurtz, Rick McCallum",
            release_date= "1977-05-25",
        ),
        TableValue(
            episode_nb= 5,
            title= "The Empire Strikes Back",
            director= "Irvin Kershner",
            producer= "Gary Kutz, Rick McCallum",
            release_date= "1980-05-17",
        ),
        TableValue(
        
            episode_nb= 6,
            title= "Return of the Jedi",
            director= "Richard Marquand",
            producer= "Howard G. Kazanjian, George Lucas, Rick McCallum",
            release_date= "1983-05-25",
        ),
        TableValue(
            episode_nb= 7,
            title= "The Force Awakens",
            director= "J.J. Abrams",
            producer= "Kathleen Kennedy, J.J. Abrams, Bryan Burk",
            release_date= "2015-12-11",
        )
    ]
    returnValue = ""
    for value in data:
        try:
            value.save(name_table)
            returnValue += "<br>OK"
        except ErrorInDatabase as e:
            returnValue += "<br> Error: {}".format(e)


    return HttpResponse(returnValue)

def display(request):
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="database",
            port="5432"
            )

        cur = conn.cursor()
        cur.execute("""SELECT * FROM {};""".format(name_table))
        test = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()
        # print(test)
        if not test:
            return HttpResponse("No data available")
        result = "<table border='1' colspan='6'>"
        result += """<tr>
    <td>Title</td>
    <td>episode_nb</td>
    <td>opening_crawl</td>
    <td>director</td>
    <td>producer</td>
    <td>release_date</td>
    <td>created</td>
    <td>updated</td>
  </tr>"""
        for row in test:
            result += "<tr>"
            for col in row:
                result += "<td>{}</td>".format(col)
            result += "</tr>"
        result += "</table>"

        return HttpResponse(result)
    except Exception as e:
        return HttpResponse("No data available")
    
def update(request):
    try:
        conn = psycopg2.connect(
            dbname="djangotraining",
            user="djangouser",
            password="secret",
            host="database",
            port="5432"
        )
        cur = conn.cursor()
        
        # If form was submitted
        if request.method == 'POST' and 'update' in request.POST:
            title = request.POST.get('title')
            opening_crawl = request.POST.get('opening_crawl')
            print(title, opening_crawl)
            if title:
                cur.execute(
                    "UPDATE {} SET opening_crawl = %s WHERE title = %s;".format(name_table), 
                    (opening_crawl, title)
                )
                conn.commit()
        
        # Get remaining movie titles for dropdown
        cur.execute("SELECT title FROM {} ORDER BY episode_nb;".format(name_table))
        movies = cur.fetchall()
        
        cur.close()
        conn.close()
        
        if not movies:
            return HttpResponse("No data available")
        
        return render(request, 'ex06_update.html', {'movies': movies})
    except Exception as e:
        return HttpResponse("No data available")

