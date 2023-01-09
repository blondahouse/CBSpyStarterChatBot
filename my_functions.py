import json


def print_dict_keys_in_columns(dictionary, frame_width) -> None:
    index_len = len(str(len(dictionary.keys())))
    item_max_len = max([len(x) for x in dictionary.keys()]) + index_len + 3
    col_number = frame_width // item_max_len
    col_width = frame_width // col_number
    row_number = abs(-len(dictionary.keys()) // col_number)
    row_limit = len(dictionary.keys()) % row_number

    for row in range(row_number):
        check_col_number = col_number if row <= row_limit - 1 else col_number - 1
        for col in range(check_col_number):
            list_item = row + row_number * col
            print(f'{list_item + 1: >{index_len}} '
                  f'{list(dictionary.keys())[list_item]: <{col_width - index_len - 1}}', end='')
        print()


def json_to_dict(filepath: str) -> dict:
    with open(filepath, 'r', encoding='utf8') as f:
        data = json.load(f)
    return data
