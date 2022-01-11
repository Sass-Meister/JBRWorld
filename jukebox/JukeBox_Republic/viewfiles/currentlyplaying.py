from django.views import View
from django.http import JsonResponse
from ..partyhandler import getparty


class currentlyplaying(View):
    def get(self, request):
        p = getparty(request)

        song = p.currently_playing()[0]

        renderdict = {"roomcode": request.session['code'],
                      "album_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/800px-Question_mark_%28black%29.svg.png",
                      "songname": "Nothing Playing",
                      "artist": "N/A"}

        if song is not None:
            if song.song_name() is not None:
                renderdict['songname'] = song.song_name()

            if song.coverart_url(1) is not None:
                renderdict['album_url'] = song.coverart_url(1)

            if song.artist() is not None:
                renderdict['artist'] = song.artist()

        return JsonResponse(renderdict, safe=False)