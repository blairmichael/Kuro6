import requests


class Entry:
    def __init__(self, data, inputs):
        self.mal_id = data['mal_id']
        self.cover = requests.get(data['image_url']).content
        self.title = data['title']
        self.typ = data['type']
        self.status = data['status']
        self.synopsis = data['synopsis']

        self.titles = self.format_titles(data['title_synonyms'], data['title_english'])
        self.related = self.format_related(data['related'])
        self.genres = self.format_genres(data['genres'])

    def format_titles(self, titles, english):
        titles.append(english) if english else None
        for title in titles:
            if title:
                yield self.mal_id, title

    def format_related(self,related):
        for relation in related:
            for title in related[relation]:
                yield self.mal_id, title['mal_id'], title['name'], title['type'], relation

    def format_genres(self, genres):
        for genre in genres:
            yield self.mal_id, genre['mal_id'], genre['name']


class AnimeEntry(Entry):
    def __init__(self, data, inputs):
        super().__init__(data, inputs)

        self.progress = inputs[0]
        self.watched = inputs[1]
        self.rating = inputs[2]


        self.source = data['source']
        self.episodes = data['episodes']
        self.duration = data['duration']
        self.premiered = data['premiered']

        self.studios = self.format_studios(data['studios'])

        self.anime = self.format_anime()

    def format_studios(self, studios):
        for studio in studios:
            yield self.mal_id, studio['mal_id'], studio['name']

    def format_anime(self):
        yield (self.mal_id, self.cover, self.title, self.typ, self.progress, self.watched, self.rating,
            self.source, self.status, self.episodes, self.duration, self.synopsis, self.premiered)

    def data(self):
        return self.anime, self.titles, self.related, self.genres, self.studios


class MangaEntry(Entry):
    def __init__(self, data, inputs):
        super().__init__(data, inputs)

        self.progress = inputs[0]
        self.volumes_read = inputs[1]
        self.chapters_read = inputs[2]
        self.rating = inputs[3]

        self.volumes = data['volumes']
        self.chapters = data['chapters']
        self.published = data['published']['string']

        self.authors = self.format_authors(data['authors'])

        self.manga = self.format_manga()

    def format_authors(self, authors):
        for author in authors:
            yield self.mal_id, author['mal_id'], author['name']

    def format_manga(self):
        yield (self.mal_id, self.cover, self.title, self.typ, self.progress, self.volumes_read, self.chapters_read,
            self.rating, self.status, self.volumes, self.chapters, self.synopsis, self.published)

    def data(self):
        return self.manga, self.titles, self.related, self.genres, self.authors
