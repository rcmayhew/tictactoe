import random
import math


class Piece:
    def __init__(self, char=' '):
        """
        Creates a Piece, default character is ' '
        :param char: the type of piece that will be played
        """
        self.piece = char

    @staticmethod
    def compare(piece1, piece2):
        """
        compares two Pieces
        :param piece1: the first Piece to be compared
        :param piece2: the second Piece to be compared
        :return: True if they are the same character
        """
        if piece1.character_type() == piece2.character_type():
            return True
        else:
            return False

    def character_type(self):
        return self.piece

    def not_null(self):
        if self.character_type() is not ' ':
            return True
        else:
            return False


class Board:
    def __init__(self):
        self.layout = [[Piece() for x in range(4)] for y in range(4)]

    def new_board(self):
        moves = self.convert_to_list()
        board = Board.copy(moves)
        return board

    def turn_count(self):
        moves = self.convert_to_list()
        return len(moves)

    @staticmethod
    def copy(moves):
        board = Board()
        for idx, move in enumerate(moves):
            loc = Game.convert_int(move)
            turn, piece = Game.determine_player(idx - 1)
            board.__play_piece__(loc, piece)
        return board

    @staticmethod
    def merge_list(xmoves, omoves):
        x = len(xmoves)
        o = len(omoves)
        moves = []
        if o > 0:
            for i in range(o):
                moves.append(xmoves[i])
                moves.append(omoves[i])
        if x > o:
            moves.append(xmoves[x - 1])
        return moves

    def convert_to_list(self):
        xmoves = []
        omoves = []
        for i in range(3):
            for j in range(3):
                element = self.layout[i][j]
                if element.character_type() == 'X':
                    xmoves.append(Game.convert_position((i, j)))
                if element.character_type() == 'O':
                    omoves.append(Game.convert_position((i, j)))
        return self.merge_list(xmoves, omoves)

    def __play_piece__(self, location, piece):
        x, y = location
        self.layout[x][y] = piece

    def __str__(self):
        return self.layout

    def clear(self):
        self.layout = [[Piece() for x in range(4)] for y in range(4)]

    def print_element(self, location):
        if not self.get_element(location).not_null():
            return Game.convert_position(location)
        else:
            return self.get_element(location)

    def print(self):
        print("\n")
        print("-------------")
        print("|", self.print_element((0, 0)), "|", self.print_element((1, 0)), "|", self.print_element((2, 0)), "|")
        print("-------------")
        print("|", self.print_element((0, 1)), "|", self.print_element((1, 1)), "|", self.print_element((2, 1)), "|")
        print("-------------")
        print("|", self.print_element((0, 2)), "|", self.print_element((1, 2)), "|", self.print_element((2, 2)), "|")
        print("-------------")

    def get_element(self, location):
        x, y = location
        return self.layout[x][y]

    def location_free(self, location):
        if self.get_element(location).not_null():
            return False
        else:
            return True

    def down(self, location):
        x, y = location
        mid = (x, y + 1)
        return mid, self.get_element(mid)

    def left(self, location):
        x, y = location
        mid = (x - 1, y)
        return mid, self.get_element(mid)

    def dial(self, location):
        x, y = location
        mid = (x - 1, y + 1)
        return mid, self.get_element(mid)

    def diar(self, location):
        x, y = location
        mid = (x + 1, y + 1)
        return mid, self.get_element(mid)

    def following(self, first, mid):
        x1, y1 = first
        x2, y2 = mid
        last = (2 * x2 - x1, 2 * y2 - y1)
        return next, self.get_element(last)

    def __down_check(self, location):
        if self.get_element(location).not_null():
            mid, piece1 = self.down(location)
            if Piece.compare(self.get_element(location), piece1):
                final, piece2 = self.down(mid)
                if Piece.compare(piece1, piece2):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def __left_check(self, location):
        if self.get_element(location).not_null():
            mid, piece1 = self.left(location)
            if Piece.compare(self.get_element(location), piece1):
                final, piece2 = self.left(mid)
                if Piece.compare(piece1, piece2):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def __dial_check(self, location):
        if self.get_element(location).not_null():
            mid, piece1 = self.dial(location)
            if Piece.compare(self.get_element(location), piece1):
                final, piece2 = self.dial(mid)
                if Piece.compare(piece1, piece2):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def __diar_check(self, location):
        if self.get_element(location).not_null():
            mid, piece1 = self.diar(location)
            if Piece.compare(self.get_element(location), piece1):
                final, piece2 = self.diar(mid)
                if Piece.compare(piece1, piece2):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    # points checked = [(0,0), (1,0), (2,0), (2,1), (2,2)]
    def check_win(self):
        if (self.__down_check((0, 0)) or self.__diar_check((0, 0)) or self.__down_check((1, 0)) or
                self.__down_check((2, 0)) or self.__left_check((2, 0)) or self.__dial_check((2, 0)) or
                self.__left_check((2, 1)) or self.__left_check((2, 2))):
            return True
        else:
            return False

    def down_axis(self):
        value = 0
        for i in range(3):
            orow = []
            xrow = []
            for j in range(3):
                if self.layout[i][j].character_type() == 'X':
                    xrow.append('X')
                elif self.layout[i][j].character_type() == 'O':
                    orow.append('O')
            value = value + self.axis_value(xrow, orow)
        return value

    def side_axis(self):
        value = 0
        for i in range(3):
            orow = []
            xrow = []
            for j in range(3):
                if self.layout[j][i].character_type() == 'X':
                    xrow.append('X')
                elif self.layout[j][i].character_type() == 'O':
                    orow.append('O')
            value = value + self.axis_value(xrow, orow)
        return value

    def dial_axis(self):
        value = 0
        orow = []
        xrow = []
        for i in range(3):
            if self.layout[i][i].character_type() == 'X':
                xrow.append('X')
            elif self.layout[i][i].character_type() == 'O':
                orow.append('O')
        value = value + self.axis_value(xrow, orow)
        return value

    def diar_axis(self):
        value = 0
        orow = []
        xrow = []
        for i in range(3):
            if self.layout[2 - i][i].character_type() == 'X':
                xrow.append('X')
            elif self.layout[2 - i][i].character_type() == 'O':
                orow.append('O')
        value = value + self.axis_value(xrow, orow)
        return value

    @staticmethod
    def axis_value(xrow, orow):
        x = len(xrow)
        o = len(orow)
        if x > 0 and o > 0:
            return 0
        maximum = (x, o)[o > x]
        if maximum == 0:
            return 0
        value = 3**maximum
        if maximum == o:
            value = -1 * value
        return value

    def value(self):
        return self.down_axis() + self.side_axis() + self.dial_axis() + self.diar_axis()


