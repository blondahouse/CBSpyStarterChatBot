import os
from art import text2art

LEFT_TAB = " " * 4
START_BOARD = (0, 0, 0, 0, 0, 0, 0, 0, 0)
ALL_MOVES = tuple(range(1, 10))
X_PLAYER = ("X", 1)
O_PLAYER = ("O", 2)
GLOBAL_GAME_STATUSES = {
    "on": 0,
    "win": 1,
    "off": 2
}
WIN_PATTERNS = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
)


def x_symbol(cell) -> tuple:
    x = text2art("x", font="univers").strip().split('\n')
    x = [f'{i.strip():^15}' for i in x]
    x1 = x.pop(0)
    x1 = f'{cell + 1}{x1[1:len(x1)]}'
    x.insert(0, x1)
    return x


def o_symbol(cell) -> list:
    o = text2art("o", font="univers").strip().split('\n')
    o = [f'{i.strip():^15}' for i in o]
    o1 = o.pop(0)
    o1 = f'{cell + 1}{o1[1:len(o1)]}'
    o.insert(0, o1)
    return o


def h_line() -> str:
    """
    ═══════════════╬═══════════════╬═══════════════
    """
    h = '═══════════════╬═══════════════╬═══════════════'
    return h


def v_line() -> str:
    """
    ║
    """
    t = '║'
    return t


def empty_line(cell) -> tuple:
    """

    """
    e = (f'{cell + 1}              ',
         f'               ',
         f'               ',
         f'               ',
         f'               ')
    return e


def select_pattern(num: int, cell):
    match num:
        case 0:
            return empty_line(cell)
        case 1:
            return x_symbol(cell)
        case 2:
            return o_symbol(cell)


def board_header():
    print(LEFT_TAB, '═' * 47)
    print(LEFT_TAB, f'{"TicTacToe Game": ^47}')
    print(LEFT_TAB, '═' * 47)


def board_footer(message):
    print(LEFT_TAB, '═' * 47)
    print(LEFT_TAB, f'Status: {message}')
    print(LEFT_TAB, f'or input \'exit\' to quit game.')


def change_player(c):
    n = O_PLAYER if c == X_PLAYER else X_PLAYER
    return n


def check_if_current_player_wins(board) -> bool:
    answer = False
    for pattern in WIN_PATTERNS:
        if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != 0:
            answer = True
    return answer


def render_board(pattern, message):
    board_header()
    for row in range(3):
        row_cells = []
        for col in range(3):
            cell = col + row * 3
            row_cells.append(select_pattern(pattern[cell], cell))
        for line in range(5):
            l1 = row_cells[0][line]
            l2 = row_cells[1][line]
            l3 = row_cells[2][line]
            print(LEFT_TAB, f'{l1}{v_line()}{l2}{v_line()}{l3}')
        if row < 2:
            print(LEFT_TAB, h_line())
    board_footer(message)


def tictactoe_play():
    current_board = list(START_BOARD)
    current_player = X_PLAYER
    available_moves = list(ALL_MOVES)
    is_win = False
    status = f'The game started, Player "{current_player[0]}" moves'
    while True:
        render_board(current_board, status)
        a = input(LEFT_TAB + " Your input: ")
        if is_win or not len(available_moves):
            current_board = list(START_BOARD)
            current_player = X_PLAYER
            available_moves = list(ALL_MOVES)
            is_win = False
            status = f'The game started, Player "{current_player[0]}" moves'
            os.system('cls')
        elif a == "exit":
            os.system('cls')
            break
        else:
            try:
                if int(a) not in available_moves:
                    raise ValueError
            except ValueError:
                status = f'Wrong input, Player "{current_player[0]}" still moves'
                os.system('cls')
            else:
                a = int(a)
                current_board[a - 1] = current_player[1]
                available_moves.remove(a)
                is_win = check_if_current_player_wins(current_board)
                if not len(available_moves):
                    status = f'Nobody wins! Any input to play again.'
                elif is_win:
                    available_moves = []
                    status = f'Player "{current_player[0]}" wins! Any input to play again.'
                else:
                    current_player = change_player(current_player)
                    status = f'The game is on, Player "{current_player[0]}" moves'

                os.system('cls')


if __name__ == "__main__":
    x_t = x_symbol(1)
    for i in x_t:
        print(i)
    tictactoe_play()
