from jikanpy import Jikan, APIException, exceptions
import random


class JikanAPI:
    def __init__(self):
        self.jikan = Jikan()
        self.anime_dict = {
            'action': 1,
            'adventure': 2,
            'cars': 3,
            'comedy': 4,
            'dementia': 5,
            'demons': 6,
            'mystery': 7,
            'drama': 8,
            'ecchi': 9,
            'fantasy': 10,
            'game': 11,
            'hentai': 12,
            'historical': 13,
            'horror': 14,
            'kids': 15,
            'magic': 16,
            'martial arts': 17,
            'mecha': 18,
            'music': 19,
            'parody': 20,
            'samurai': 21,
            'romance': 22,
            'school': 23,
            'sci fi': 24,
            'shoujo': 25,
            'shoujo ai': 26,
            'shounen': 27,
            'shounen ai': 28,
            'space': 29,
            'sports': 30,
            'super power': 31,
            'vampire': 32,
            'yaoi': 33,
            'yuri': 34,
            'harem': 35,
            'slice of life': 36,
            'supernatural': 37,
            'military': 38,
            'police': 39,
            'psychological': 40,
            'thriller': 41,
            'seinen': 42,
            'josei': 43
        }
        self.manga_dict = {
            'action': 1,
            'adventure': 2,
            'cars': 3,
            'comedy': 4,
            'dementia': 5,
            'demons': 6,
            'mystery': 7,
            'drama': 8,
            'ecchi': 9,
            'fantasy': 10,
            'game': 11,
            'hentai': 12,
            'historical': 13,
            'horror': 14,
            'kids': 15,
            'magic': 16,
            'martial arts': 17,
            'mecha': 18,
            'music': 19,
            'parody': 20,
            'samurai': 21,
            'romance': 22,
            'school': 23,
            'sci fi': 24,
            'shoujo': 25,
            'shoujo ai': 26,
            'shounen': 27,
            'shounen ai': 28,
            'space': 29,
            'sports': 30,
            'super power': 31,
            'vampire': 32,
            'yaoi': 33,
            'yuri': 34,
            'harem': 35,
            'slice of life': 36,
            'supernatural': 37,
            'military': 38,
            'police': 39,
            'psychological': 40,
            'seinen': 41,
            'josei': 42,
            'doujinshi': 43,
            'gender bender': 44,
            'thriller': 45
        }

    def search(self, category, query, type_, genres):
        if category.lower() == 'anime':
            try:
                responses = self.jikan.search(
                    category.lower(),
                    query,
                    parameters={
                        'limit': 10,
                        'type': type_,
                        'genres': [self.anime_dict[genre] for genre in genres]
                    }
                )['results']
                for response in responses:
                    yield (response['image_url'], response['mal_id'], response['title'], category.lower(), response['type'],
                        response['episodes'])
            except APIException as e:
                raise e
        else:
            try:
                responses = self.jikan.search(
                    category.lower(),
                    query,
                    parameters={
                        'limit': 10,
                        'type': type_,
                        'genres': [self.manga_dict[genre] for genre in genres]
                    }
                )['results']
                for response in responses:
                    yield (response['image_url'], response['mal_id'], response['title'], category.lower(), response['type'],
                        response['volumes'], response['chapters'])
            except APIException as e:
                raise e

    def id(self, category, mal_id):
        if category.lower() == 'anime':
            try:
                response = self.jikan.anime(mal_id)
                return (response['image_url'], response['mal_id'], response['title'], 'anime', response['type'],
                    response['episodes'])
            except APIException as e:
                raise e
        else:
            try:
                response = self.jikan.manga(mal_id)
                return (response['image_url'], response['mal_id'], response['title'], 'manga', response['type'],
                    response['volumes'], response['chapters'])
            except APIException as e:
                raise e

    def genre(self, category, genre, results, page):
        try:
            responses = self.jikan.genre(
                type=category.lower(),
                genre_id=genre[0],
                page=page
            )[category.lower()][int(results[0])- 1:int(results[1])]
            if category.lower() == 'anime':
                for response in responses:
                    yield (response['image_url'], response['mal_id'], response['title'], category.lower(), response['type'],
                        response['episodes'])
            else:
                for response in responses:
                    yield (response['image_url'], response['mal_id'], response['title'], category.lower(), response['type'],
                        response['volumes'])
        except APIException as e:
            raise e

    def top(self, category, type_, results, page):
        try:
            if type_:
                responses = self.jikan.top(
                    type=category.lower(),
                    page=page,
                    subtype=type_
                )['top'][int(results[0])-1:int(results[1])]
            else:
                responses = self.jikan.top(
                    type=category.lower(),
                    page=page
                )['top'][int(results[0])-1:int(results[1])]
            if category.lower() == 'anime':
                for response in responses:
                    yield (response['image_url'], response['mal_id'], response['title'], 'anime', response['type'],
                        response['episodes'])
            else:
                for response in responses:
                    yield (response['image_url'], response['mal_id'], response['title'], 'manga', response['type'],
                        response['volumes'])
        except APIException as e:
            raise e

    def season(self, year, season, shuffle):
        try:
            responses = self.jikan.season(
                year=year,
                season=season
            )['anime']
            if shuffle:
                random.shuffle(responses)
            for response in responses[:15]:
                yield (response['image_url'], response['mal_id'], response['title'], 'anime', response['type'],
                    response['episodes'])
        except APIException as e:
            raise e

    def anime(self, mal_id):
        try:
            data = self.jikan.anime(mal_id)
            return data
        except APIException as e:
            raise e

    def manga(self, mal_id):
        try:
            data = self.jikan.manga(mal_id)
            return data
        except APIException as e:
            return e

    def anime_info(self, mal_id):
        try:
            data = self.jikan.anime(mal_id)
            return ((data['mal_id'], data['image_url'], data['title'], data['title_synonyms'], data['type'],
                data['source'], data['episodes'], data['synopsis'][:-25] if data['synopsis'] else '', data['premiered'],
                data['status'], data['duration'], data['score'], data['studios'], data['genres'], data['related']))
        except APIException as e:
            raise e

    def manga_info(self, mal_id):
        try:
            data = self.jikan.manga(mal_id)
            return (data['mal_id'], data['image_url'], data['title'], data['title_synonyms'], data['type'],
                data['volumes'], data['chapters'], data['synopsis'][:-25], data['published'], data['status'],
                data['score'], data['authors'], data['genres'], data['related'])
        except APIException as e:
            raise e
