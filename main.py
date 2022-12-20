from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

from album import Album
from song import Song
from config_manager import ConfigManager
from logger import Logger
from helpers import slugify

config = ConfigManager()
logger = Logger()
os.makedirs(config.get_output_path(), exist_ok=True)

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
        current_album = Album(name=album_title)
        logger.write("{}".format(album_title))
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
            
            logger.write("{:<2} - {:<18} - {:<18} - {}".format(i, current_song.name, current_song.name_translated, current_song.url))
            
        albums.append(current_album)
        logger.write("-" * 100)

logger.write("Fetching song links finished")


for album in albums:
    for index, song in enumerate(album.songs, 1):
        logger.write("extracting {}...".format(song.name))
        song.extract_song_lyrics(driver)
        logger.write(config.get_output_path())
        logger.write(album.name)
        logger.write(song.lyrics)
        song.save_to_file(path=config.get_output_path(), album_name=album.name, index=index)
        logger.write("-" * 150)
