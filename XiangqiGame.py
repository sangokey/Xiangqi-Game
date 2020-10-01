# Author: Sang Ok Suh
# Date: 03/03/2020
# Description: Writing a program that simulates the Xiangqi Game (Chinese Chess).


class XiangqiGame:

    """""
    XiangqiGame class initiates the board with appropriate piece type/color.
    Initiates game_state, turn, check status for each color.
    Contains get methods and set methods for data members.
    Contains make_move method that checks for valid moves and updates the board.
    """""

    def __init__(self):

        # Initiate actual board
        self._board = [[Chariot("red"), Horse("red"), Elephant("red"),
                        Advisor("red"), General("red"), Advisor("red"),
                        Elephant("red"), Horse("red"), Chariot("red")],
                       [None, None, None, None, None, None, None, None, None],
                       [None, Cannon("red"), None, None, None, None, None, Cannon("red"), None],
                       [Soldier("red"), None, Soldier("red"), None,
                        Soldier("red"), None, Soldier("red"), None, Soldier("red")],
                       [None, None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None, gam1None],
                       [Soldier("black"), None, Soldier("black"), None,
                        Soldier("black"), None, Soldier("black"), None, Soldier("black")],
                       [None, Cannon("black"), None, None, None, None, None, Cannon("black"), None],
                       [None, None, None, None, None, None, None, None, None],
                       [Chariot("black"), Horse("black"), Elephant("black"), Advisor("black"),
                        General("black"), Advisor("black"), Elephant("black"), Horse("black"),
                        Chariot("black")]]

        # Initiate Initial Game State = UNFINISHED
        self._game_state = "UNFINISHED"

        # Initiate first turn = Red
        self._turn = "red"

        # Initiate Check Status
        self._red_check = False
        self._black_check = False

    # Get Methods for Data Members
    def get_turn(self):
        return self._turn

    def get_game_state(self):
        return self._game_state

    def get_piece(self, row, col):
        return self._board[row][col]

    def get_opponent_check(self):
        if self._turn == "red":
            return self._black_check
        elif self._turn == "black":
            return self._red_check

    # Set Methods for Data Members

    def update_board(self, row, col, item):
        self._board[row][col] = item

    def set_turn(self):
        if self._turn == "red":
            self._turn = "black"
        elif self._turn == "black":
            self._turn = "red"

    def set_win(self):
        if self._turn == "red":
            self._game_state = "RED_WON"
        elif self._turn == "black":
            self._game_state = "BLACK_WON"

    def set_check(self):
        if self._turn == "red":
            self._black_check = True
        elif self._turn == "black":
            self._red_check = True

    def remove_check(self):
        if self._turn == "red":
            self._black_check = False
        elif self._turn == "black":
            self._red_check = False

    # Checking Check Status
    def is_in_check(self, color):
        if color == "red":
            return self._red_check
        elif color == "black":
            return self._black_check
        else:
            return False

    # Make Move Method
    def make_move(self, start, end):

        # List for column letters for indexing
        column_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

        """Start Evaluation"""

        # Get Row Coordinate of Start
        if len(start) == 2:
            start_row = int(start[1]) - 1
        elif len(start) == 3:
            if start[1] == '1' and start[2] == '0':
                start_row = 9
            else:
                return False

        # Get Column Coordinate of start
        if start[0] in column_list:
            start_col = column_list.index(start[0])
        else:
            return False

        # Get the piece of start
        current_piece = self.get_piece(start_row, start_col)

        # If current piece is none return False
        if current_piece is None:
            return False

        # Get the color of current piece
        current_piece_color = current_piece.get_piece_color()

        # Get current turn
        current_turn = self.get_turn()

        # Check for invalid moves
        # If current piece is not same color as turn color return False
        if current_turn != current_piece_color:
            return False
        # If game has already been won return False
        elif self.get_game_state() != "UNFINISHED":
            return False

        """End Evaluation"""

        # Get Row Coordinate of End
        if len(end) == 2:
            end_row = int(end[1]) - 1
        elif len(end) == 3:
            if end[1] == '1' and end[2] == '0':
                end_row = 9
            else:
                return False

        # Get Column Coordinate of End
        if end[0] in column_list:
            end_col = column_list.index(end[0])
        else:
            return False

        # Get the piece of end
        end_piece = self.get_piece(end_row, end_col)

        # Get the color of current piece
        if end_piece is not None:
            end_piece_color = end_piece.get_piece_color()
            if end_piece_color == current_piece_color:
                return False

        # Check if current location and end location is same
        if current_piece == end_piece:
            return False

        # Check if valid move according to piece type move conditions
        if current_piece.check_valid_move(start_row, start_col, end_row, end_col, self._board) is True \
                and (end_piece is None or end_piece.get_piece_type() != "General"):

            # Update Board - End Position
            self.update_board(end_row, end_col, current_piece)

            # Update Board - Start Position
            self.update_board(start_row, start_col, None)

            # Loop through the board to find location of other colors general:
            for i in range(0, 10):
                for j in range(0, 9):
                    if self._board[i][j] is not None and self._board[i][j].get_piece_type() == "General" \
                            and self._board[i][j].get_piece_color() != current_turn:
                        opponent_general_row = i
                        opponent_general_col = j

            # Loop through the board to find location of current colors general:
            for i in range(0, 10):
                for j in range(0, 9):
                    if self._board[i][j] is not None and self._board[i][j].get_piece_type() == "General" \
                            and self._board[i][j].get_piece_color() == current_turn:
                        current_general_row = i
                        current_general_col = j

            # Check for "flying general" situation, return test_board and return False
            if opponent_general_col == current_general_col:

                block = 0

                if current_turn == "red":
                    for i in range(current_general_row + 1, opponent_general_row):
                        if self._board[i][opponent_general_col] is not None:
                            block += 1

                elif current_turn == "black":
                    for i in range(opponent_general_row + 1, current_general_row):
                        if self._board[i][opponent_general_col] is not None:
                            block += 1

                # If no blocking piece return False and return to previous positions
                if block == 0:

                    # Revert End Position Piece
                    self.update_board(end_row, end_col, end_piece)

                    # Revert Start Position Piece
                    self.update_board(start_row, start_col, current_piece)

                    # Return False
                    return False

            # Current General Check Counter
            current_general_check = 0

            # Loop through board
            for i in range(0, 10):
                for j in range(0, 9):

                    # Check if valid move according condition:
                    # Own general is checked after move (opponent has a valid move that can capture general)

                    # Check if other opponents have valid move to current color general
                    if self._board[i][j] is not None and \
                            self._board[i][j].get_piece_color() != current_turn and \
                            self._board[i][j].check_valid_move(i, j, current_general_row,
                                                               current_general_col, self._board) is True:

                        # Increment general check counter
                        current_general_check += 1

            # If opponent has at least 1 move to take current general next turn
            if current_general_check >= 1:

                #Return False and revert

                # Revert End Position Piece
                self.update_board(end_row, end_col, end_piece)

                # Revert Start Position Piece
                self.update_board(start_row, start_col, current_piece)

                return False

            # Now check for check

            # Initiate possible check moves = 0
            check_possible = 0

            # Loop through board
            for i in range(0, 10):
                for j in range(0, 9):

                    # Check if current color pieces can take opponent general on next turn
                    if self._board[i][j] is not None and \
                            self._board[i][j].get_piece_color() == current_turn and \
                            self._board[i][j].check_valid_move(i, j, opponent_general_row, opponent_general_col,
                                                               self._board) is True:
                        # Add 1 to check_possible if move found
                        check_possible += 1

            # If no check move is found, set opposite color check status to False
            if check_possible == 0:
                self.remove_check()

            # If check move is found, set opposite color check status to True
            else:
                self.set_check()

            # Initiate Block Possible for Winning Algorithm
            opponent_block = 0

            # Loop through board
            # Find each opponent piece
            for i in range(0, 10):
                for j in range(0, 9):

                    new_current = self._board[i][j]

                    # Check for all the moves the piece can make
                    for x in range(0, 10):
                        for y in range(0, 9):

                            new_end = self._board[x][y]

                            # If an opponent piece is found, check if it can move to the location
                            if new_current is not None \
                                    and new_current.get_piece_color() != current_turn \
                                    and new_current.check_valid_move(i, j, x, y, self._board) is True:

                                # Update Board - End Position
                                self.update_board(x, y, new_current)

                                # Update Board - Start Position
                                self.update_board(i, j, None)

                                # Check if the opponent general cannot be eaten

                                # Loop through the board to find location of opponent general:
                                for a in range(0, 10):
                                    for b in range(0, 9):
                                        if self._board[a][b] is not None \
                                                and self._board[a][b].get_piece_type() == "General" \
                                                and self._board[a][b].get_piece_color() != current_turn:
                                            opponent_general_row = a
                                            opponent_general_col = b

                                # Loop through the board to find location of current color pieces
                                for c in range(0, 10):
                                    for d in range(0, 9):

                                        # and check if there is no valid moves to opponent general
                                        if self._board[c][d] is not None \
                                                and self._board[c][d].get_piece_color() == current_turn and \
                                                self._board[c][d].check_valid_move(c, d, opponent_general_row,
                                                                                        opponent_general_col,
                                                                                        self._board) is False:

                                            # If there is at least one invalid move, increment block_possible
                                            opponent_block += 1

                                            # Revert for next iteration
                                            self.update_board(x, y, new_end)
                                            self.update_board(i, j, new_current)

                                        else:
                                            # Revert for next iteration
                                            self.update_board(x, y, new_end)
                                            self.update_board(i, j, new_current)

            # If no block possible, current color wins - checkmate/stalemate
            if opponent_block == 0:
                self.set_win()

            # Update next turn
            self.set_turn()

            # Return True
            return True

        else:
            return False


