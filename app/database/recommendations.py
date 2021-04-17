import sqlite3

class Recommendations:
    def __init__(self):
        self.connection = sqlite3.connect('recommendations.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.initialise()

    def initialise(self):
        query = """
            CREATE TABLE IF NOT EXISTS anime(
                id INTEGER PRIMARY KEY,
                cover BLOB,
                title TEXT,
                type TEXT,
                score TEXT,
                synopsis TEXT,
                rank INTEGER
            );

            CREATE TABLE IF NOT EXISTS anime_genres(
                genre_id INTEGER PRIMARY KEY,
                genre TEXT
            );

            CREATE TABLE IF NOT EXISTS anime_genres_link(
                id INTEGER,
                genre_id INTEGER,
                UNIQUE(id, genre_id)
                FOREIGN KEY (id) REFERENCES anime (id)
                ON DELETE CASCADE
                FOREIGN KEY (genre_id) REFERENCES anime_genres (genre_id)
                ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS studios(
                studio_id INTEGER PRIMARY KEY,
                studio TEXT
            );

            CREATE TABLE IF NOT EXISTS studios_link(
                id INTEGER,
                studio_id INTEGER,
                UNIQUE(id, studio_id)
                FOREIGN KEY (id) REFERENCES anime (id)
                ON DELETE CASCADE
                FOREIGN KEY (studio_id) REFERENCES studios (studio_id)
                ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS manga(
                id INTEGER PRIMARY KEY,
                cover BLOB,
                title TEXT,
                type TEXT,
                score TEXT,
                synopsis TEXT,
                rank INTEGER
            );

            CREATE TABLE IF NOT EXISTS manga_genres(
                genre_id INTEGER PRIMARY KEY,
                genre TEXT
            );

            CREATE TABLE IF NOT EXISTS manga_genres_link(
                id INTEGER,
                genre_id INTEGER,
                UNIQUE(id, genre_id)
                FOREIGN KEY (id) REFERENCES manga (id)
                ON DELETE CASCADE
                FOREIGN KEY (genre_id) REFERENCES manga_genres (genre_id)
                ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS authors(
                author_id INTEGER PRIMARY KEY,
                author TEXT
            );

            CREATE TABLE IF NOT EXISTS authors_link(
                id INTEGER,
                author_id INTEGER,
                UNIQUE(id, author_id)
                FOREIGN KEY (id) REFERENCES manga (id)
                ON DELETE CASCADE
                FOREIGN KEY (author_id) REFERENCES authors (author_id)
                ON DELETE CASCADE
            );
        """

        queries = query.split('\n\n')
        for q in queries:
            self.cursor.execute(q)
        self.connection.commit()

    def add_anime(self, data):
        anime = """
            REPLACE INTO anime(id, cover, title, type, score, synopsis)
            VALUES(?, ?, ?, ?, ?, ?)
        """

        genres = """
            REPLACE INTO anime_genres(genre_id, genre)
            VALUES(?, ?)
        """

        g_link = """
            REPLACE INTO anime_genres_link(id, genre_id)
            VALUES(?, ?)
        """

        studios = """
            REPLACE INTO studios(studio_id, studio)
            VALUES(?, ?)
        """

        studios_link = """
            REPLACE INTO studios_link(id, studio_id)
            VALUES(?, ?)
        """

        self.cursor.execute(anime, data[0])
        for genre in data[1]:
            g_1 = (genre[1], genre[2])
            g_2 = (genre[0], genre[1])
            self.cursor.execute(genres, g_1)
            self.cursor.execute(g_link, g_2)
        for studio in data[2]:
            s_1 = (studio[1], studio[2])
            s_2 = (studio[0], studio[1])
            self.cursor.execute(studios, s_1)
            self.cursor.execute(studios_link, s_2)

        self.connection.commit()

    def add_manga(self, data):
        manga = """
            REPLACE INTO manga(id, cover, title, type, score, synopsis)
            VALUES(?, ?, ?, ?, ?, ?)
        """

        genres = """
            REPLACE INTO manga_genres(genre_id, genre)
            VALUES(?, ?)
        """

        g_link = """
            REPLACE INTO manga_genres_link(id, genre_id)
            VALUES(?, ?)
        """

        authors = """
            REPLACE INTO authors(author_id, author)
            VALUES(?, ?)
        """

        authors_link = """
            REPLACE INTO authors_link(id, author_id)
            VALUES(?, ?)
        """

        self.cursor.execute(manga, data[0])
        for genre in data[1]:
            g_1 = (genre[1], genre[2])
            g_2 = (genre[0], genre[1])
            self.cursor.execute(genres, g_1)
            self.cursor.execute(g_link, g_2)
        for author in data[2]:
            s_1 = (author[1], author[2])
            s_2 = (author[0], author[1])
            self.cursor.execute(authors, s_1)
            self.cursor.execute(authors_link, s_2)

        self.connection.commit()

    def get_anime(self):
        query = """
            SELECT anime.id, anime_genres_link.genre_id
            FROM anime
            INNER JOIN anime_genres_link ON anime_genres_link.id = anime.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def get_manga(self):
        query = """
            SELECT manga.id, manga_genres_link.genre_id
            FROM manga
            INNER JOIN manga_genres_link ON manga_genres_link.id = manga.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def update_anime_rank(self, ids):
        rank = 1
        for id_ in ids:
            query = f"""
                UPDATE anime
                SET rank = {rank}
                WHERE id = {id_}
            """
            rank += 1
            self.cursor.execute(query)
        self.connection.commit()


    def update_manga_rank(self, ids):
        rank = 1
        for id_ in ids:
            query = f"""
                UPDATE manga
                SET rank = {rank}
                WHERE id = {id_}
            """
            rank += 1
            self.cursor.execute(query)
        self.connection.commit()


    def count_anime(self):
        self.cursor.execute('SELECT COUNT(*) FROM anime')
        count = self.cursor.fetchone()
        return count[0]


    def count_manga(self):
        self.cursor.execute('SELECT COUNT(*) FROM manga')
        count = self.cursor.fetchone()
        return count[0]


    def anime_information(self, rank):
        self.cursor.execute(f'SELECT * FROM anime WHERE rank = {rank}')
        anime = self.cursor.fetchone()
        id_ = anime[0]
        genre_query = f"""
            SELECT anime_genres.genre
            FROM anime_genres
            INNER JOIN anime_genres_link ON anime_genres_link.genre_id = anime_genres.genre_id
            WHERE anime_genres_link.id = {id_}
        """
        self.cursor.execute(genre_query)
        genres = ', '.join([genre[0] for genre in self.cursor.fetchall()])
        studio_query = f"""
            SELECT studios.studio
            FROM studios
            INNER JOIN studios_link ON studios_link.studio_id = studios.studio_id
            WHERE studios_link.id = {id_}
        """
        self.cursor.execute(studio_query)
        studios = ', '.join([studio[0] for studio in self.cursor.fetchall()])
        return anime, genres, studios


    def manga_information(self, rank):
        self.cursor.execute(f'SELECT * FROM manga WHERE rank = {rank}')
        manga = self.cursor.fetchone()
        id_ = manga[0]
        genre_query = f"""
            SELECT manga_genres.genre
            FROM manga_genres
            INNER JOIN manga_genres_link ON manga_genres_link.genre_id = manga_genres.genre_id
            WHERE manga_genres_link.id = {id_}
        """
        self.cursor.execute(genre_query)
        genres = ', '.join([genre[0] for genre in self.cursor.fetchall()])
        authors_query = f"""
            SELECT authors.author
            FROM authors
            INNER JOIN authors_link ON authors_link.author_id = authors.author_id
            WHERE authors_link.id = {id_}
        """
        self.cursor.execute(authors_query)
        authors = ', '.join([author[0] for author in self.cursor.fetchall()])
        return manga, genres, authors


    def get_anime_id(self, rank):
        self.cursor.execute(f'SELECT id FROM anime WHERE rank = {rank}')
        id_ = self.cursor.fetchone()
        return id_[0]


    def get_manga_id(self, rank):
        self.cursor.execute(f'SELECT id FROM manga WHERE rank = {rank}')
        id_ = self.cursor.fetchone()
        return id_[0]
