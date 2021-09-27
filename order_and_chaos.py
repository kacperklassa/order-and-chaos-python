'''
Order and Chaos game

base rules:
- 6x6 board
- two players - Order, Chaos
- Order needs to create consequtive 5 X's or O's in a row to win
- Chaos tries to prevent Order from achieving that goal

classes:
- Game
- Board
- Square
- SquareNotEmptyError
'''
from os import system, name
from time import sleep
from random import choice, randint


class SquareNotEmptyError(Exception):
    def __init__(self):
        super().__init__('You can only use empty squares')


class Board:
    def __init__(self, board=None):
        self._board = board if board else [[], [], [], [], [], []]

    def create_board(self):
        for sublist in self._board:
            for _ in range(6):
                sublist.append(Square(True))

    def get_board(self):
        return self._board

    def show_board(self):
        print("_|_1___2___3___4___5___6_")
        i = 0
        for sublist in self._board:
            j=0
            print(f"{i+1}|", end='')
            for item in sublist:
                if j < 5:
                    print(' ' + item.get_value(), end=' ' + '|')
                    j += 1
                else:
                    print(' ' + item.get_value(), end=' ')
            if i < 5:
                print('\n' + '-'*25)
                i += 1
            else:
                print('\n')


    def get_square(self, row, col):
        '''
        returns a Square object on a given position
        '''
        return self._board[int(row)][int(col)]

    def square_set_value(self, row, col, new_value):
        '''
        raises SquareNotEmptyError if the chosen square
        was already assigned a valid value
        '''
        if self.get_square(row, col).get_is_empty() == True:
            self.get_square(row, col).set_value(new_value.upper())
        else:
            raise SquareNotEmptyError()

    def clear(self):
        '''
        clears console output
        '''
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def check_order_win_condition(self):
        '''
        Order player wins if there is a line of five like pieces on the board
        either vertically, horizontally or diagonally
        '''
        #check vertical wins
        for col in range(0, 6):
            for start_row in range(0, 2):
                win = True
                expected_value = self.get_square(start_row, col).get_value()
                if expected_value == 'X' or expected_value =='O':
                    for row in range(start_row, start_row+5):
                        if self.get_square(row, col).get_value() != expected_value:
                            win = False
                    if win:
                        return win

        #check horizontal wins
        for row in range(0, 6):
            for start_col in range(0, 2):
                win = True
                expected_value = self.get_square(row, start_col).get_value()
                if expected_value == 'X' or expected_value =='O':
                    for col in range(start_col, start_col+5):
                        if self.get_square(row, col).get_value() != expected_value:
                            win = False
                    if win:
                        return win

        #check downward diagonal wins
        start_points = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for point in start_points:
            win = True
            start_row, start_col = point
            expected_value = self.get_square(start_row, start_col).get_value()
            if expected_value == 'X' or expected_value =='O':
                for i in range(0, 5):
                    if self.get_square(start_row + i, start_col + i).get_value() != expected_value:
                        win = False
                if win:
                    return win

        #check upward diagonal wins
        win = True
        start_points = [(4, 0), (4, 1), (5, 0), (5, 1)]
        for point in start_points:
            win = True
            start_row, start_col = point
            expected_value = self.get_square(start_row, start_col).get_value()
            if expected_value == 'X' or expected_value =='O':
                for i in range(0, 5):
                    if self.get_square(start_row - i, start_col + i).get_value() != expected_value:
                        win = False
                if win:
                    return win

        return False

    def check_chaos_win_condition(self):
        '''
        Chaos player wins only when the board is filled
        without completion of a line of five like pieces
        '''
        all_full = True
        for sublist in self.get_board():
            for square in sublist:
                if square.get_is_empty() == True:
                    all_full = False
        return all_full




class Square:
    def __init__(self, is_empty=True, value=None):
        '''
        param _is_empty - holds information whether there is a value in this square or if it's empty
        type _is_empty = bool

        param _value - can be either X, O or None
        type _value = str
        '''
        self._is_empty = is_empty
        self._value = value

    def get_value(self):
        return self._value if self._value else " "

    def set_value(self, new_value):
        self._value = new_value.upper()
        self._is_empty = False

    def get_is_empty(self):
        return self._is_empty


