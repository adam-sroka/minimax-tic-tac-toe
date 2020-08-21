import random


class Field:
    def __init__(self, cells: str, side_length=3):
        self.cells = [cell if cell != '_' else ' ' for cell in cells]
        self.side_length = side_length
        if len(self.cells) % self.side_length != 0:
            raise Exception('The number of cells must be exactly divisible by side length!')

    def __repr__(self):
        field_cells = '---------\n|'
        for i, cell in enumerate(self.cells):
            if (i + 1) % self.side_length == 0:
                field_cells = field_cells + ' ' + cell + ' |\n|'
            else:
                field_cells = field_cells + ' ' + cell
        field_cells = field_cells[:-1] + '---------'  # slicing to remove extra '|'
        return field_cells

    def update_cells(self, cells: str):
        self.cells = [cell if cell != '_' else ' ' for cell in cells]
        if len(self.cells) % self.side_length != 0:
            raise Exception('The number of cells must be exactly divisible by side length!')

    def check_cell_coordinates(self, cell_x_coord: int, cell_y_coord: int):
        if (cell_x_coord > self.side_length or cell_y_coord > self.side_length or
                cell_x_coord < 1 or cell_y_coord < 1):
            raise ValueError(f'Cell coordinates must be from 1 to {self.side_length}!')

    def get_cell_index(self, cell_x_coord: int, cell_y_coord: int):
        """Get cell index in self.cells list from cell coordinates"""
        self.check_cell_coordinates(cell_x_coord, cell_y_coord)
        return - (cell_y_coord * self.side_length - cell_x_coord + 1)  # +1 due to reverse indexing

    def find_cell_indices_value(self, value: str):
        """Returns a list of indices of cells of matching value"""
        indices = list()
        for index, cell_value in enumerate(self.cells):
            if cell_value == value:
                indices.append(index)
        return indices

    def get_cell_value(self, cell_x_coord: int, cell_y_coord: int):
        self.check_cell_coordinates(cell_x_coord, cell_y_coord)
        cell_index = self.get_cell_index(cell_x_coord, cell_y_coord)
        return self.cells[cell_index]

    def update_cell_by_coords(self, cell_x_coord: int, cell_y_coord: int, value: str):
        self.check_cell_coordinates(cell_x_coord, cell_y_coord)
        cell_index = self.get_cell_index(cell_x_coord, cell_y_coord)
        self.cells[cell_index] = value

    def update_cell_by_index(self, cell_index: int, value: str):
        self.cells[cell_index] = value

    def count_given_cells(self, given_cell: str):
        return self.cells.count(given_cell)

    def get_cell_rows(self):
        rows = list()
        for i in range(self.side_length):
            rows.append(self.cells[i * self.side_length:(i + 1) * self.side_length])
        return rows

    def get_cell_columns(self):
        columns = list()
        for i in range(self.side_length):
            column = list()
            for j in range(self.side_length):
                column.append(self.cells[i + j * self.side_length])
            columns.append(column)
        return columns

    def get_cell_diagonals(self):
        first_diag = list()
        second_diag = list()
        for i in range(self.side_length):
            first_diag.append(self.cells[i * self.side_length + i])
            second_diag.append(self.cells[i * self.side_length + self.side_length - (i + 1)])
        return first_diag, second_diag

    def has_straight(self, symbol: str):
        for row in self.get_cell_rows():  # Horizontal straights
            if row.count(symbol) == self.side_length:
                return True
        for column in self.get_cell_columns():  # Vertical straights
            if column.count(symbol) == self.side_length:
                return True
        for diagonal in self.get_cell_diagonals():  # Diagonal straights
            if diagonal.count(symbol) == self.side_length:
                return True
        return False

    def find_indices_for_straights(self, symbol: str, empty_symbol=' '):
        straights_indices = list()
        rows = self.get_cell_rows()
        for row_number, row in enumerate(rows):
            if row.count(symbol) == self.side_length - 1:
                for cell_index, cell in enumerate(row):
                    if cell == empty_symbol:
                        straights_indices.append(row_number * self.side_length + cell_index)
        columns = self.get_cell_columns()
        for column_number, column in enumerate(columns):
            if column.count(symbol) == self.side_length - 1:
                for cell_index, cell in enumerate(column):
                    if cell == empty_symbol:
                        straights_indices.append(cell_index * self.side_length + column_number)
        diagonals = self.get_cell_diagonals()
        if diagonals[0].count(symbol) == self.side_length - 1:
            for cell_index, cell in enumerate(diagonals[0]):
                if cell == empty_symbol:
                    straights_indices.append(cell_index * self.side_length + cell_index)
        if diagonals[1].count(symbol) == self.side_length - 1:
            for cell_index, cell in enumerate(diagonals[1]):
                if cell == empty_symbol:
                    straights_indices.append(cell_index * self.side_length + self.side_length - (cell_index + 1))
        return straights_indices


