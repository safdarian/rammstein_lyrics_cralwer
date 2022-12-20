from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from itertools import zip_longest

from album import Album
from song import Song
from config_manager import ConfigManager
from logger import Logger

config = ConfigManager()
logger = Logger()
s = Service(config.get_selenium_webdriver_path())
url = config.get_affenknecht_lyrics_page()

options = Options()
options.headless = True

driver = webdriver.Chrome(service=s, options=options)
driver.get(url)
album_elements = driver.find_elements(By.XPATH, value= '//table/tbody/tr/td')

albums = []
for album_element in album_elements:
    title_elements = album_element.find_elements(By.XPATH, value='h2')
    # if td block is not empty
    if title_elements:
        album_title = title_elements[0].text
        current_album = Album(album_name=album_title)
        print("{}".format(album_title))
        song_elements = album_element.find_elements(By.XPATH, value='(p/br/following-sibling::a[1])|(p/a[1])')
        for i, song_element in enumerate(song_elements, 1):
            
            
            separator = ""
            if "–" in song_element.text:
                separator = "–"
            elif "-" in song_element.text:
                separator = "-"
            
            
            german_name  = song_element.text.strip()
            english_name = ""
                
            if separator:
                german_name  = song_element.text.split(separator)[0].strip()
                english_name = song_element.text.split(separator)[1].strip()
                
            song_lyric_page_url = song_element.get_attribute("href")
            
            current_song = Song(name=german_name, name_translated=english_name, url=song_lyric_page_url)
            current_album.songs.append(current_song)
            
            print("{:<2} - {:<18} - {:<18} - {}".format(i, current_song.name, current_song.name_translated, current_song.url))
            
        albums.append(current_album)
        print("-" * 100)

