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


def get_albums(url: str) -> list[tuple[str | None, str | None, str | None]]:
    """Returns a list of tuples with album name, URL, and release date"""
    response = get(url, timeout=TIME_OUT)
    s = Selector(response.text)
    albums = s.css('.ZvWhZ')

    albums_list = []

    for album in albums:
        album_url = album.css('.kqeBAm').attrib["href"]
        album_name = album.css('.gpuzaZ::text').get()
        album_date = album.css('.cedmJJ::text').get()

        albums_list.append(
            (album_url, album_name, album_date)
        )
    return albums_list


url = "https://genius.com/artists/Led-zeppelin/albums"

with open('led_zeppelin.csv', 'w', newline='', encoding='utf-8') as f:
    writer = DictWriter(f, ['album', 'date', 'track', 'lyrics'])
    writer.writeheader()

    for album in get_albums(url):
        for track in get_tracks(album[0]):
            row = {
                'album': album[1],
                'date': dateparser.parse(album[2]),
                'track': track[0],
                'lyrics': get_lyrics(track[1])
            }
            writer.writerow(row)
            time.sleep(SLEEP_TIME)
    print('done.')
