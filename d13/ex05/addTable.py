import psycopg2
from .models import Movies

class ErrorInDatabase(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)

class TableValue():
    def __init__(self, title, episode_nb, director, producer, release_date, opening_crawl="None"):
        self.title = title
        self.episode_nb = episode_nb
        if opening_crawl:
            self.opening_crawl = opening_crawl
        else:
            self.opening_crawl = None
        self.director = director
        self.producer = producer
        self.release_date = release_date

    def save(self):
        try:
            Movies.objects.create(
                title=self.title,
                episode_nb=self.episode_nb,
                opening_crawl=self.opening_crawl,
                director=self.director,
                producer=self.producer,
                release_date=self.release_date
            )

        except Exception as e:
            raise  ErrorInDatabase("Error: {}".format(e))
    