from song import Song
from typing import List

class Album:
    def __init__(self, name:str = "", songs: List[Song] = None):
        self.name = name
        self.songs = songs if songs else []