import os
from TicTacToe import tictactoe_play
from Apple_music import \
    apple_music_genre_update, \
    apple_music_topcharts_update, \
    apple_music_genre_recommendation, \
    apple_music_topcharts_recommendation
from my_functions import \
    json_to_dict, \
    dict_keys_menu, \
    input_int_in_list, \
    random_pyjoke

MAX_WIDTH = 120

# filepath = "AppleMusicScrapping/AppleMusicGenreRecommendations.json"
while True:
    filepath = "mainmenu.json"
    data = json_to_dict(filepath)
    dict_keys_menu(data, MAX_WIDTH)
    indices = list(range(len(data.keys()) + 1))
    menu_item = input_int_in_list(indices)
    match menu_item:
        case 0:
            break
        case 1:
            pass
            random_pyjoke()
        case 2:
            apple_music_genre_update()
        case 3:
            apple_music_topcharts_update()
        case 4:
            apple_music_genre_recommendation(MAX_WIDTH)
        case 5:
            apple_music_topcharts_recommendation(MAX_WIDTH)
        case 6:
            tictactoe_play()