class Piece:

    """""
    Piece class that is the parent class of other types.
    Takes color as parameter.
    """""

    def __init__(self, piece_color):
        self._piece_color = piece_color

    def get_piece_color(self):
        return self._piece_color


class General(Piece):

    """""
    General class that inherits from Piece class.
    Sets piece type and has own valid move checker.
    Confined to palace.
    Can move 1 point orthogonally.
    """""

    def __init__(self, piece_color):
        super().__init__(piece_color)
        self._piece_type = "General"

    def get_piece_type(self):
        return self._piece_type

    def check_valid_move(self, start_row, start_col, end_row, end_col, board):

        if self.get_piece_color() == "red":

            # Blacks Confined Palace
            if (end_row == 0 and (end_col == 3 or end_col == 4 or end_col == 5)) \
                    or (end_row == 1 and (end_col == 3 or end_col == 4 or end_col == 5)) \
                    or (end_row == 2 and (end_col == 3 or end_col == 4 or end_col == 5)):

                # Check for 1 Orthogonal Move
                if ((start_row == end_row) and abs(start_col - end_col) == 1) or \
                        (abs(start_row - end_row) == 1 and (start_col == end_col)):
                    return True

                else:
                    return False

        elif self.get_piece_color() == "black":

            # Red Confined Palace
            if (end_row == 9 and (end_col == 3 or end_col == 4 or end_col == 5)) \
                    or (end_row == 8 and (end_col == 3 or end_col == 4 or end_col == 5)) \
                    or (end_row == 7 and (end_col == 3 or end_col == 4 or end_col == 5)):

                # Check for 1 Orthogonal Move
                if ((start_row == end_row) and abs(start_col - end_col) == 1) or \
                        (abs(start_row - end_row) == 1 and (start_col == end_col)):
                    return True


