import os
from dotenv import load_dotenv
from lyricsgenius import Genius
from csv import DictWriter

load_dotenv()

token = os.getenv("GENIUS_API_TOKEN")

genius = Genius(
    token,
    skip_non_songs=True,
    # excluded_terms=["(Live)", "(Remix)", "(Acoustic)"],
    remove_section_headers=True,
    timeout=15,
    verbose=False
)

artist_name = 'Led Zeppelin'
artist = genius.search_artist(
    artist_name,
    # max_songs=150,
    sort="popularity")

if artist:
    with open('led_zeppelin.csv', 'w', newline='', encoding='utf-8') as f:
        writer = DictWriter(f, ['album', 'track', 'lyrics'])
        writer.writeheader()
        for song in artist.songs:
            album_name = song.album.name if song.album else ''
            track_name = song.title if song.title else ''
            track_lyrics = song.lyrics if song.lyrics else ''

            if track_name:
                row = {
                    'album': album_name,
                    'track': track_name,
                    'lyrics': track_lyrics
                }
                writer.writerow(row)
    print('Done.')
else:
    print(f"Não foi possível encontrar o artista {artist_name}.")
