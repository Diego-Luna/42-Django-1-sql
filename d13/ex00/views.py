from django.shortcuts import HttpResponse
import psycopg2

# Create your views here.

#  todo: create the init view and 
def init(request):
    try:

        # conn = psycopg2.connect("dbname=ex00 user=user")
        conn = psycopg2.connect(
            dbname="ex00",
            user="user",
            password="queso",
            host="database",
            port="5432"
            )

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS ex00_movies (
            title varchar(64) UNIQUE NOT NULL,\
            episode_nb serial PRIMARY KEY,
            opening_crawl text, 
            director varchar(32) NOT NULL,
            producer varchar(128) NOT NULL,
            release_date date NOT NULL)
        """)

        conn.commit()
        cur.close()
        conn.close()

        return HttpResponse('Ok')
    except Exception as e:
        return HttpResponse("Error: {}".format(e))