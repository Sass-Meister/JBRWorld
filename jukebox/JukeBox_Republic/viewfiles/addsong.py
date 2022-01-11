from django.views import View
from django.shortcuts import render

from ..SpotifyHandler import Spotify
from django.shortcuts import redirect

from ..miscutils import dictverify

from ..partyhandler import Party, getparty

class addSong(View):
    def get(self, request):
        getparty(request).add_to_queue(request.GET['uri'])

        return redirect("/party")

    def post(self, request):
        p = getparty(request) # p for party

        # check if something is playing before doing anything else
        # Should this actually be checked or just take the nothing playing path when the api tells us we can't add to que?
        # This also causes a lot of problems
        if p.currently_playing() is None:
            error_text = "Something must be playing in order to add to the Spotify queue.  " \
                         "Please have something currently playing, such as a playlist."
            return render(request, "noresults.html", {"errortext": error_text,"roomcode": request.session['code']})

        query = ""

        # This method of creating the query from the us`er input might seem to be close to what spotify envisioned, but
        # in practice it fails to return as quality results as just combining the user input

        # for field in ['track', 'artist', 'album']:
        #     if field in request.POST and request.POST[field] != "":
        #         if query == "":
        #             query = field + ":%22" + request.POST[field].replace(" ", "+") + "%22"
        #
        #         else:
        #             query = query + "+" + field + ":%22" + request.POST[field].replace(" ", "+") + "%22"

        for field in ['track', 'artist', 'album']: # For each of the fields in the user form
            if field in request.POST and request.POST[field] != "": # If the user actually entered anything in this field
                if query == "": # If the query is empty
                    query = request.POST[field].replace(" ", "+") # Add user input to the query

                else: # Otherwise
                    query = query + "+" + request.POST[field].replace(" ", "+") # Add the user input to the end of the query

        results = p.search(q=query, limit=10)

        if len(results) == 0: # Just checking if spotify found anything
            return render(request, "noresults.html", {"errortext": "No Results.","roomcode": request.session['code']})

        # TODO: Finish this program.

        # resultlist = []
        # backuplist = []
        #
        # for result in results['tracks']['items']:
        #     duplicate = False
        #
        #     # Detect if this result has the same artist as any result already picked to be displayed
        #     for entry in resultlist: # For every result that we know will be shown
        #         for artist in result['artists']: # For each artist in the current song we're trying to decide to show or not
        #             if entry['artist'] == artist['name']: # If their artists are the same
        #                 duplicate = True # Set the correct flag
        #                 break # Break out of the inner loop
        #         else: # If the previous for loop ended naturally (without a break) https://stackoverflow.com/questions/189645/how-to-break-out-of-multiple-loops
        #             continue # Continue onto the next entry
        #         break # If the previous loop ended because of a break, then break the outer loop
        #
        #     # Add the current entry to the appropriate list
        #     if not duplicate:
        #         resultlist.append({"link": "/addsong?uri=%s" % result['uri'], # This is just what the template expects
        #                            "art": result['album']['images'][0]['url'],
        #                            "name": result['name'],
        #                            "artist": result['artists'][0]['name']})
        #
        #     else:
        #         backuplist.append({"link": "/addsong?uri=%s" % result['uri'],
        #                            "art": result['album']['images'][0]['url'],
        #                            "name": result['name'],
        #                            "artist": result['artists'][0]['name']})
        #
        #     # If we already have 6 results to display, there is no reason to continue to toil in the result mines
        #     if len(resultlist) == 6:
        #         break
        #
        # while len(resultlist) < 6 and len(backuplist) > 0: # While we do not have 6 results to show and there are results we passed over
        #     resultlist.append(backuplist.pop(0)) # Put the first result passed over at the end of the current results
        #
        # return render(request, "results.html", {"roomcode": request.session['code'], "result_list": resultlist})

        resultlist = []
        backuplist = []

        for result in results:
            duplicate = False

            if len(results) > 6:
                for entry in resultlist:
                    if result.artist() == entry.artist():
                        duplicate = True
                        break

            if not duplicate:
                resultlist.append(result)

            else:
                backuplist.append(result)

            if len(resultlist) >= 6:
                break

        while len(resultlist) < 6 and len(backuplist) > 0:
            resultlist.append(backuplist.pop(0))

        for i in range(len(resultlist)):
            resultlist[i] = {"link": "/addsong?uri=%s" % resultlist[i].uri(),
                             "art": resultlist[i].coverart_url(1),
                             "name": resultlist[i].song_name(),
                             "artist": resultlist[i].artist()}

        return render(request, "results.html", {"roomcode": request.session['code'], "result_list": resultlist})
