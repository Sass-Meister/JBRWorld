# import User
# from .rules import SongRules
from enum import Enum
import json


class ListType(Enum):
    NONE = 1
    WHITELIST = 2
    BLACKLIST = 3


class PartyClass:
    def __init__(self, room_code=00000, repeat_dist=0, user=""):
        self.list_of_users = []
        self.list_of_hosts = [user]
        self.party_code = room_code
        self.current_queue = []  # matches with the spotify playlist: current song + future songs
        self.suggestion_queue = []  # our temporary queue
        self.blacklisted_users = []
        self.list_type = ListType.NONE

        # repeat dist of 0 means no restriction on repeat, -1 means no repeats at all
        #   positive rdist = # of songs that must be inbetween an identical song
        self.repeat_dist = repeat_dist
        self.rule_list = []
        # self.artist_list = []             # currently unused fields
        # self.album_list = []
        # self.genre_list = []

    # functions

    def add_user(self, user):
        if self.blacklisted_users.__contains__(user):
            return
        else:
            self.list_of_users.append(user)

    def add_host(self, user_asking, user_adding):
        # verify that user_asking is a host
        if self.list_of_hosts.__contains__(user_asking):
            self.list_of_hosts.append(user_adding)

    def add_rule_list(self, song_id):
        self.rule_list.append(song_id)

    def remove_rule_list(self, song_id):
        self.rule_list.remove(song_id)

    def add_suggestion(self, song_id):
        # check if user is in user list - removed
        # if self.list_of_users.__contains__(user):
        if self.validate(song_id):
            self.suggestion_queue.append(song_id)
            # TODO: add song_id to database count
        else:
            print("Requested song did not pass validation")

    def remove_next_suggestion(self):
        return self.suggestion_queue.pop(0)

    def add_next_suggestion_to_live(self):
        song_id = self.remove_next_suggestion()
        self.current_queue.append(song_id)
        # TODO: add request to be added to Spotify playlist in host view
        return song_id

    def add_live_queue(self, song_id, user):
        if self.list_of_users.__contains__(user):
            if self.validate(song_id):
                self.current_queue.append(song_id)
                # TODO: add request to be added to Spotify playlist in host view
                return song_id

    def advance_current(self):
        self.current_queue.pop(0)  # update our currently playing list to the next song

    def kick_user(self, user_asking, user):
        if self.list_of_hosts.__contains__(user_asking):
            self.list_of_users.remove(user)
            self.blacklisted_users.append(user)

    def leave_party(self, user):
        self.list_of_users.remove(user)

    def view_suggest_num(self, song_id):
        pass  # TODO: db lookup of count under song_id, return 0 if lookup fails

    def end_party(self):
        self.suggestion_queue.clear()
        self.list_of_users.clear()
        self.list_of_hosts.clear()

    def validate(self, song_id):
        song_list_copy = self.get_current_queue()
        song_list_copy.append(self.get_suggestion_queue())  # current queue + suggestion queue
        song_list_copy.reverse()  # reversed to check from back to front
        if self.repeat_dist == -1:
            # if song_list_copy.__contains__(song_id):
            #     return False
            # else:
            #     return True
            return True             # rdist doesn't really work for some reason, just bypassing it
        elif self.repeat_dist >= 0:
            # # check for the requested song within the repeat distance
            # count = self.repeat_dist
            # # if the song is found within the repeat distance, return false
            # while count > 0:
            #     if song_list_copy.pop(0) == song_id:
            #         return False
            #     count = count - 1
            # # otherwise, continue checking

            # based on type of list, if the requested song is in the list, decide what to return
            if self.list_type == ListType.NONE:
                return True
            elif self.list_type == ListType.WHITELIST:
                if self.rule_list.__contains__(song_id):
                    return True
                else:
                    return False
            elif self.list_type == ListType.BLACKLIST:
                if self.rule_list.__contains__(song_id):
                    return False
                else:
                    return True

    # setters
    def set_list_type(self, list_type):
        self.list_type = list_type

    def set_repeat_dist(self, dist):
        self.repeat_dist = dist

    # getters
    def get_list_of_users(self):
        return self.list_of_users

    def get_list_of_hosts(self):
        return self.list_of_hosts

    def get_party_code(self):
        return self.party_code

    def get_suggestion_queue(self):
        return self.suggestion_queue

    def get_current_queue(self):
        return self.suggestion_queue

    def get_rule_list(self):
        return self.rule_list

    def get_list_type(self):
        return self.list_type
