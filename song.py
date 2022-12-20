from itertools import zip_longest
from selenium import webdriver
from selenium.webdriver.common.by import By
from helpers import slugify
import os

class Song:
    def __init__(self, name="", name_translated="", url="", lyrics=None):
        self.name = name
        self.name_translated = name_translated
        self.url = url
        self.lyrics = lyrics if lyrics else []
    
    def get_lyrics_str(self):
        ans = ""
        for item in self.lyrics:
            ans += item[0] + "\n" + item[1] + "\n\n"
        return ans
    
    def extract_song_lyrics(self, d: webdriver.Chrome):
        d.get(self.url)
        row_elements = d.find_elements(By.XPATH, value='//table/tbody/tr')
        if len(row_elements) <= 1:
            cells = d.find_elements(By.XPATH, value='//pre')
            if len(cells):
                all_german = cells[0].text.strip()
                all_english = cells[1].text.strip() if len(cells) >= 2 else ""
                german_list = all_german.split("\n")
                english_list = all_english.split("\n")
                self.lyrics = list(zip_longest(german_list, english_list, fillvalue=""))
        else:
            for row_element in row_elements:
                cells = row_element.find_elements(By.XPATH, value='td')
                german = cells[0].text.strip()
                english = cells[1].text.strip() if len(cells) >= 2 else ""
                self.lyrics.append((german, english))
    
    def save_to_file(self, path, album_name, index):
        if not os.path.exists(os.path.join(path, album_name)):
            os.makedirs(os.path.join(path, album_name))
        full_path = os.path.join(path, album_name, "{} - {}.txt".format(index, slugify(self.name)))
        with open(full_path, "w") as f:
            f.write(self.get_lyrics_str())



