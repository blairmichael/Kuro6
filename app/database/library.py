import sqlite3

class Library:
    def __init__(self):
        self.connection = sqlite3.connect('library.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.initialise()

    def initialise(self):
        query = """
            CREATE TABLE IF NOT EXISTS anime(
                id INTEGER PRIMARY KEY,
                cover BLOB,
                title TEXT,
                type TEXT,
                progress TEXT,
                episodes_watched INTEGER,
                rating INTEGER,
                source TEXT,
                status TEXT,
                episodes TEXT,
                duration TEXT,
                synopsis TEXT,
                premiered TEXT
            );

            CREATE TABLE IF NOT EXISTS anime_titles(
                id INTEGER,
                title TEXT,
                FOREIGN KEY (id) REFERENCES anime (id)
                ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS related(
                related_id INTEGER PRIMARY KEY,
                name TEXT,
                type TEXT,
                UNIQUE(related_id, type)
            );

            CREATE TABLE IF NOT EXISTS anime_relations(
                id INTEGER,
                related_id INTEGER,
                relation TEXT,
                UNIQUE(id, related_id)
                FOREIGN KEY (id) REFERENCES anime (id)
                ON DELETE CASCADE
                FOREIGN KEY (related_id) REFERENCES related (related_id)
                ON DELETE CASCADE
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
                progress TEXT,
                volumes_read INTEGER,
                chapters_read INTEGER,
                rating INTEGER,
                status TEXT,
                volumes TEXT,
                chapters TEXT,
                duration TEXT,
                synopsis TEXT,
                published TEXT
            );

            CREATE TABLE IF NOT EXISTS manga_titles(
                id INTEGER,
                title TEXT,
                FOREIGN KEY (id) REFERENCES manga (id)
                ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS manga_relations(
                id INTEGER,
                related_id INTEGER,
                relation TEXT,
                UNIQUE(id, related_id)
                FOREIGN KEY (id) REFERENCES manga (id)
                ON DELETE CASCADE
                FOREIGN KEY (related_id) REFERENCES related (related_id)
                ON DELETE CASCADE
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

        for i in query.split('\n\n'):
            self.cursor.execute(i)
        self.connection.commit()

    def add_anime(self, data):
        anime = """
            REPLACE INTO anime(id, cover, title, type, progress, episodes_watched,
                rating, source, status, episodes, duration, synopsis, premiered)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        titles = """
            REPLACE INTO anime_titles(id, title)
            VALUES(?, ?)
        """

        related = """
            REPLACE INTO related(related_id, name, type)
            VALUES(?, ?, ?)
        """

        r_link = """
            REPLACE INTO anime_relations(id, related_id, relation)
            VALUES(?, ?, ?)
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

        s_link = """
            REPLACE INTO studios_link(id, studio_id)
            VALUES(?, ?)
        """

        self.cursor.execute(anime, next(data[0]))
        for title in data[1]:
            self.cursor.execute(titles, title)
        for relation in data[2]:
            r_1 = (relation[1], relation[2], relation[3])
            r_2 = (relation[0], relation[1], relation[4])
            self.cursor.execute(related, r_1)
            self.cursor.execute(r_link, r_2)
        for genre in data[3]:
            g_1 = (genre[1], genre[2])
            g_2 = (genre[0], genre[1])
            self.cursor.execute(genres, g_1)
            self.cursor.execute(g_link, g_2)
        for studio in data[4]:
            s_1 = (studio[1], studio[2])
            s_2 = (studio[0], studio[1])
            self.cursor.execute(studios, s_1)
            self.cursor.execute(s_link, s_2)
        self.connection.commit()

    def add_manga(self, data):
        manga = """
            REPLACE INTO manga(id, cover, title, type, progress, volumes_read,
                chapters_read, rating, status, volumes, chapters, synopsis, published)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        titles = """
            REPLACE INTO manga_titles(id, title)
            VALUES(?, ?)
        """

        related = """
            REPLACE INTO related(related_id, name, type)
            VALUES(?, ?, ?)
        """

        r_link = """
            REPLACE INTO manga_relations(id, related_id, relation)
            VALUES(?, ?, ?)
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

        a_link = """
            REPLACE INTO authors_link(id, author_id)
            VALUES(?, ?)
        """

        self.cursor.execute(manga, next(data[0]))
        for title in data[1]:
            self.cursor.execute(titles, title)
        for relation in data[2]:
            r_1 = (relation[1], relation[2], relation[3])
            r_2 = (relation[0], relation[1], relation[4])
            self.cursor.execute(related, r_1)
            self.cursor.execute(r_link, r_2)
        for genre in data[3]:
            g_1 = (genre[1], genre[2])
            g_2 = (genre[0], genre[1])
            self.cursor.execute(genres, g_1)
            self.cursor.execute(g_link, g_2)
        for author in data[4]:
            a_1 = (author[1], author[2])
            a_2 = (author[0], author[1])
            self.cursor.execute(authors, a_1)
            self.cursor.execute(a_link, a_2)
        self.connection.commit()

    def update_anime(self, data):
        query = """
            UPDATE anime
            SET progress = ?,
                episodes_watched = ?,
                rating = ?
            WHERE id = ?
        """

        self.cursor.execute(query, data)
        self.connection.commit()

    def update_manga(self, data):
        query = """
            UPDATE manga
            SET progress = ?,
                volumes_watched = ?,
                chapters_watched = ?,
                rating = ?
            WHERE id = ?
        """

        self.cursor.execute(query, data)
        self.connection.commit()

    def delete_anime(self, id_):
        query = f"""
            DELETE FROM anime
            WHERE id = {id_}
        """

        self.cursor.execute(query)
        self.connection.commit()


    def delete_manga(self, id_):
        query = f"""
            DELETE FROM manga
            WHERE id = {id_}
        """

        self.cursor.execute(query)
        self.connection.commit()

    def anime_info(self, id_):
        anime_query = f"""
            SELECT *
            FROM anime
            WHERE id = {id_}
        """
        self.cursor.execute(anime_query)
        anime = self.cursor.fetchall()

        titles_query = f"""
            SELECT anime_titles.title
            FROM anime_titles
            WHERE anime_titles.id = {id_}
        """
        self.cursor.execute(titles_query)
        titles = ' - '.join([title[0] for title in self.cursor.fetchall()])

        genres_query = f"""
            SELECT anime_genres.genre
            FROM anime_genres
            INNER JOIN anime_genres_link ON anime_genres_link.genre_id = anime_genres.genre_id
            WHERE anime_genres_link.id = {id_}
        """
        self.cursor.execute(genres_query)
        genres = ', '.join([genre[0] for genre in self.cursor.fetchall()])

        related_query = f"""
            SELECT related.name, related.type, anime_relations.relation
            FROM related
            INNER JOIN anime_relations ON anime_relations.related_id = related.related_id
            WHERE anime_relations.id = {id_}
        """
        self.cursor.execute(related_query)
        related = self.cursor.fetchall()
        related_dictionary = dict()
        for relation in related:
            if relation[2] in related_dictionary:
                related_dictionary[relation[2]] += f' - {relation[0]} ({relation[1]})'
            else:
                related_dictionary[relation[2]] = f'{relation[0]} ({relation[1]})'

        studios_query = f"""
            SELECT studios.studio
            FROM studios
            INNER JOIN studios_link ON studios_link.studio_id = studios.studio_id
            WHERE studios_link.id = {id_}
        """
        self.cursor.execute(studios_query)
        studios = ' - '.join([studio[0] for studio in self.cursor.fetchall()])

        return anime, titles, genres, related_dictionary, studios

    def manga_info(self, id_):
        manga_query = f"""
            SELECT *
            FROM manga
            WHERE id = {id_}
        """
        self.cursor.execute(manga_query)
        manga = self.cursor.fetchall()

        titles_query = f"""
            SELECT manga_titles.title
            FROM manga_titles
            WHERE manga_titles.id = {id_}
        """
        self.cursor.execute(titles_query)
        titles = ' - '.join([title[0] for title in self.cursor.fetchall()])

        genres_query = f"""
            SELECT manga_genres.genre
            FROM manga_genres
            INNER JOIN manga_genres_link ON manga_genres_link.genre_id = manga_genres.genre_id
            WHERE manga_genres_link.id = {id_}
        """
        self.cursor.execute(genres_query)
        genres = ', '.join([genre[0] for genre in self.cursor.fetchall()])

        related_query = f"""
            SELECT related.name, related.type, manga_relations.relation
            FROM related
            INNER JOIN manga_relations ON manga_relations.related_id = related.related_id
            WHERE manga_relations.id = {id_}
        """
        self.cursor.execute(related_query)
        related = self.cursor.fetchall()
        related_dictionary = dict()
        for relation in related:
            if relation[2] in related_dictionary:
                related_dictionary[relation[2]] += f' - {relation[0]} ({relation[1]})'
            else:
                related_dictionary[relation[2]] = f'{relation[0]} ({relation[1]})'

        authors_query = f"""
            SELECT authors.author
            FROM authors
            INNER JOIN authors_link ON authors_link.author_id = authors.author_id
            WHERE authors_link.id = {id_}
        """
        self.cursor.execute(authors_query)
        authors = ' - '.join([author[0] for author in self.cursor.fetchall()])

        return manga, titles, genres, related_dictionary, authors

    def get_anime_statistics(self):
        record_query = """
            SELECT count(*)
            FROM anime
        """

        self.cursor.execute(record_query)
        num_anime = self.cursor.fetchone()[0]

        watching_query = """
            SELECT count(*)
            FROM anime
            WHERE progress == 'Watching'
        """
        self.cursor.execute(watching_query)
        watching = self.cursor.fetchone()[0]

        completed_query = """
            SELECT count(*)
            FROM anime
            WHERE progress == 'Completed'
        """
        self.cursor.execute(completed_query)
        completed = self.cursor.fetchone()[0]

        planning_query = """
            SELECT count(*)
            FROM anime
            WHERE progress == 'Planning'
        """
        self.cursor.execute(planning_query)
        planning = self.cursor.fetchone()[0]

        dropped_query = """
            SELECT count(*)
            FROM anime
            WHERE progress == 'Dropped'
        """
        self.cursor.execute(dropped_query)
        dropped = self.cursor.fetchone()[0]

        episodes_query = """
            SELECT sum(episodes_watched)
            FROM anime
        """
        self.cursor.execute(episodes_query)
        episodes = self.cursor.fetchone()[0]

        return num_anime, planning, watching, completed, dropped, episodes

    def get_manga_statistics(self):
        record_query = """
            SELECT count(*)
            FROM manga
        """

        self.cursor.execute(record_query)
        num_manga = self.cursor.fetchone()[0]

        reading_query = """
            SELECT count(*)
            FROM manga
            WHERE progress == 'Reading'
        """
        self.cursor.execute(reading_query)
        reading = self.cursor.fetchone()[0]

        completed_query = """
            SELECT count(*)
            FROM manga
            WHERE progress == 'Completed'
        """
        self.cursor.execute(completed_query)
        completed = self.cursor.fetchone()[0]

        planning_query = """
            SELECT count(*)
            FROM manga
            WHERE progress == 'Planning'
        """
        self.cursor.execute(planning_query)
        planning = self.cursor.fetchone()[0]

        dropped_query = """
            SELECT count(*)
            FROM manga
            WHERE progress == 'Dropped'
        """
        self.cursor.execute(dropped_query)
        dropped = self.cursor.fetchone()[0]

        volumes_query = """
            SELECT sum(volumes_read)
            FROM manga
        """
        self.cursor.execute(volumes_query)
        volumes = self.cursor.fetchone()[0]

        chapters_query = """
                SELECT sum(chapters_read)
                FROM manga
            """
        self.cursor.execute(chapters_query)
        chapters = self.cursor.fetchone()[0]

        return num_manga, planning, reading, completed, dropped, volumes, chapters


    def get_anime_genres(self):
        query = """
            SELECT anime.rating, anime_genres_link.genre_id
            FROM anime
            INNER JOIN anime_genres_link ON anime_genres_link.id = anime.id
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()


    def get_manga_genres(self):
        query = """
            SELECT manga.rating, manga_genres_link.genre_id
            FROM manga
            INNER JOIN manga_genres_link ON manga_genres_link.id = manga.id
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()
