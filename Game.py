import random
import string


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

    def __play_piece__(self, location, piece):
        x, y = location
        self.layout[x][y] = piece

    def __str__(self):
        return self.layout

    def clear(self):
        self.layout = [[Piece() for x in range(4)] for y in range(4)]

    def print_element(self, location):
        if not self.get_element(location).not_null():
            x, y = location
            return (2 - y)*3 + x + 1
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
        next = (2 * x2 - x1, 2 * y2 - y1)
        return next, self.get_element(next)

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
    def __init__(self, piece='o', actual=True):
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


class Game:
    def __init__(self):
        self.board = Board()
        self.player = [Player('X'), Player('O')]
        self.turn = 0

    @staticmethod
    def choose_location(player, testing):
        # will add input options later
        if not testing:
            hold = input("where do you want to place a piece?, 1-9  ")
            num = int(hold) - 1
            y = 2 - (num // 3)
            x = num % 3
            loc = (int(x), int(y))
        else:
            loc = (random.randint(0, 2), random.randint(0, 2))
        if player.is_real():
            return loc
        else:
            return loc

    def next_turn(self, testing, wins):
        self.turn = self.turn + 1
        play = self.turn % 2 - 1
        location = self.choose_location(self.player[play], testing)
        cont = self.board.location_free(location)
        while not cont:
            if not testing:
                print("There is a piece in that location already")
            location = self.choose_location(self.player[play], testing)
            cont = self.board.location_free(location)
        self.player[play].play(self.board, location)
        if not testing:
            self.board.print()
        if self.board.check_win():
            print(self.player[play].piece_type(), "WINS!")
            wins.append(2*play - 1)
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