class Game:
    '''
    has methods allowing for gameplay:

    self.play_pvp() - between two human players

    self.play_npc(mode) - between a human player and a bot,
    bot makes either random moves or utilizes a best move algorythm,
    according to the mode argument

    param mode -
    type mode = str
    '''
    def __init__(self, board=None):
        if not board:
            self._game_board = Board()
            self._game_board.create_board()
        else:
            self._game_board = board

    def play_pvp(self):
        self._game_board.clear()
        run = True
        round_id = 1
        while run:
            player = 'Order' if round_id%2 == 1 else 'Chaos'
            self._game_board.show_board()
            if self.player_make_move(player):
                return
            if self.check_winner():
                self._game_board.clear()
                self._game_board.show_board()
                print(self.check_winner())
                return
            self._game_board.clear()
            round_id += 1

    def play_npc(self, mode):
        self._game_board.clear()
        player = str()
        while not player:
            print('Do you want to play as Order or as Chaos? (1 for Order, 2 for Chaos)')
            choice = input('> ')
            if choice == '1':
                player = 'Order'
                enemy = 'Chaos'
            elif choice == '2':
                player = 'Chaos'
                enemy = 'Order'
            else:
                print('Invalid choice')
        self._game_board.clear()
        run = True
        round_id = 1
        while run:
            self._game_board.show_board()
            if round_id%2 == 1:
                if player == 'Order':
                    if self.player_make_move(player):
                        return
                else:
                    if mode == 'random':
                        print(self.npc_make_random_move(enemy))
                        sleep(1)
                    else:
                        print(self.npc_make_best_move(enemy))
                        sleep(1)
            elif round_id%2 == 0:
                if player == 'Chaos':
                    if self.player_make_move(player):
                        return
                else:
                    if mode == 'random':
                        print(self.npc_make_random_move(enemy))
                        sleep(1)
                    else:
                        print(self.npc_make_best_move(enemy))
                        sleep(1)
            if self.check_winner():
                self._game_board.clear()
                self._game_board.show_board()
                print(self.check_winner())
                return
            self._game_board.clear()
            round_id += 1


    def check_winner(self):
        '''
        returns a string with adequate information when either of the player's win condition is met
        '''
        order_win = self._game_board.check_order_win_condition()
        if order_win:
            return 'Order won the game!'
        elif self._game_board.check_chaos_win_condition():
            return 'Chaos won the game!'


    def player_make_move(self, player):
        '''
        asks player to input the value they want to set, either 'X' or 'O',
        and coordinates of the square in which they want to set it in row, column order

        the function does not end until valid data is given
        '''
        valid_values = {'X', 'x', 'O', 'o'}
        valid_coordinates = {str(i) for i in range(1, 7)}
        move = False
        while not move:
            try:
                print(f"{player}'s turn")
                value = str()
                while not value:
                    player_value = input("Choose value - X or O (or input sur if you want to surrender): ")
                    if player_value == 'sur':
                        surrender = True
                        return surrender
                    elif player_value in valid_values:
                        value = player_value
                    else:
                        print('Incorrect value - please choose between X and O')
                coordinates_set = False
                while not coordinates_set:
                    print("Where do you want to put it? (row, column)")
                    row_input = input("> ")
                    column_input = input("> ")
                    if column_input not in valid_coordinates or row_input not in valid_coordinates:
                        print('Column and row values must be from range 1 to 6')
                    else:
                        row = str(int(row_input) - 1)
                        column = str(int(column_input) - 1)
                        coordinates_set = True
                self._game_board.square_set_value(row, column, value)
            except SquareNotEmptyError as e:
                print(e)
                sleep(1)
                self._game_board.clear()
                self._game_board.show_board()
            else:
                move = True

    def available_positions(self):
        '''
        iterates through the board, if a given Square object's param _is_empty is equal true,
        adds it's coordinates in a form of a tuple to the postions list which is returned by the function
        '''
        positions = []
        for row in range(6):
            for col in range(6):
                if self._game_board.get_square(row, col).get_is_empty():
                    positions.append((row, col))
        return positions

    def npc_make_random_move(self, role):
        '''
        gets a list of available positions from the available_positions method,
        then chooses random tuple with coordinates out of it,
        draws a random value and sets a corresponding square to that value
        '''
        positions = self.available_positions()
        row, col = choice(positions)
        value = 'X' if randint(0, 2) == 1 else 'O'
        self._game_board.square_set_value(row, col, value)
        return f'{role} puts {value} on position {row + 1}, {col + 1}'

    def npc_make_best_move(self, role):
        '''
        analizes the board similarly to win condition functions
        calculates Xs and Os in a given row, column or diagonal
        decides the move on the basis of max count scores
        '''
        self.max_X_count = 0
        self.max_O_count = 0
        best_positions = []

        #vertical combinations
        for col in range(0, 6):
            for start_row in range(0, 2):
                X_count = 0
                O_count = 0
                empty_positions = []
                for row in range(start_row, start_row+5):
                    if self._game_board.get_square(row, col).get_value() == 'X':
                        X_count += 1
                    elif self._game_board.get_square(row, col).get_value() == 'O':
                        O_count += 1
                    else:
                        empty_positions.append((row, col))
                if empty_positions and (X_count > self.max_X_count or O_count > self.max_O_count):
                    value = self.decide_best_value(X_count, O_count, role)
                    if value:
                        best_value = value
                        best_positions = empty_positions

        #horizontal combinations
        for row in range(0, 6):
            for start_col in range(0, 2):
                X_count = 0
                O_count = 0
                empty_positions = []
                for col in range(start_col, start_col + 5):
                    if self._game_board.get_square(row, col).get_value() == 'X':
                        X_count += 1
                    elif self._game_board.get_square(row, col).get_value() == 'O':
                        O_count += 1
                    else:
                        empty_positions.append((row, col))
                    if empty_positions and (X_count > self.max_X_count or O_count > self.max_O_count):
                        value = self.decide_best_value(X_count, O_count, role)
                        if value:
                            best_positions = empty_positions
                            best_value = value


        #downward diagonal combinations
        start_points = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for point in start_points:
            start_row, start_col = point
            X_count = 0
            O_count = 0
            empty_positions = []
            for i in range(0, 5):
                if self._game_board.get_square(start_row + i, start_col + i).get_value() == 'X':
                        X_count += 1
                elif self._game_board.get_square(start_row + i, start_col + i).get_value() == 'O':
                    O_count += 1
                else:
                    empty_positions.append((start_row + i, start_col + i))
                if empty_positions and (X_count > self.max_X_count or O_count > self.max_O_count):
                    value = self.decide_best_value(X_count, O_count, role)
                    if value:
                        best_positions = empty_positions
                        best_value = value

        #upward diagonal combinations
        start_points = [(4, 0), (4, 1), (5, 0), (5, 1)]
        for point in start_points:
            start_row, start_col = point
            X_count = 0
            O_count = 0
            empty_positions = []
            for i in range(0, 5):
                if self._game_board.get_square(start_row - i, start_col + i).get_value() == 'X':
                        X_count += 1
                elif self._game_board.get_square(start_row - i, start_col + i).get_value() == 'O':
                    O_count += 1
                else:
                    empty_positions.append((start_row - i, start_col + i))
                if empty_positions and (X_count > self.max_X_count or O_count > self.max_O_count):
                    value = self.decide_best_value(X_count, O_count, role)
                    if value:
                        best_positions = empty_positions
                        best_value = value


        if best_positions:
            row, col = choice(best_positions)
            self._game_board.square_set_value(row, col, best_value)
            return f'{role} puts {best_value} on position {row}, {col}'
        else:
            return self.npc_make_random_move(role)



    def decide_best_value(self, X_count, O_count, role):
        value = str()
        if X_count > O_count and X_count > self.max_X_count:
            self.max_X_count = X_count
            if role == 'Chaos':
                value = 'O'
            else:
                value = 'X'
        elif X_count < O_count and O_count > self.max_O_count:
            self.max_O_count = O_count
            if role == 'Chaos':
                value = 'X'
            else:
                value = 'O'
        if not value:
            return None
        return value
