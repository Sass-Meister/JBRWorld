from django.views import View
from django.shortcuts import render

from ..SpotifyHandler import login_link


class Index(View):
    def get(self, request):
        return render(request, "index.html", {"loggedin": False,
                                              "loginlink": login_link,
                                              "error": False,
                                              "errortext": ""})