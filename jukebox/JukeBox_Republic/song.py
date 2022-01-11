class Song:
    def __init__(self, uri, title="", album="", artist=""):
        self.uri = uri
        self.title = title
        self.album = album
        self.artist = artist

    def __str__(self):
        return str("Title: " + self.title + "; Album: " + self.album + "; Artist: " + self.artist)

    def get_uri(self):
        return self.uri