class Player:
    def __init__(self, piece='O', actual=True):
        self.char = Piece(piece)
        self.person = actual

    def play(self, board, location):
        board.__play_piece__(location, self.piece_type())

    def is_real(self):
        if self.person:
            return True
        else:
            return False

    def piece_type(self):
        return self.char

    def set_piece(self, piece):
        self.char = piece

    @staticmethod
    def pick_position(starting):
        """
        picks the best move by searching through the move set
        :param starting: the moves that have already happened before the AI's turn
        :return: the [1-9] position that is the best for the Ai
        """

        turn = starting.turn_count() + 1
        weight = Game.player_weight(turn)
        player = Player()
        char, piece = Game.determine_player(turn)
        player.set_piece(piece)
        bmove, bcost = 0, -100000000
        for num in range(1, 10):
            location = Game.convert_int(num)
            if starting.location_free(location):
                # search through each move
                board = starting.new_board()
                player.play(board, location)
                cost = board.value() * weight
                if cost > bcost:
                    # pick the move with the highest points
                    bmove = location
                    bcost = cost
            else:
                continue
        return bmove


class Game:
    def __init__(self):
        self.board = Board()
        self.player = [Player('X', actual=True), Player('O', actual=False)]
        self.turn = 0

    @staticmethod
    def choose_location(player, board, testing=False):
        # will add input options later
        if player.is_real():
            if not testing:
                hold = input("where do you want to place a piece?, 1-9  ")
                loc = Game.convert_int(int(hold))
            else:
                loc = (random.randint(0, 2), random.randint(0, 2))
            return loc
        else:
            if not testing:
                loc = player.pick_position(board)
                print("Computer's turn")
            else:
                loc = player.pick_position(board)
            return loc

    @staticmethod
    def convert_int(move):
        num = move - 1
        y = 2 - (num // 3)
        x = num % 3
        loc = (int(x), int(y))
        return loc

    @staticmethod
    def convert_position(pair):
        x, y = pair
        return (2 - y)*3 + x + 1

    @staticmethod
    def determine_player(turn):
        if turn % 2 == 0:
            return 0, Piece('O')
        else:
            return 1, Piece('X')

    @staticmethod
    def player_weight(turn):
        if turn % 2 == 0:
            return -1
        else:
            return 1

    @staticmethod
    def win_cost(turn):
        return -2*turn + 1

    def next_turn(self, testing, wins):
        self.turn = self.turn + 1
        play = self.turn % 2 - 1
        location = self.choose_location(self.player[play], self.board, testing)
        cont = self.board.location_free(location)

        while not cont:
            if not testing:
                print("There is a piece in that location already")
            location = self.choose_location(self.player[play], self.board, testing)
            cont = self.board.location_free(location)

        self.player[play].play(self.board, location)

        if not testing:
            self.board.print()
        if not testing:
            if self.board.check_win():
                print(self.player[play].piece_type(), "WINS!")
                wins.append(self.win_cost(play))
                return False

            if self.turn == 9:
                print("Its a tie!")
                wins.append(0)
                return False
        else:
            if self.board.check_win():
                if self.player[play].piece_type() == 'X':
                    print(self.player[play].piece_type(), "WINS!")
                wins.append(self.win_cost(play))
                return False

            if self.turn == 9:
                wins.append(0)
                return False
        return True

    def start_game(self, wins, testing=False):
        start = True

        while start:
            self.board.clear()
            self.turn = 0
            if not testing:
                self.board.print()

            keep_going = self.next_turn(testing, wins)

            while keep_going:
                keep_going = self.next_turn(testing, wins)

            if not testing:
                stay = input("keep playing? : y/n   ")
                if stay != 'y':
                    start = False
                else:
                    start = True
            else:
                start = False

        return
