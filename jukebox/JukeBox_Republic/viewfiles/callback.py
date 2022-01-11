import datetime
from django.views import View
import requests
from ..secret_keys import client_id, client_secret, redirect_uri
from django.shortcuts import redirect
from ..partyhandler import Party
from ..SpotifyHandler import Spotify

class Callback(View):
    def get(self, request):
        r = requests.post("https://accounts.spotify.com/api/token",
                          data={'grant_type': "authorization_code",
                                'code': request.GET['code'],
                                'redirect_uri': redirect_uri,
                                'client_id': client_id,
                                'client_secret': client_secret})

        p = Party(Spotify(r.json()['access_token'], r.json()['refresh_token'], datetime.datetime.now() + datetime.timedelta(seconds=r.json()['expires_in'])))

        request.session["code"] = p.code

        return redirect('/host?roomcode=%i' % p.code)