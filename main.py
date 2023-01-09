from my_functions import *

from random import randint

MAX_WIDTH = 120

filepath = "AppleMusicScrapping/AppleMusicGenreRecommendations.json"
data = json_to_dict(filepath)

print_dict_keys_in_columns(data, MAX_WIDTH)

print()

genre = 32  # TODO change to input
data_key = list(data.keys())[genre - 1]
len_list = len(data[data_key])
random_choice = str(randint(1, len_list))

print(f'Your recommendation is: '
      f'{data[data_key][random_choice]["title"]}, By {data[data_key][random_choice]["artist"]}')
