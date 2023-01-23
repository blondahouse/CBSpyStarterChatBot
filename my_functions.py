import json
import pyjokes


def random_pyjoke():
    print(pyjokes.get_joke())


def input_int_in_list(values: list) -> int:
    while True:
        a = input("Enter your choice: ")
        try:
            if int(a) not in values:
                raise ValueError
        except ValueError:
            print("Wrong input, please try again!")
        else:
            return int(a)


def dict_keys_menu(dictionary, frame_width) -> None:
    dict_len = len(dictionary.keys()) + 1
    index_len = len(str(dict_len))
    item_max_len = max([len(x) for x in dictionary.keys()]) + index_len + 3
    col_number = frame_width // item_max_len if frame_width // item_max_len <= dict_len else dict_len
    col_width = frame_width // col_number
    row_number = abs(-dict_len // col_number)
    row_limit = dict_len % row_number if dict_len % row_number != 0 else row_number

    # print("index_len:", index_len)
    # print("item_max_len:", item_max_len)
    # print("col_number:", col_number)
    # print("col_width:", col_width)
    # print("row_number:", row_number)
    # print("row_limit:", row_limit)

    for row in range(row_number):
        check_col_number = col_number if row <= row_limit - 1 else col_number - 1
        for col in range(check_col_number):
            list_item = row + row_number * col
            if list_item == dict_len - 1:
                print(f'{"0": >{index_len}} '
                      f'{"Exit": <{col_width - index_len - 1}}', end='')
            else:
                print(f'{list_item + 1: >{index_len}} '
                      f'{list(dictionary.keys())[list_item]: <{col_width - index_len - 1}}', end='')
        print()


def json_to_dict(filepath: str) -> dict:
    with open(filepath, 'r', encoding='utf8') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    MAX_WIDTH = 120

    filepath = "AppleMusicScrapping/AppleMusicGenreRecommendations.json"
    # filepath = "mainmenu.json"

    data = json_to_dict(filepath)
    dict_keys_menu(data, MAX_WIDTH)
