import random
import math


class Piece:
    def __init__(self, char=' '):
        self.piece = char

    def __str__(self):
        return self.character_type()

    @staticmethod
    def compare(piece1, piece2):
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

    @staticmethod
    def copy(moves):
        board = Board()
        for idx, move in enumerate(moves):
            loc = Game.convert_int(move)
            turn, piece = Game.determine_player(idx)
            board.__play_piece__(loc, piece)
        return board

    def convert_to_list(self):
        moves = []
        for i, row in enumerate(self.layout):
            for j, element in enumerate(row):
                if element == 'X' or element == 'O':
                    moves.append(Game.convert_position((i, j)))
        return moves

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

    @staticmethod
    def pick_position(starting):
        """
        picks the best move by searching through the move set
        :param starting: the moves that have already happened before the AI's turn
        :return: the [1-9] position that is the best for the Ai
        """
        turn = len(starting) + 1
        weight = Game.player_weight(turn)
        bmove, bcost = 0, -100000000
        for num in range(10):
            if num not in starting:
                # search through each move
                move = list(starting)
                move.append(num)
                cost = Player.search(move) * weight
                if cost > bcost:
                    # pick the move with the highest points
                    bmove = num
            else:
                continue
        return bmove

    @staticmethod
    def search(moves):
        """
        checks each move and returns a value that is a weighted win ratio.
        Assumes that there is a move in the moves list
        :param moves: the moves that have already been done or test. It is also the list of moves to not test.
        :return: the "weight" of winning form the current position. Positive is victory to 'X'
        """
        # will do a complete depth first search
        # will recurse
        # start with board - but not actaully board. will hand around a list instead
        cost = 0
        for num in range(10):
            #  moves are 1-9
            # add a move to the board and search down the list
            if num not in moves:
                move = list(moves)
                move.append(num)
                board = Board.copy(move)
                turn = len(moves)
                if board.check_win():
                    cost = cost + Game.win_cost(turn) * math.factorial(10 - turn)
                else:
                    cost = cost + Player.search(move)
                del board
                if turn >= 9:
                    return 0
            else:
                continue
        return cost


class Game:
    def __init__(self):
        self.board = Board()
        self.player = [Player('X', actual=False), Player('O')]
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
            position = player.pick_position(board.convert_to_list())
            loc = Game.convert_int(position)
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
            return 0, Piece('X')
        else:
            return 1, Piece('O')

    @staticmethod
    def player_weight(turn):
        if turn % 2 == 0:
            return 1
        else:
            return -1

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

        if self.board.check_win():
            print(self.player[play].piece_type(), "WINS!")
            wins.append(self.win_cost(play))
            return False

        if self.turn == 9:
            print("Its a tie!")
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
