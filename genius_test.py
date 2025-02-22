import os
from dotenv import load_dotenv
from lyricsgenius import Genius
from csv import DictWriter
import polars as pl

load_dotenv()
token = os.getenv("GENIUS_API_TOKEN")

artist = 'Led Zeppelin'
albums = ['Led Zeppelin',
          'Led Zeppelin II',
          'Led Zeppelin III',
          'Led Zeppelin IV',
          'Houses of the Holy',
          'Physical Graffiti',
          'Presence',
          'In Through the Out Door',
          'Coda']

genius = Genius(
    token,
    skip_non_songs=True,
    remove_section_headers=True,
    timeout=15,
    sleep_time=0.5,
)

for album in albums:
    a = genius.search_albums(album)
    print(dir(a))
    break
