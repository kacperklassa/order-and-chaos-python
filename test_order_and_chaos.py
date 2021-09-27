from order_and_chaos import Square, Board, Game, SquareNotEmptyError
import pytest


def test_board_create_board():
    board = Board()
    board.create_board()


def test_square_get_value():
    board = Board()
    board.create_board()
    assert board.get_square(2, 2).get_value() == ' '


def test_board_square_set_value_empty_square():
    board = Board()
    board.create_board()
    assert board.get_square(2, 2).get_value() == ' '
    board.square_set_value(2, 2, 'X')
    assert board.get_square(2, 2).get_value() == 'X'


def test_board_square_set_value_not_empty_square():
    board = Board()
    board.create_board()
    assert board.get_square(2, 2).get_value() == ' '
    board.square_set_value(2, 2, 'X')
    assert board.get_square(2, 2).get_value() == 'X'
    with pytest.raises(SquareNotEmptyError):
        board.square_set_value(2, 2, 'O')


def test_board_check_order_win_vertical():
    board = Board([
        [Square(), Square(), Square(), Square(), Square(), Square()],
        [Square(), Square(False, 'X'), Square(), Square(), Square(), Square()],
        [Square(), Square(False, 'X'), Square(), Square(), Square(), Square()],
        [Square(), Square(False, 'X'), Square(), Square(), Square(), Square()],
        [Square(), Square(False, 'X'), Square(), Square(), Square(), Square()],
        [Square(), Square(False, 'X'), Square(), Square(), Square(), Square()]
    ])
    assert board.check_order_win_condition() == True


def test_board_check_order_win_horizontal1():
    board = Board([
        [Square(), Square(), Square(), Square(), Square(), Square()],
        [Square(), Square(False, 'X'), Square(False, 'X'), Square(False, 'X'), Square(False, 'X'), Square(False, 'X')],
        [Square(), Square(), Square(), Square(), Square(), Square()],
        [Square(), Square(), Square(), Square(), Square(), Square()],
        [Square(), Square(), Square(), Square(), Square(), Square()],
        [Square(), Square(), Square(), Square(), Square(), Square()]
    ])
    assert board.check_order_win_condition() == True


def test_board_check_order_win_horizontal2():
    board = Board([
        [Square(), Square(), Square(), Square(), Square(), Square()],
        [Square(), Square(), Square(), Square(), Square(), Square()],
        [Square(), Square(), Square(), Square(), Square(), Square()],
        [Square(False, 'X'), Square(False, 'X'), Square(False, 'X'), Square(False, 'X'), Square(False, 'X'), Square()],
        [Square(), Square(), Square(), Square(), Square(), Square()],
        [Square(), Square(), Square(), Square(), Square(), Square()]
    ])
    assert board.check_order_win_condition() == True


def test_board_check_order_win_downward_diagonal():
    board = Board([
        [Square(), Square(False, 'X'), Square(), Square(), Square(), Square()],
        [Square(), Square(), Square(False, 'X'), Square(), Square(), Square()],
        [Square(), Square(), Square(), Square(False, 'X'), Square(), Square()],
        [Square(), Square(), Square(), Square(), Square(False, 'X'), Square()],
        [Square(), Square(), Square(), Square(), Square(), Square(False, 'X')],
        [Square(), Square(), Square(), Square(), Square(), Square()]
    ])
    assert board.check_order_win_condition() == True


def test_board_check_order_win_upward_diagonal():
    board = Board([
        [Square(), Square(), Square(), Square(), Square(), Square(False, 'X')],
        [Square(), Square(), Square(), Square(), Square(False, 'X'), Square()],
        [Square(), Square(), Square(), Square(False, 'X'), Square(), Square()],
        [Square(), Square(), Square(False, 'X'), Square(), Square(), Square()],
        [Square(), Square(False, 'X'), Square(), Square(), Square(), Square()],
        [Square(), Square(), Square(), Square(), Square(), Square()]
    ])
    assert board.check_order_win_condition() == True


def test_board_check_chaos_win():
    board = Board([
        [Square(False, 'X'), Square(False, 'O'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'O')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X')],
        [Square(False, 'X'), Square(False, 'O'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'O')],
        [Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'X'), Square(False, 'X')]
    ])
    assert board.check_chaos_win_condition() == True


def test_game_available_positions():
    board = Board([
        [Square(False, 'X'), Square(False, 'O'), Square(True), Square(False, 'X'), Square(False, 'O'), Square(False, 'X')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'O')],
        [Square(False, 'O'), Square(True), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X')],
        [Square(False, 'X'), Square(False, 'O'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'O')],
        [Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'X'), Square(True)]
    ])
    game = Game(board)
    assert game.available_positions() == [(0, 2), (3, 1), (5, 5)]


def test_game_npc_make_random_move(monkeypatch):
    board = Board([
        [Square(False, 'X'), Square(False, 'O'), Square(True), Square(False, 'X'), Square(False, 'O'), Square(False, 'X')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'O')],
        [Square(False, 'O'), Square(True), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X')],
        [Square(False, 'X'), Square(False, 'O'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'O')],
        [Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'X'), Square(True)]
    ])
    game = Game(board)
    assert game._game_board.get_square(3, 1).get_is_empty() == True
    def get_31(a):
        return (3, 1)
    monkeypatch.setattr('order_and_chaos.choice', get_31)
    game.npc_make_random_move('Order')
    assert game._game_board.get_square(3, 1).get_is_empty() == False
    assert game._game_board.get_square(3, 1).get_value() in {'X', 'O'}


def test_game_check_winner_order1():
    board = Board([
        [Square(), Square(), Square(), Square(), Square(), Square(False, 'X')],
        [Square(), Square(), Square(), Square(), Square(False, 'X'), Square()],
        [Square(), Square(), Square(), Square(False, 'X'), Square(), Square()],
        [Square(), Square(), Square(False, 'X'), Square(), Square(), Square()],
        [Square(), Square(False, 'X'), Square(), Square(), Square(), Square()],
        [Square(), Square(), Square(), Square(), Square(), Square()]
    ])
    game = Game(board)
    assert game.check_winner() == 'Order won the game!'


def test_game_check_winner_order2():
    board = Board([
        [Square(False, 'X'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'O')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X')],
        [Square(False, 'X'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'O')],
        [Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'X'), Square(False, 'X')]
    ])
    game = Game(board)
    assert game.check_winner() == 'Order won the game!'


def test_game_check_winner_chaos():
    board = Board([
        [Square(False, 'X'), Square(False, 'O'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'O')],
        [Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X')],
        [Square(False, 'X'), Square(False, 'O'), Square(False, 'O'), Square(False, 'X'), Square(False, 'O'), Square(False, 'O')],
        [Square(False, 'X'), Square(False, 'O'), Square(False, 'X'), Square(False, 'X'), Square(False, 'X'), Square(False, 'X')]
    ])
    game = Game(board)
    assert game.check_winner() == 'Chaos won the game!'
