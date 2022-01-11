# from enum import Enum
# from .partyclass import PartyClass
#
#
# class ListType(Enum):
#     NONE = 1
#     WHITELIST = 2
#     BLACKLIST = 3
#
#
# class SongRules:
#
#     def __init__(self, party, repeat_dist):
#         self.party = party
#         self.list_type = ListType.NONE
#
#         # repeat dist of 0 means no restriction on repeat, -1 means no repeats at all
#         self.repeat_distance = repeat_dist
#
#         self.song_list = []
#         # not sure if these fields are needed, or how to use them.  That depends on how the songs are structured.
#         # self.artist_list = []
#         # self.album_list = []
#         # self.genre_list = []
#
#     def validate(self, song_id):
#         song_list_copy = PartyClass.get_song_queue(self.party)
#         song_list_copy.append(PartyClass.get_suggestion_queue(self.party))
#         song_list_copy.reverse()
#         if self.repeat_distance == -1:
#             if song_list_copy.__contains__(song_id):
#                 return False
#         elif self.repeat_distance >= 0:
#             # check for the requested song within the repeat distance
#             count = self.repeat_distance
#             # if the song is found within the repeat distance, return false
#             while count > 0:
#                 if song_list_copy.pop(0) == song_id:
#                     return False
#                 count = count - 1
#             # otherwise, continue checking
#
#             # based on type of list, if the requested song is in the list, decide what to return
#             if self.list_type == ListType.NONE:
#                 return True
#             elif self.list_type == ListType.WHITELIST:
#                 if self.song_list.__contains__(song_id):
#                     return True
#                 else:
#                     return False
#             elif self.list_type == ListType.BLACKLIST:
#                 if self.song_list.__contains__(song_id):
#                     return False
#                 else:
#                     return True
#
#     # setters
#     def set_list_type(self, type_of_list):
#         self.list_type = type_of_list
#
#     def set_repeat_dist(self, repeat_dist):
#         self.repeat_distance = repeat_dist
#
#     # getters
#     def get_list_type(self):
#         return self.list_type
#
#     def get_repeat_dist(self):
#         return self.repeat_distance
#
#     # adders
#     def add_song(self, song_id):
#         self.song_list.append(song_id)
#
#     # removers
#     def remove_song(self, song_id):
#         self.song_list.remove(song_id)
