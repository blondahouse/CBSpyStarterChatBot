import json
import re
import requests
from bs4 import BeautifulSoup


def apple_music_get_songs_from_curator(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(attrs={
        "aria-label": re.compile("Best New Songs|Best New Tracks|Hot Tracks|Featured Tracks|Featured Songs")
    })

    job_elements = results.find_all("div", attrs={"data-testid": "track-lockup"})

    songs = {}
    counter = 0
    for job_element in job_elements:
        counter += 1
        title = job_element.find("li", class_=re.compile("track-lockup__title"))
        title = title.text.strip()

        artists = job_element.find("li", class_=re.compile("track-lockup__subtitle"))
        artists = artists.text.strip()

        songs[counter] = {
            "title": title,
            "artist": artists
        }
    return songs


def apple_music_get_genres(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("main")

    job_elements = results.find_all("li", class_="grid-item svelte-1tas3ca")

    top100_charts = {}

    for job_element in job_elements:
        genre_name = job_element.find("a")
        genre_name = genre_name.text
        genre_name = re.sub(r'Apple Music|Apple', '', genre_name)
        genre_name = genre_name.strip()

        genre_link = job_element.find("a")["href"]
        try:
            songs = apple_music_get_songs_from_curator(genre_link)
        except:
            pass
        else:
            top100_charts[genre_name] = songs
            
    return top100_charts


def write_json(dict_in, file_name):
    with open(file_name, 'w', encoding='utf8') as f:
        json.dump(dict_in, f, ensure_ascii=False)


def apple_genre_update():
    url = "https://music.apple.com/us/room/1654814539"
    filename = "AppleMusicGenreRecommendations.json"
    dictionary = apple_music_get_genres(url)
    # print(dictionary.keys())
    write_json(dictionary, filename)


if __name__ == "__main__":
    apple_genre_update()
