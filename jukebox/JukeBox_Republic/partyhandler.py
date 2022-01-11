# The idea with this class is that it is all much easier if views only interact with the party hander and the party handler interacts with the respective API to that party.
from django.http import HttpRequest

from .SpotifyHandler import Spotify, Song
from threading import Semaphore
from enum import Enum
from random import randint

parties = dict() # Master dictionary of all current parties. Use getparties to access this correctly

class RulesType(Enum):
    WHITELIST = 0
    BLACKLIST = 1

class RulesEnum(Enum):
    EXPLICIT = 0 # Bans explicit songs (ignores RulesType)
    DUPLICATE = 1 # Prevents a duplicate song if it was played within the last 20 songs

# The responsibilities of the party class are to manage the playback queue and ensure that song requests fit the rules of the party
class Party:
    def __init__(self, spotify):
        code = randint(10000, 99999)

        while code in parties:
            code = randint(10000, 99999)

        self.code = code # 5 digit room code
        self.spotify = spotify # The spotify object to be used with this specific party
        self.lock = Semaphore() # To ensure thread safety
        self.que = list() # The upcoming songs on the queue
        self.play_history = list() # The
        self.rules = list()
        self.thread = None # Created when the first song is played

        parties[code] = self

    # Should a search result be filtered out if the results match the rules or not?
    # Given a search query, the respective API will be called and results will be returned as a list of song objects of length max_objects (defaults to 6)
    def search(self, q:str, limit: int =6) -> list:
        return self.spotify.search(q, limit)

    # Returns the currently playing song as a tuple of the Song and its progress
    # TODO: Add caching
    def currently_playing(self) -> (Song, int):
        return self.spotify.currently_playing()

    def add_to_queue(self, uri:str):
        return self.spotify.add_to_queue(uri)

def getparty(request: HttpRequest) -> Party:
    if 'code' in request.session:
        code = request.session['code']

    elif 'roomcode' in request.GET:
        request.session['code'] = request.GET['roomcode']
        code = request.GET['roomcode']

    else:
        return None

    code = int(code)

    if code not in parties.keys():
        return None

    return parties[code]