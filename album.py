class Album:
    def __init__(self, album_name="", songs=None):
        self.album_name = album_name
        self.songs = songs if songs else []