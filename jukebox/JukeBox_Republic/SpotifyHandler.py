# This should really implement some interface, but since its the only API we've implemented we'll get to that later

import requests.models
import requests
from .secret_keys import client_id, client_secret, redirect_uri, scope
import datetime
from enum import Enum
from time import sleep
from .miscutils import dictverify


login_link = "https://accounts.spotify.com/authorize?" + \
                     "client_id=" + client_id + \
                     "&redirect_uri=" + redirect_uri + \
                     "&scope=" + scope + \
                     "&response_type=code"

class RequestMethod(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4


class Song:
    def __init__(self, json):
        self.json = json
        self.verified = dict() # Keeps track of what entries in the json are verified to exist. Prevents having to check on every call

    def uri(self):
        if 'uri' not in self.verified:
            self.verified['uri'] = dictverify(self.json, 'uri')

        if self.verified['uri']:
            return self.json['uri']

        return None

    def coverart_url(self, size:int=0):
        key = ('coverart%i' % size)

        if key not in self.verified:
            self.verified[key] = dictverify(self.json, 'album', 'images', size, 'url')

        if self.verified[key]:
            return self.json['album']['images'][size]['url']

        return None

    def song_name(self):
        if 'name' not in self.verified:
            self.verified['name'] = dictverify(self.json, 'name')

        if self.verified['name']:
            return self.json['name']

        return None

    def artist(self):
        if 'artist' not in self.verified:
            self.verified['artist'] = dictverify(self.json, 'artists', 0, 'name')

        if self.verified['artist']:
            return self.json['artists'][0]['name']

        return None

    def duration(self):
        if 'duration' not in self.verified:
            self.verified['duration'] = dictverify(self.json, 'duration_ms')

        if self.verified['duration']:
            return self.json['duration_ms']

        return None

class Device:
    def __init__(self, json):
        json = json['devices']

        self.id = json['id']
        self.active = json['is_active'] == "true"
        self.name = json['name']

    def id(self):
        return self.id

    def active(self):
        return self.active

    def name(self):
        return self.name




class Spotify:
    def __init__(self, token:str, refresh_token:str, expires_at:datetime):
        self.token = token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    # This method should link our app to the Spotify API by generating the login link for users
    @staticmethod
    def generate_login_link():
        login_link = "https://accounts.spotify.com/authorize?" + \
                     "client_id=" + client_id + \
                     "&redirect_uri=" + redirect_uri + \
                     "&scope=" + scope + \
                     "&response_type=code"
        return login_link

    # Updates stale tokens. Only updated if the token is stale. If the token is not stale, set force to true and it will always be updated
    def update_token(self, force: bool = False):
        if self.expires_at.replace(tzinfo=None) < datetime.datetime.now() or force: # No need to update if it's not stale
            r = requests.post("https://accounts.spotify.com/api/token",
                              data={'grant_type': 'refresh_token',
                                    'refresh_token': self.refresh_token,
                                    'client_id': client_id,
                                    'client_secret': client_secret})

            self.token = r.json()['access_token']
            self.expires_at=datetime.datetime.now() + datetime.timedelta(seconds=r.json()['expires_in'])

    # This method is to take care of all the edge cases involved with sending and receiving data from the api.
    # This method will make sure to refresh the access token when the time is right, interpret the response code, and if
    # need be resend the request if spotify says we're doing too much.
    # This just returns the final response that spotify provides.
    def send(self, method: RequestMethod, url:str, params:dict=None) -> requests.models.Response:
        if params is None:
            params = dict()

        self.update_token()

        if method is RequestMethod.GET:
            r = requests.get(url, headers={'Authorization': 'Bearer %s' % self.token}, params=params)

        elif method is RequestMethod.POST:
            r = requests.post(url, headers={'Authorization': 'Bearer %s' % self.token}, params=params)

        elif method is RequestMethod.PUT:
            r = requests.put(url, headers={'Authorization': 'Bearer %s' % self.token}, params=params)

        elif method is RequestMethod.DELETE:
            r = requests.delete(url, headers={'Authorization': 'Bearer %s' % self.token}, params=params)

        else:
            raise Exception("Invalid RequestMethod")

        if r.status_code >= 400:   # aka "if there is a problem"
            # When spotify is mad we're sending too many request.
            # I wish there was a better way than making a blocking call but idk a better way
            if r.status_code == 429:
                sleep(int(r.headers['Retry-After']))

            # Request Unauthorized: My guess is that most of the time we just need to refresh the access token.
            elif r.status_code == 401:
                raise Exception("Unhandled Status Code %s: %s" % (r.status_code, r))

            elif r.status_code == 404:
                print("A playback device must be active and playing something")
                return r
                # return error message

            else:
                raise Exception("Unhandled Status Code " + str(r.status_code) + ": " + str(r))

            return self.send(method=method, url=url, params=params)

        return r

    def search(self, q, limit:int=4, type:str="track"):
        r = self.send(RequestMethod.GET, "https://api.spotify.com/v1/search", {'q': q, 'limit': limit, 'type': type}).json()
        rtr = []

        for result in r['tracks']['items']:
            rtr.append(Song(result))

        return rtr

    def add_to_queue(self, uri) -> bool:
        r = self.send(RequestMethod.POST, "https://api.spotify.com/v1/me/player/queue", {'uri': uri})
        return r.status_code == 204

    def currently_playing(self) -> (Song, int):
        r = self.send(RequestMethod.GET, "https://api.spotify.com/v1/me/player/currently-playing")

        if r.status_code == 204:
            return None, 0

        json = r.json()

        return Song(json['item']), int(json['progress_ms'])

    # this method checks if the current user is a Spotify Premium user
    def check_premium(self) -> bool:
        r = self.send(RequestMethod.GET, "https://api.spotify.com/v1/me")
        return 'product' in r.json() and r.json()['product'] == "premium"


    # Used to either resume playing (leave uri blank) or start playing a new song (provide a uri)
    def play(self, uri:str="", device_id:str="") -> bool:
        r = self.send(RequestMethod.PUT, "https://api.spotify.com/v1/me/player/play", {'context_uri': uri, 'device_id': device_id})
        return r.status_code == 204

    def get_devices(self):
        return Device(self.send(RequestMethod.GET, "https://api.spotify.com/v1/me/player/devices").json())
