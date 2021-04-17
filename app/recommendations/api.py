from jikanpy import Jikan, APIException
import requests


class JikanAPI:
    def __init__(self):
        self.jikan = Jikan()

    def anime(self, genre_id):
        try:
            responses = self.jikan.genre('anime', genre_id)['anime']
            for response in responses[:25]:
                yield (response['mal_id'], response['image_url'], response['title'],
                    response['type'], response['score'], response['synopsis'],
                    response['genres'], response['producers'])
        except APIException as e:
            raise e

    def manga(self, genre_id):
        try:
            responses = self.jikan.genre('manga', genre_id)['manga']
            for response in responses[:25]:
                yield (response['mal_id'], response['image_url'], response['title'],
                    response['type'], response['score'], response['synopsis'],
                    response['genres'], response['authors'])
        except APIException as e:
            raise e


class Entry:
    def __init__(self, mal_id, url, title, type_, score, synopsis, genres):
        self.main_query = (mal_id, requests.get(url).content, title, type_, score, synopsis)
        self.genres = self.format_genres(mal_id, genres)

    @staticmethod
    def format_genres(mal_id, genres):
        for genre in genres:
            yield mal_id, genre['mal_id'], genre['name']


class AnimeEntry(Entry):
    def __init__(self, mal_id, url, title, type_, score, synopsis, genres, studios):
        super(AnimeEntry, self).__init__(mal_id, url, title, type_, score, synopsis, genres)
        self.studios = self.format_studios(mal_id, studios)

    @staticmethod
    def format_studios(mal_id, studios):
        for studio in studios:
            yield mal_id, studio['mal_id'], studio['name']

    def data(self):
        return self.main_query, self.genres, self.studios


class MangaEntry(Entry):
    def __init__(self, mal_id, url, title, type_, score, synopsis, genres, authors):
        super(MangaEntry, self).__init__(mal_id, url, title, type_, score, synopsis, genres)
        self.authors = self.format_authors(mal_id, authors)

    @staticmethod
    def format_authors(mal_id, authors):
        for author in authors:
            yield mal_id, author['mal_id'], author['name']

    def data(self):
        return self.main_query, self.genres, self.authors
