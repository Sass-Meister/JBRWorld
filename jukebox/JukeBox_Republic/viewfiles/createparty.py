from django.views import View
from django.shortcuts import render

from ..SpotifyHandler import Spotify
from ..models import Party as PartyModel
from ..models import AuthSet
from ..partyclass import PartyClass, ListType
from random import randint
from django.shortcuts import redirect
import jsonpickle

class CreateParty(View):
    def get(self, request):
        if not request.session.has_key('my_token'):
            error_text = "Not logged in, can't create party"
            return render(request, "index.html", {"loggedin": False, "error": True, "errortext": error_text})

        request.session['party_token'] = request.session['my_token']

        spotify = Spotify(request)      # init a Spotify class to check the user's account type

        if not spotify.check_premium():                  # if user isn't Premium, send them back to index page
            error_text = "Must be a Spotify Premium user to create a room"
            return render(request, "index.html", {"loggedin": False, "error": True, "errortext": error_text})

        try:
            authset = AuthSet.objects.get(access_token=request.session['my_token'])
        except AuthSet.DoesNotExist: # If this errors out there is an internal problem because the callback view will be run and redirect here (we can assume an authset will be created before we get here)
            error_text = "Authset not found"
            return render(request, "index.html", {"loggedin": False, "error": True, "errortext": error_text})

        # Testing if this spotify user already has created party, just take them back to the party they had already created
        try:
            party = PartyModel.objects.get(authset=authset)

            request.session['code'] = party.code

            return redirect('/host?roomcode=%s' % party.code)

        except PartyModel.DoesNotExist:
            pass # If this user does not have a party associated with it, continue on and create a party for them

        newcode = randint(10000, 99999)

        while PartyModel.objects.filter(code=newcode).count() > 0:
            newcode = randint(10000, 99999)

        PartyModel(authset=authset, code=newcode).save()

        request.session['code'] = newcode

        # encoding partyclass instance to json to pass around in sessions
        newparty = PartyClass(newcode)
        request.session['partyobj'] = jsonpickle.encode(newparty)

        return redirect('/host?roomcode=%s' % newcode)