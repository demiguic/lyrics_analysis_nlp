"""
CSV =

Album: nome do disco
Data: ano de lançamento
Música: título da faixa
letra: letra da música

Led Zeppelin I | 1969 | Good Times Bad Times | In the days of my youth...
"""

from csv import DictWriter
import time
import dateparser
from httpx import get
from parsel import Selector

TIME_OUT = 10
SLEEP_TIME = 2

ALBUNS = [
    ("Led Zeppelin I", "1969", "https://genius.com/albums/Led-zeppelin/Led-zeppelin"),
    ("Led Zeppelin II", "1969", "https://genius.com/albums/Led-zeppelin/Led-zeppelin-ii"),
    ("Led Zeppelin III", "1970",
     "https://genius.com/albums/Led-zeppelin/Led-zeppelin-iii"),
    ("Led Zeppelin IV", "1971", "https://genius.com/albums/Led-zeppelin/Led-zeppelin-iv"),
    ("Houses of the Holy", "1973",
     "https://genius.com/albums/Led-zeppelin/Houses-of-the-holy"),
    ("Physical Graffiti", "1975",
     "https://genius.com/albums/Led-zeppelin/Physical-graffiti"),
    ("Presence", "1976", "https://genius.com/albums/Led-zeppelin/Presence"),
    ("In Through the Out Door", "1979",
     "https://genius.com/albums/Led-zeppelin/In-through-the-out-door")
]


def get_lyrics(url: str) -> str:
    """Returns the lyrics of a song from a URL"""
    response = get(url, timeout=TIME_OUT)
    s = Selector(response.text)
    letra = '\n'.join(s.css('[data-lyrics-container]::text').getall())
    return letra


def get_tracks(url: str) -> list[tuple[str, str]]:
    """Returns a list of tuples with track name and URL"""
    response = get(url, timeout=TIME_OUT)
    s = Selector(response.text)
    tracks = s.css('div.chart_row-content')
    return [
        (track.css('h3::text').get().strip(), track.css('a').attrib['href'])
        for track in tracks
    ]


url = "https://genius.com/artists/Led-zeppelin/albums"

with open('led_zeppelin.csv', 'w', newline='', encoding='utf-8') as f:
    writer = DictWriter(f, ['album', 'date', 'track', 'lyrics'])
    writer.writeheader()

    for album in ALBUNS:
        print(f"Getting tracks from {album[0]}...")
        for track in get_tracks(album[2]):
            row = {
                'album': album[0],
                'date': dateparser.parse(album[1]),
                'track': track[0],
                'lyrics': get_lyrics(track[1])
            }
            writer.writerow(row)
            time.sleep(SLEEP_TIME)
    print('Done.')
