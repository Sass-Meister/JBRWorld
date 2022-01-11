from django.views import View
from django.shortcuts import render
from ..partyhandler import *

class Party(View):
    def get(self, request):
        if 'roomcode' in request.GET:
            request.session['code'] = request.GET['roomcode']

        p = getparty(request)

        song = p.currently_playing()[0]

        defaultvalues = {"roomcode": request.session['code'],
                         "album_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/800px-Question_mark_%28black%29.svg.png",
                         "songname": "Nothing Playing",
                         "artist": "N/A",
                         "error": False}

        if song is None:
            return render(request, "party.html", defaultvalues)

        renderdict = {"roomcode": request.session['code'], "album_url": song.coverart_url(),
                      "songname": song.song_name(), "artist": song.artist(), "error": False}

        for key in renderdict:
            if renderdict[key] is None and key in defaultvalues:
                renderdict[key] = defaultvalues[key]

        return render(request, "party.html", renderdict)