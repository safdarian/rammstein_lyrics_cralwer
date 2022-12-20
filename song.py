class Song:
    def __init__(self, name="", name_translated="", url="", lyrics=None):
        self.name = name
        self.name_translated = name_translated
        self.url = url
        self.lyrics = lyrics if lyrics else []