def mini_max(current_field: Field, symbol: str, maximizing_symbol: str, symbols=('X', 'O')):
    """Returns the maximum/minimum score for a given symbol and a given field by running the mini max algorithm.
    Returns maximum score if symbol is the first element in symbols and minimum score if it is the second element."""
    symbol_1_win = current_field.has_straight(symbols[0])
    symbol_2_win = current_field.has_straight(symbols[1])
    current_field_has_empty = current_field.count_given_cells(' ') > 0
    if current_field_has_empty and (not symbol_1_win and not symbol_2_win):
        pass
    elif not current_field_has_empty and (not symbol_1_win and not symbol_2_win):
        return 0
    elif symbol_1_win:
        return 1  # Symbol 1 maximizes score
    elif symbol_2_win:
        return -1  # Symbol 2 minimizes score
    scores = list()
    empty_cell_indices = current_field.find_cell_indices_value(' ')
    new_symbol = [_symbol for _symbol in symbols if _symbol != symbol][0]
    for possible_move_index in empty_cell_indices:
        current_field_cells = current_field.cells.copy()
        current_field_cells[possible_move_index] = symbol
        new_current_field = Field('_________')
        new_current_field.cells = current_field_cells
        scores.append(mini_max(new_current_field, new_symbol, maximizing_symbol))
    return max(scores) if symbol == symbols[0] else min(scores)  # symbols[0] maximizes score