class Advisor(Piece):

    """""
    Advisor class that inherits from Piece class.
    Sets piece type and has own valid move checker.
    Confined to palace.
    Can only move one point diagonally - one point vertical & one point horizontal.
    """""

    def __init__(self, piece_color):
        super().__init__(piece_color)
        self._piece_type = "Advisor"

    def get_piece_type(self):
        return self._piece_type

    def check_valid_move(self, start_row, start_col, end_row, end_col, board):

        # Black's confined Palace
        if self.get_piece_color() == "red":
            if (end_row == 0 and end_col == 3) or (end_row == 0 and end_col == 5) or (end_row == 1 and end_col == 4) \
                    or (end_row == 2 and end_col == 3) or (end_row == 2 and end_col == 5):

                # Check for 1 diagonal move
                if abs(end_row - start_row) == 1 and abs(end_col - start_col) == 1:
                    return True
            else:
                return False

        # Red's confined Palace
        elif self.get_piece_color() == "black":
            if (end_row == 9 and end_col == 3) or (end_row == 9 and end_col == 5) or (end_row == 8 and end_col == 4) \
                    or (end_row == 7 and end_col == 3) or (end_row == 7 and end_col == 5):

                # Check for 1 diagonal move
                if abs(end_row - start_row) == 1 and abs(end_col - start_col) == 1:
                    return True
            else:
                return False


