import json
import re
import time
import requests

from random import randint
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

from my_functions import json_to_dict, input_int_in_list, dict_keys_menu


def apple_music_get_songs_from_curator(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(attrs={
        "aria-label": re.compile("Best New Songs|Best New Tracks|Hot Tracks|Featured Tracks|Featured Songs")
    })

    job_elements = results.find_all("div", attrs={"data-testid": "track-lockup"})

    songs = {}
    counter = 0
    # for job_element in tqdm(job_elements):
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
    # for job_element in tqdm(job_elements):
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


def apple_music_get_genres(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Opens the browser up in background

    with Chrome(options=chrome_options) as browser:
        browser.get(url)
        html = browser.page_source

    # page = requests.get(url)
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find("main")

    job_elements = results.find_all("li", class_="grid-item svelte-1tas3ca")

    top100_charts = {}

    for job_element in tqdm(job_elements):
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


def apple_music_get_topcharts(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Opens the browser up in background

    with Chrome(options=chrome_options) as browser:
        browser.get(url)
        # Get scroll height after first time page load
        last_height = browser.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page / use a better technique like `waitforpageload` etc., if possible
            time.sleep(2)
            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        # time.sleep(3)
        html = browser.page_source

    # page = requests.get(url)
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find("div", class_="section-content svelte-1g7ob8i")

    job_elements = results.find_all("li", class_="grid-item svelte-1tas3ca")

    top100_charts = {}

    for job_element in tqdm(job_elements):
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


def apple_music_genre_update():
    url = "https://music.apple.com/us/room/1654814539"
    filename = "AppleMusicScrapping/AppleMusicGenreRecommendations.json"
    dictionary = apple_music_get_genres(url)
    write_json(dictionary, filename)


def apple_music_topcharts_update():
    url = "https://music.apple.com/us/browse/top-charts/dailyGlobalTopCharts/"
    filename = "AppleMusicScrapping/AppleMusicTopChartByCountry.json"
    dictionary = apple_music_get_topcharts(url)
    write_json(dictionary, filename)


def apple_music_genre_recommendation(max_width):
    filepath = "AppleMusicScrapping/AppleMusicGenreRecommendations.json"
    data = json_to_dict(filepath)
    dict_keys_menu(data, max_width)
    indices = list(range(len(data.keys()) + 1))
    menu_item = input_int_in_list(indices)
    data_key = list(data.keys())[menu_item - 1]
    len_list = len(data[data_key])
    random_choice = str(randint(1, len_list))
    print(f'Your recommendation is: '
          f'{data[data_key][random_choice]["title"]}, By {data[data_key][random_choice]["artist"]}')


def apple_music_topcharts_recommendation(max_width):
    filepath = "AppleMusicScrapping/AppleMusicTopChartByCountry.json"
    data = json_to_dict(filepath)
    dict_keys_menu(data, max_width)
    indices = list(range(len(data.keys()) + 1))
    menu_item = input_int_in_list(indices)
    data_key = list(data.keys())[menu_item - 1]
    len_list = len(data[data_key])
    random_choice = str(randint(1, len_list))
    print(f'Your recommendation is: '
          f'{data[data_key][random_choice]["title"]}, By {data[data_key][random_choice]["artist"]}')


if __name__ == "__main__":
    apple_music_genre_update()
    apple_music_topcharts_update()
