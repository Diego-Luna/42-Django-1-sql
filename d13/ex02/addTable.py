import psycopg2

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
        # print("--> Diego:"+opening_crawl)
        self.director = director
        self.producer = producer
        self.release_date = release_date

    def save(self, table_name):
        try:
            conn = psycopg2.connect(
                    dbname="djangotraining",
                    user="djangouser",
                    password="secret",
                    host="database",
                    port="5432"
                )

            cur = conn.cursor()
            cur.execute("""
                INSERT INTO {table_name} (title, episode_nb, opening_crawl, director, producer, release_date)
                VALUES (%s, %s, %s, %s, %s, %s);
            """.format(table_name=table_name), (self.title, self.episode_nb, self.opening_crawl, self.director, self.producer, self.release_date))
    #         cur.execute("""INSERT INTO {table_name}
    # VALUES ({title}, {episode_nb}, {opening_crawl}, {director}, {producer}, {release_date});""".format(
    #             table_name=table_name, title=self.title, episode_nb=self.episode_nb, opening_crawl=self.opening_crawl, director=self.director, producer=self.producer, release_date=self.release_date))

            conn.commit()
            cur.close()
            conn.close()

        except Exception as e:
            raise  ErrorInDatabase("Error: {}".format(e))
    