class Elephant(Piece):

    """""
    Elephant class that inherits from Piece class.
    Sets piece type and has own valid move checker.
    Cannot cross river.
    Can only move two points vertically + two points horizontally (2 points diagonally).
    Check for blocking pieces.
    """""

    def __init__(self, piece_color):
        super().__init__(piece_color)
        self._piece_type = "Elephant"

    def get_piece_type(self):
        return self._piece_type

    def check_valid_move(self, start_row, start_col, end_row, end_col, board):

        # Black cannot cross river (row > 5)
        if self.get_piece_color() == "red":

            # If end_row is past the river then false
            if end_row > 4:
                return False

        # Red cannot cross river (row < 6)
        elif self.get_piece_color() == "black":

            if end_row < 5:
                return False

        # Check for SE move
        if (end_row - start_row == 2) and (end_col - start_col == 2):

            # Check for diagonally blocking piece
            if board[end_row - 1][end_col - 1] is not None:
                return False
            else:
                return True

        # Check for SW move
        elif (end_row - start_row == 2) and (start_col - end_col == 2):

            # Check for diagonally blocking piece
            if board[end_row - 1][start_col - 1] is not None:
                return False
            else:
                return True

        # Check for NW move
        elif (start_row - end_row == 2) and (start_col - end_col == 2):

            # Check for diagonally blocking piece
            if board[start_row - 1][start_col - 1] is not None:
                return False
            else:
                return True

        # Check for NE move
        elif (start_row - end_row == 2) and (end_col - start_col == 2):

            # Check for diagonally blocking space
            if board[start_row - 1][end_col - 1] is not None:
                return False
            else:
                return True

        else:
            return False


class Horse(Piece):

    """""
    Horse class that inherits from Piece class.
    Sets piece type and has own valid move checker.
    Can move 2 in vertical/horizontal & 1 in horizontal/vertical (opposite directions)
    Checks for any blocking pieces.
    """""

    def __init__(self, piece_color):
        super().__init__(piece_color)
        self._piece_type = "Horse"

    def get_piece_type(self):
        return self._piece_type

    def check_valid_move(self, start_row, start_col, end_row, end_col, board):

        # Check for positive vertical move (2 up position and 1 left/right)
        if (start_row - end_row == 2) and (start_col - end_col == 1 or start_col - end_col == -1):
            if board[start_row - 1][start_col] is not None:
                return False
            else:
                return True

        # Check for negative vertical move (2 down position and 1 left/right)
        elif (start_row - end_row == -2) and (start_col - end_col == 1 or start_col - end_col == -1):
            if board[start_row + 1][start_col] is not None:
                return False
            else:
                return True

        # Check for negative horizontal move (2 left position and 1 top/bottom)
        elif (start_col - end_col == 2) and (start_row - end_row == 1 or start_row - end_row == -1):
            if board[start_row][start_col - 1] is not None:
                return False
            else:
                return True

        # Check for positive horizontal move (2 right of position and 1 top/bottom)
        elif (start_col - end_col == -2) and (start_row - end_row == 1 or start_row - end_row == -1):
            if board[start_row][start_col + 1] is not None:
                return False
            else:
                return True

        # If none of the valid moves, then return False
        else:
            return False


