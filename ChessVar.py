# Author: Brenden Covington
# GitHub username: covingtb
# Date: 8/15/2023
# Description: Chess Variation game where each player starts on the same side of the board with a king, a rook,
# 2 knights, and 2 bishops. As in standard chess, white moves first. The first player to move their king onto row 8 is
# the winner, unless it's a tie on the same round. Pieces move and capture the same as in standard chess. Also, a player
# is not allowed to expose their own king to check (including moving a piece that was blocking a check such that it no
# longer does). A player is not allowed to put the opponent's king in check.

class ChessVar:
    """Class that initiates a chess game and begins by setting a board and variables for tracking important
     information"""

    rankstoRows = {'1': 7, '2': 6, '3': 5, '4': 4,
                   '5': 3, '6': 2, '7': 1, '8': 0}
    rowstoRanks = {v: k for k, v in rankstoRows.items()}
    filestoCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colstoFiles = {v: k for k, v in filestoCols.items()}
    wKingLoc = 'a1'
    bKingLoc = 'h1'
    lastTo = ['a1']

    def __init__(self):
        self._board = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['R', 'B', 'N', ' ', ' ', 'n', 'b', 'r'],
            ['K', 'B', 'N', ' ', ' ', 'n', 'b', 'k']
        ]
        self._squares = (
            'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
            'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',
            'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8',
            'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8',
            'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
            'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'
        )
        self._game_state = 'UNFINISHED'
        self._near_win = False
        self._turn = 'white'

    def get_game_state(self):
        """Returns state of game"""
        return self._game_state

    def get_col(self, coord):
        """Returns column of piece square"""
        return self.filestoCols[coord[0]]

    def get_row(self, coord):
        """Returns row of piece square"""
        return self.rankstoRows[coord[1]]

    def king_legal(self, orig, dest):
        """Outlines what squares are within king's valid movement"""
        if (abs(ord(dest[0]) - ord(orig[0])) <= 1) and (abs(ord(dest[1]) - ord(orig[1])) <= 1):
            return True

    def rook_legal(self, orig, dest):
        """Defines what squares are within rook's valid movements"""
        if (abs(ord(dest[0]) - ord(orig[0])) == 0) and (abs(ord(dest[1]) - ord(orig[1])) != 0):
            orig_row = self.get_row(orig)
            dest_row = self.get_row(dest)
            column = self.get_col(orig)
            rows = int(orig_row) - int(dest_row)
            if rows > 0:
                for i in range(rows):
                    if self._board[i][column] != ' ':
                        return False
                else:
                    return True
        if (abs(ord(dest[0]) - ord(orig[0])) != 0) and (abs(ord(dest[1]) - ord(orig[1])) == 0):
            row = self.get_row(orig)
            orig_col = self.get_col(orig)
            dest_col = self.get_col(dest)
            for square in self._board[row][orig_col + 1:dest_col - 1]:
                pieces = 0
                if square != ' ':
                    pieces += 1
                    if pieces > 2:
                        return False

    def bishop_legal(self, orig, dest):
        """Outlines what bishop moves are possible"""

        def is_valid_position(x, y):
            """Keeps movement on board"""
            return 0 <= x < 8 and 0 <= y < 8

        start_x = self.get_col(orig)
        start_y = self.get_row(dest)
        moves = []

        # Diagonal movement directions (4 possible diagonals)
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            x, y = start_x + dx, start_y + dy
            while is_valid_position(x, y):
                moves.append((x, y))
                x, y = x + dx, y + dy

        if ((self._board[8 - int(dest[1])]), (self._board[ord(dest[0]) - ord('a')])) in moves:
            return True

    def knight_legal(self, orig, dest):
        """Outlines what knight moves are possible"""
        if (abs(ord(dest[0]) - ord(orig[0])) == 1) or (abs(ord(dest[1]) - ord(orig[1])) == 1):
            if (abs(ord(dest[0]) - ord(orig[0])) == 2) or (abs(ord(dest[1]) - ord(orig[1])) == 2):
                return True

    def wcheck_checker(self):
        """Checks if white king is in check"""
        kingpos = self.wKingLoc
        kingsafe = True
        for row in self._board:
            for square in row:
                if square != 'K' and square != ' ':
                    if square == 'k':
                        if self.king_legal(self.lastTo[0], kingpos):
                            kingsafe = False
                            return kingsafe
                    elif square == 'r':
                        if self.rook_legal(self.lastTo[0], kingpos):
                            kingsafe = False
                            return kingsafe
                    elif square == 'b':
                        if self.bishop_legal(self.lastTo[0], kingpos):
                            kingsafe = False
                            return kingsafe
                    elif square == 'n':
                        if self.knight_legal(self.lastTo[0], kingpos):
                            kingsafe = False
                            return kingsafe

    def bcheck_checker(self):
        """Checks if black king is in check"""
        kingpos = self.bKingLoc
        kingsafe = True
        for row in self._board:
            for square in row:
                if square != 'k' and square != ' ':
                    if square == 'K':
                        if self.king_legal(self.lastTo[0], kingpos):
                            kingsafe = False
                            return kingsafe
                    elif square == 'R':
                        if self.rook_legal(self.lastTo[0], kingpos):
                            kingsafe = False
                            return kingsafe
                    elif square == 'B':
                        if self.bishop_legal(self.lastTo[0], kingpos):
                            kingsafe = False
                            return kingsafe
                    elif square == 'N':
                        if self.knight_legal(self.lastTo[0], kingpos):
                            kingsafe = False
                            return kingsafe

    def make_move(self, fromsq, tosq):
        """Determines if player is black or white and then decides if the move is valid through a
        series of validations"""
        if self._game_state == 'UNFINISHED':
            if self._turn == 'white':
                if fromsq in self._squares:
                    if tosq in self._squares:
                        if fromsq != tosq:
                            piece = self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')]
                            if piece.isupper():
                                self.lastTo[0] = tosq

                                if piece == 'K':
                                    if self.king_legal(fromsq, tosq):
                                        destination = self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')]
                                        if destination == ' ':
                                            if self.wcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            if self.bcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                            self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'K'
                                            self.wKingLoc = tosq
                                            if 'K' in self._board[0]:
                                                self._near_win = True
                                                self._turn = 'black'
                                                return True
                                            else:
                                                self._turn = 'black'
                                                return True
                                        elif destination != ' ':
                                            if destination.isupper():
                                                print("Invalid Move: Can't move piece onto another of your pieces.")
                                                return False
                                            else:
                                                if self.wcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                if self.bcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                                self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'K'
                                                self.wKingLoc = tosq
                                                if 'K' in self._board[0]:
                                                    self._near_win = True
                                                    self._turn = 'black'
                                                    return True
                                                else:
                                                    self._turn = 'black'
                                                    return True
                                    else:
                                        print("Invalid Move: King can't move there.")
                                        return False

                                elif piece == 'R':
                                    if self.rook_legal(fromsq, tosq):
                                        destination = self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')]
                                        if destination == ' ':
                                            if self.wcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            if self.bcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                            self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'R'
                                            self._turn = 'black'
                                            return True
                                        elif destination == 'k':
                                            print('Invalid Movement: Cannot Take King.')
                                            return False
                                        elif destination != ' ':
                                            if destination.isupper():
                                                print("Invalid Move: Can't move piece onto another of your pieces.")
                                                return False
                                            else:
                                                if self.wcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                if self.bcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                                self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'R'
                                                self._turn = 'black'
                                                return True
                                    else:
                                        print("Invalid Move: Rook can't move there.")
                                        return False

                                elif piece == 'B':
                                    if self.bishop_legal(fromsq, tosq):
                                        destination = self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')]
                                        if destination == ' ':
                                            if self.wcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            if self.bcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                            self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'B'
                                            self._turn = 'black'
                                            return True
                                        elif destination == 'k':
                                            print('Invalid Movement: Cannot Take King.')
                                            return False
                                        elif destination != ' ':
                                            if destination.isupper():
                                                print("Invalid Move: Can't move piece onto another of your pieces.")
                                                return False
                                            else:
                                                if self.wcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                if self.bcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                                self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'B'
                                                self._turn = 'black'
                                                return True
                                    else:
                                        print("Invalid Move: Bishop can't move there.")
                                        return False

                                elif piece == 'N':
                                    if self.knight_legal(fromsq, tosq):
                                        destination = self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')]
                                        if destination == ' ':
                                            if self.wcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            if self.bcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                            self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'N'
                                            self._turn = 'black'
                                            return True
                                        elif destination == 'k':
                                            print('Invalid Movement: Cannot Take King.')
                                            return False
                                        elif destination != ' ':
                                            if destination.isupper():
                                                print("Invalid Move: Can't move piece onto another of your pieces.")
                                                return False
                                            else:
                                                if self.wcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                if self.bcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                                self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'N'
                                                self._turn = 'black'
                                                return True
                                    else:
                                        print("Invalid Move: Knight can't move there.")
                                        return False


                            else:
                                print("Invalid Move: Can't move other player's piece.")
                                return False
                        else:
                            print("Invalid Move: Origin and destination can't be the same")
                            return False
                    else:
                        print('Invalid Move: Destination not on board.')
                        return False
                else:
                    print('Invalid Move: Origin not on board.')
                    return False
            else:
                print('Invalid Move: Not your piece.')
                return False


            if self._turn == 'black':
                if fromsq in self._squares:
                    if tosq in self._squares:
                        if fromsq != tosq:
                            piece = self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')]
                            if piece.islower():
                                self.lastTo[0] = tosq

                                if piece == 'k':
                                    if self.king_legal(fromsq, tosq):
                                        destination = self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')]
                                        if destination == ' ':
                                            if self.bcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            if self.wcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                            self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'k'
                                            self.bKingLoc = tosq
                                            if 'k' in self._board[0]:
                                                if self._near_win is True:
                                                    self._game_state = 'TIE'
                                                    return True
                                                else:
                                                    self._game_state = 'BLACK WINS'
                                                    return True
                                            else:
                                                self._turn = 'white'
                                                return True
                                        elif destination != ' ':
                                            if destination.islower():
                                                print("Invalid Move: Can't move piece onto another of your pieces.")
                                                return False
                                            else:
                                                if self.bcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                if self.wcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                                self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'k'
                                                self.bKingLoc = tosq
                                                if 'k' in self._board[0]:
                                                    if self._near_win is True:
                                                        self._game_state = 'TIE'
                                                        return True
                                                    else:
                                                        self._game_state = 'BLACK WINS'
                                                        return True
                                                else:
                                                    self._turn = 'white'
                                                    return True
                                    else:
                                        print("Invalid Move: King can't move there.")
                                        return False

                                elif piece == 'r':
                                    if self.rook_legal(fromsq, tosq):
                                        destination = self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')]
                                        if destination == ' ':
                                            if self.bcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            if self.wcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                            self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'r'
                                            self._turn = 'white'
                                            return True
                                        elif destination == 'K':
                                            print('Invalid Movement: Cannot Take King.')
                                            return False
                                        elif destination != ' ':
                                            if destination.islower():
                                                print("Invalid Move: Can't move piece onto another of your pieces.")
                                                return False
                                            else:
                                                if self.bcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                if self.wcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                                self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'r'
                                                self._turn = 'white'
                                                return True
                                    else:
                                        print("Invalid Move: Rook can't move there.")
                                        return False

                                elif piece == 'b':
                                    if self.bishop_legal(fromsq, tosq):
                                        destination = self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')]
                                        if destination == ' ':
                                            if self.bcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            if self.wcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                            self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'b'
                                            self._turn = 'white'
                                            return True
                                        elif destination == 'K':
                                            print('Invalid Movement: Cannot Take King.')
                                            return False
                                        elif destination != ' ':
                                            if destination.islower():
                                                print("Invalid Move: Can't move piece onto another of your pieces.")
                                                return False
                                            else:
                                                if self.bcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                if self.wcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                                self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'b'
                                                self._turn = 'white'
                                                return True
                                    else:
                                        print("Invalid Move: Bishop can't move there.")
                                        return False

                                elif piece == 'n':
                                    if self.knight_legal(fromsq, tosq):
                                        destination = self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')]
                                        if destination == ' ':
                                            if self.bcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            if self.wcheck_checker():
                                                print("Invalid Move: King can't be in check.")
                                                return False
                                            self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                            self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'n'
                                            self._turn = 'white'
                                            return True
                                        elif destination == 'K':
                                            print('Invalid Movement: Cannot Take King.')
                                            return False
                                        elif destination != ' ':
                                            if destination.islower():
                                                print("Invalid Move: Can't move piece onto another of your pieces.")
                                                return False
                                            else:
                                                if self.bcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                if self.wcheck_checker():
                                                    print("Invalid Move: King can't be in check.")
                                                    return False
                                                self._board[8 - int(fromsq[1])][ord(fromsq[0]) - ord('a')] = ' '
                                                self._board[8 - int(tosq[1])][ord(tosq[0]) - ord('a')] = 'n'
                                                self._turn = 'white'
                                                return True

                            else:
                                print("Invalid Move: Can't move other player's piece.")
                                return False
                        else:
                            print("Invalid Move: Origin and destination can't be the same")
                            return False
                    else:
                        print('Invalid Move: Destination not on board.')
                        return False
                else:
                    print('Invalid Move: Origin not on board.')
                    return False
            else:
                print('Invalid Move: Not your piece.')
                return False
        else:
            print('Invalid Move: Game is Over.')
            return False
