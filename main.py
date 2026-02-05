import requests
from termcolor import cprint
import argparse
import re
from bs4 import BeautifulSoup
from pprint import pprint
import json
import os
from difflib import SequenceMatcher
from typing import Dict

def parse_to_dashes(s: str) -> str:
    words = s.strip().split(' ')
    words_lowercase = [x.lower() for x in words]
    return '-'.join(words_lowercase)

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def generate_url(artist: str, song: str) -> str:
    song_list = get_artist_song_list(artist)
    # ideal_url = f"/{parse_to_dashes(artist)}/{parse_to_dashes(song)}/"
    similar_songs = list(map(lambda x: (x['title'], x['url'], similarity(song, x['title'].lower())), song_list))
    similar_songs = list(filter(lambda x: x[2] > 0.3, similar_songs))
    similar_songs.sort(key=lambda x: x[2], reverse=True)

    similar_songs = similar_songs[:5] if len(similar_songs) > 5 else similar_songs

    selected_url = None
    if similar_songs[0][2] == 1.0:
        selected_url = similar_songs[0][1]
    else:
        print(f"Could not find \"{song}\". Select the song you intended:")
        for i, x in enumerate(similar_songs):
            print(f"[{i+1}]: {x[0]}")
        print("[6]: None of the above")
        selected_idx = int(input(">>> ")) # do try catch or do while here
        if selected_idx == 6:
            print("Your song could not be found :(")
            quit()
        selected_url = similar_songs[selected_idx-1][1]

    return f"https://www.cifraclub.com.br{selected_url}"

def get_song_page(artist, song):
    url = generate_url(artist, song)
    try:
        r = requests.get(url)
        if r.status_code == 301:
            raise Exception("This url was not found.")
        
        return r
    except:
        raise Exception("Something wrong happened.")

def cache_artist_songs(artist) -> list[Dict]:
    """
    Saves the song list for a given artist in a json file. Returns the song list as a dictionary.
    """
    artist_dashes = parse_to_dashes(artist)
    res = requests.get(f"https://www.cifraclub.com.br/{artist_dashes}/musicas.html")  
    page = res.text
    soup = BeautifulSoup(page, 'html.parser')
    song_urls = list(filter(lambda x: str(x.get('href')).startswith(f"/{artist_dashes}/"), soup.find_all('a')))

    # ignores first six elements bc they are not song links (from manual analysis)
    song_urls = list(map(lambda x: {"title": x.get_text(), "url": x.get('href')}, song_urls))[6:]

    os.makedirs("artists/", exist_ok=True)

    with open(f"artists/{artist_dashes}.json", mode="w+", encoding="utf-8") as write_file:
        json.dump(song_urls, write_file)

    print("Successfully cached song list for " + artist)   
    return song_urls

def get_artist_song_list(artist) -> list[Dict]:
    artist = parse_to_dashes(artist)

    if not os.path.isfile(f"artists/{artist}.json"):
        return cache_artist_songs(artist)

    data = ""
    with open(f"artists/{artist}.json", mode="r", encoding="utf-8") as f:
        data = f.read()
    
    return json.loads(data)
        

configs = {
    "color": {
        "chords": "green",
        "lyrics": "white",
    },
    "sparse": False,
}

if __name__ == "__main__":
    
    # parse CLI args
    parser = argparse.ArgumentParser(prog="cifraglub")
    parser.add_argument("artist")
    parser.add_argument("song")

    args = parser.parse_args()
    artist = args.artist
    song = args.song

    soup = BeautifulSoup(get_song_page(artist, song).text, "html.parser")
    chords = soup.find('pre') 
    
    if chords is not None:
        lines = chords.get_text().split('\n')
        lines = list(filter(lambda x: len(x) > 1, lines))

        for idx, l in enumerate(lines):
            if idx % 2 == 0:
                cprint(l, configs["color"]["chords"])
            else:
                cprint(l + ("\n" if configs["sparse"] else ""), configs["color"]["lyrics"])
            