class Chariot(Piece):

    """""
    Chariot class that inherits from Piece class.
    Sets piece type and has own valid move checker.
    Any move points orthogonally, but make sure there is no piece in way from start to end.
    """""

    def __init__(self, piece_color):
        super().__init__(piece_color)
        self._piece_type = "Chariot"

    def get_piece_type(self):
        return self._piece_type

    def check_valid_move(self, start_row, start_col, end_row, end_col, board):

        pieces_way = 0

        # Horizontal Move (positive direction)
        if start_row == end_row and start_col < end_col:
            for i in range(start_col + 1, end_col):
                if board[start_row][i] is not None:
                    pieces_way += 1

        # Horizontal Move (negative direction)
        elif start_row == end_row and start_col > end_col:
            for i in range(end_col + 1, start_col):
                if board[start_row][i] is not None:
                    pieces_way += 1

        # Vertical Move (positive direction)
        elif start_col == end_col and start_row < end_row:
            for i in range(start_row + 1, end_row):
                if board[i][start_col] is not None:
                    pieces_way += 1

        # Vertical Move (negative direction)
        elif start_col == end_col and start_row > end_row:
            for i in range(end_row + 1, start_row):
                if board[i][start_col] is not None:
                    pieces_way += 1

        else:
            return False

        if pieces_way == 0:
            return True
        else:
            return False


class Cannon(Piece):

    """""
    Cannon class that inherits from Piece class.
    Sets piece type and has own valid move checker.
    Checks for pieces in the way of start and end.
    If the end position is empty, make sure no pieces in way.
    If the end position is not empty, make sure 1 piece in way.
    Moves: as many points as it wants
    """""

    def __init__(self, piece_color):
        super().__init__(piece_color)
        self._piece_type = "Cannon"

    def get_piece_type(self):
        return self._piece_type

    def check_valid_move(self, start_row, start_col, end_row, end_col, board):

        pieces_way = 0

        # Horizontal Move (positive direction)
        if start_row == end_row and start_col < end_col:
            for i in range(start_col + 1, end_col):
                if board[start_row][i] is not None:
                    pieces_way += 1

        # Horizontal Move (negative direction)
        elif start_row == end_row and start_col > end_col:
            for i in range(end_col + 1, start_col):
                if board[start_row][i] is not None:
                    pieces_way += 1

        # Vertical Move (positive direction)
        elif start_col == end_col and start_row < end_row:
            for i in range(start_row + 1, end_row):
                if board[i][start_col] is not None:
                    pieces_way += 1

        # Vertical Move (negative direction)
        elif start_col == end_col and start_row > end_row:
            for i in range(end_row + 1, start_row):
                if board[i][start_col] is not None:
                    pieces_way += 1

        # If the end position is empty, check if there is anything in between
        if board[end_row][end_col] is None:

            if pieces_way == 0:
                return True
            else:
                return False

        # If the end position is not empty, check if there is anything in between
        elif board[end_row][end_col] is not None:

            if pieces_way == 1:
                return True
            else:
                return False


class Soldier(Piece):

    """""
    Solider class that inherits from Piece class.
    Sets piece type and has own valid move checker.
    If before the river, only forward moves.
    If after the river, only forward moves or any horizontal moves.
    Moves: 1 point
    """""

    def __init__(self, piece_color):
        super().__init__(piece_color)
        self._piece_type = "Solider"

    def get_piece_type(self):
        return self._piece_type

    def check_valid_move(self, start_row, start_col, end_row, end_col, board):

        """Checks if move is valid"""

        row_change = end_row - start_row
        col_change = end_col - start_col

        # Black
        if self.get_piece_color() == "red":

            # If before the river, check only for row change
            if start_row < 5:

                # Only forward, no horizontal
                if row_change == 1 and col_change == 0:
                    return True
                else:
                    return False

            # If after the river, check for row and col change
            elif start_row >= 5:
                if (row_change == 1 and col_change == 0) or (row_change == 0 and (col_change == 1 or col_change == -1)):
                    return True
                else:
                    return False

        # Red
        elif self.get_piece_color() == "black":

            # If before the river, check only for row change
            if start_row > 4:

                # Only forward, no horizontal
                if row_change == -1 and col_change == 0:
                    return True
                else:
                    return False

            # If after the river, check for row and col change
            elif start_row <= 4:
                if (row_change == -1 and col_change == 0) or (
                        row_change == 0 and (col_change == 1 or col_change == -1)):
                    return True
                else:
                    return False