class Game:
    def __init__(self, cells='_________', side_length=3):
        self.field = Field(cells, side_length=side_length)

    def show_game(self):
        print(self.field)

    def is_move_valid(self, move: str, verbose=True):
        try:
            x_coord = int(move[0])
            y_coord = int(move[-1])
        except ValueError:
            if verbose:
                print('You should enter numbers!')
            return False

        try:
            self.field.check_cell_coordinates(x_coord, y_coord)
        except ValueError:
            if verbose:
                print('Coordinates should be from 1 to 3!')
            return False

        if self.field.get_cell_value(x_coord, y_coord) != ' ':
            if verbose:
                print('This cell is occupied! Choose another one!')
            return False
        return True

    def get_move_symbol(self, symbol_1='X', symbol_2='O'):
        symbol_1_num = self.field.count_given_cells(symbol_1)
        symbol_2_num = self.field.count_given_cells(symbol_2)
        if symbol_1_num == symbol_2_num:
            return symbol_1
        elif symbol_1_num == symbol_2_num + 1:
            return symbol_2
        else:
            raise ValueError(f'Invalid number of {symbol_1}s and {symbol_2}s on field!')

    def update_game_with_move(self, valid_x_coord: int, valid_y_coord: int, symbol: str):
        self.field.update_cell_by_coords(valid_x_coord, valid_y_coord, symbol)

    def is_game_done(self, symbol_1='X', symbol_2='O', verbose=True):
        symbol_1_win = self.field.has_straight(symbol_1)
        symbol_2_win = self.field.has_straight(symbol_2)
        field_has_empty = self.field.count_given_cells(' ') > 0
        if field_has_empty and (not symbol_1_win and not symbol_2_win):
            if verbose:
                print('Game not finished')
            return False
        elif not field_has_empty and (not symbol_1_win and not symbol_2_win):
            if verbose:
                print('Draw')
        elif symbol_1_win:
            if verbose:
                print(f'{symbol_1} wins')
        elif symbol_2_win:
            if verbose:
                print(f'{symbol_2} wins')
        return True

    def make_easy_move(self, symbol):
        """Picks a random spot and makes a move with symbol"""
        empty_cell_indices = self.field.find_cell_indices_value(' ')
        move_index = random.choice(empty_cell_indices)
        self.field.update_cell_by_index(move_index, symbol)

    def make_medium_move(self, symbol, symbols=('X', 'O')):
        """Tries to find a spot that either wins the game for symbol or prevents the other symbol from winning.
        If no such spot for a move is found, it performs an easy move"""
        winning_indices = self.field.find_indices_for_straights(symbol)
        opponent_symbol = [char for char in symbols if char != symbol][0]
        opponent_winning_indices = self.field.find_indices_for_straights(opponent_symbol)
        if winning_indices:
            self.field.update_cell_by_index(winning_indices[0], symbol)
        elif opponent_winning_indices:
            self.field.update_cell_by_index(opponent_winning_indices[0], symbol)
        else:
            self.make_easy_move(symbol)

    def make_hard_move(self, symbol, symbols=('X', 'O')):
        best_score = - float('inf') if symbol == symbols[0] else float('inf')
        best_move_index = None
        empty_cell_indices = self.field.find_cell_indices_value(' ')
        new_symbol = [_symbol for _symbol in symbols if _symbol != symbol][0]
        for possible_move_index in empty_cell_indices:
            possible_field_cells = self.field.cells.copy()
            possible_field_cells[possible_move_index] = symbol
            temp_field = Field('_________')
            temp_field.cells = possible_field_cells
            score = mini_max(temp_field, new_symbol, symbol)  # not sure if new_symbol and symbol are right
            if (symbol == symbols[0] and score > best_score) or (symbol == symbols[1] and score < best_score):
                best_score = score
                best_move_index = possible_move_index
        if best_move_index is None:
            raise ValueError('Invalid mini_max result')
        self.field.update_cell_by_index(best_move_index, symbol)

    def make_bot_move(self, difficulty: str, symbol, verbose=True):
        if verbose:
            print(f'Making move level "{difficulty}"')
        if difficulty == 'easy':
            self.make_easy_move(symbol)
        elif difficulty == 'medium':
            self.make_medium_move(symbol)
        elif difficulty == 'hard':
            self.make_hard_move(symbol)
        else:
            raise ValueError('Invalid difficulty of bot move!')

    def play_game(self, player_1, player_2):
        """This method can be used to play a single game given players and difficulties. It is to be used wrapped
        inside the run method."""
        allowed_bot_difficulties = {'easy', 'medium', 'hard'}
        if player_1 == 'user' and player_2 == 'user':
            mode = 'user_user'
        elif player_1 == 'user' and player_2 in allowed_bot_difficulties:
            mode = 'user_bot'
            bot_1_level = player_2
            bot_2_level = player_2
        elif player_1 in allowed_bot_difficulties and player_2 == 'user':
            mode = 'bot_user'
            bot_1_level = player_1
            bot_2_level = player_1
        elif player_1 in allowed_bot_difficulties and player_2 in allowed_bot_difficulties:
            mode = 'bot_bot'
            bot_1_level = player_1
            bot_2_level = player_2
        else:
            raise ValueError('Incorrect combination of player_1 and player_2')
        starting_cells = '_________'
        self.field.update_cells(starting_cells)
        turn_number = 0
        while True:
            self.show_game()
            if self.is_game_done(verbose=False):
                _ = self.is_game_done()  # Display end game message
                break
            if (mode == 'user_user' or mode == 'user_bot'
                    or mode == 'bot_user' and turn_number != 0):
                new_move = input('Enter the coordinates: ')
                if not self.is_move_valid(new_move):
                    continue
                new_x_coord = int(new_move[0])
                new_y_coord = int(new_move[-1])
                new_symbol = self.get_move_symbol()
                self.update_game_with_move(new_x_coord, new_y_coord, new_symbol)
                self.show_game()
                if self.is_game_done(verbose=False):
                    _ = self.is_game_done()  # Display end game message
                    break
            if mode != 'user_user':
                bot_symbol = self.get_move_symbol()
                if turn_number % 2 == 0:
                    current_difficulty = bot_1_level  # noqa
                else:
                    current_difficulty = bot_2_level  # noqa
                self.make_bot_move(difficulty=current_difficulty, symbol=bot_symbol)
            turn_number += 1

    def run(self):
        while True:
            command = input('Input command: ')
            commands = command.split()
            allowed_start_options = {'user', 'easy', 'medium', 'hard'}
            if command == 'exit':
                break
            elif (len(commands) == 3 and commands[0] == 'start' and commands[1] in allowed_start_options
                    and commands[2] in allowed_start_options):
                self.play_game(commands[1], commands[2])
            else:
                print('Bad parameters!')


def main():
    tic_tac_toe = Game()
    tic_tac_toe.run()


if __name__ == "__main__":
    main()
