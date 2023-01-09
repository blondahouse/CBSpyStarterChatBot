import json
import re
import requests
from bs4 import BeautifulSoup


def apple_music_get_songs_from_playlist(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="songs-list svelte-n1wn2z songs-list--header-is-visible songs-list--playlist")

    job_elements = results.find_all("div", class_="songs-list-row svelte-1yo4jst "
                                                  "songs-list-row-"
                                                  "-artwork songs-list-row-"
                                                  "-two-lines songs-list-row-"
                                                  "-playlist songs-list-row--preview")

    songs = {}
    counter = 0
    for job_element in job_elements:
        counter += 1
        title = job_element.find("div", class_="songs-list-row__song-name svelte-1yo4jst")
        title = title.text.strip()

        artist = job_element.find("a", class_="click-action")
        artist = artist.text.strip()

        songs[counter] = {
            "title": title,
            "artist": artist
        }
    return songs


def apple_music_get_topcharts(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="section-content svelte-1g7ob8i")

    job_elements = results.find_all("li", class_="grid-item svelte-1tas3ca")

    top100_charts = {}

    for job_element in job_elements:
        chart_name = job_element.find("a", class_="product-lockup__title svelte-4lw5dn")
        chart_name = chart_name.text
        chart_name = re.findall(r':(.+)', chart_name)
        chart_name = chart_name[0].strip()

        chart_link = job_element.find("a")["href"]
        songs = apple_music_get_songs_from_playlist(chart_link)

        top100_charts[chart_name] = songs
    return top100_charts


def write_json(dict_in, file_name):
    with open(file_name, 'w', encoding='utf8') as f:
        json.dump(dict_in, f, ensure_ascii=False)


if __name__ == "__main__":
    URL = "https://music.apple.com/us/browse/top-charts/dailyGlobalTopCharts/"
    FILENAME = "AppleMusicTopChartByCountry.json"

    dictionary = apple_music_get_topcharts(URL)
    write_json(dictionary, FILENAME)
