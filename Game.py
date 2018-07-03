import random


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
        """
        Gives the type of character that the Piece is
        :return: the char type that is embedded in the Piece
        """
        return self.piece

    def not_null(self):
        """
        checks if the Piece is a black space
        :return: True if the Piece is a space
        """
        if self.character_type() is not ' ':
            return True
        else:
            return False


class Board:
    def __init__(self):
        """
        Creates a board with empty spaces
        """
        self.layout = [[Piece() for x in range(4)] for y in range(4)]

    def new_board(self):
        """
        Copys self and returns a copy as a new board
        :return: the new Board that is equal
        """
        moves = self.convert_to_list()
        board = Board.copy(moves)
        return board

    def turn_count(self):
        """
        Gives the amount of turns that have been played
        :return: the number of turns as an int
        """
        moves = self.convert_to_list()
        return len(moves)

    @staticmethod
    def copy(moves):
        """
        Creates a new board from a list of moves.
        :param moves: the list of moves as int, assumes that the moves are [X, O] order
        :return: gives the new Board
        """
        board = Board()
        for idx, move in enumerate(moves):
            loc = Game.convert_int(move)
            turn, piece = Game.determine_player(idx - 1)
            board.__play_piece__(loc, piece)
        return board

    @staticmethod
    def merge_list(xmoves, omoves):
        """
        merges the lists to make a single list of all the moves
        :param xmoves: the list of all x moves
        :param omoves: the list of all o moves
        :return: returns a list of [X, O] from the given lists
        """
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
        """
        Converts the board into a list in alternating [X, O] order
        :return: the list of all moves done so far
        """
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
        """
        Places the Piece at the location
        :param location: is the location to get the Piece, should already be checked and collected by the Game
        :param piece: the Piece that is being played. Should be chosen based on whose turn it is
        """
        x, y = location
        self.layout[x][y] = piece

    def clear(self):
        """
        Makes the Board empty, filled with space Pieces
        """
        self.layout = [[Piece() for x in range(4)] for y in range(4)]

    def print_element(self, location):
        """
        gives the number as an int
        :param location: the x, y position
        :return: returns the char from the Piece at that location
        """
        if not self.get_element(location).not_null():
            return Game.convert_position(location)
        else:
            return self.get_element(location).character_type()

    def print(self):
        """
        Prints out the Board in the form for Tic Tac Toe
        """
        print("\n")
        print("-------------")
        print("|", self.print_element((0, 0)), "|", self.print_element((1, 0)), "|", self.print_element((2, 0)), "|")
        print("-------------")
        print("|", self.print_element((0, 1)), "|", self.print_element((1, 1)), "|", self.print_element((2, 1)), "|")
        print("-------------")
        print("|", self.print_element((0, 2)), "|", self.print_element((1, 2)), "|", self.print_element((2, 2)), "|")
        print("-------------")

    def get_element(self, location):
        """
        Gives the Piece at the location
        :param location: the location that that element
        :return: the Piece at the location
        """
        x, y = location
        return self.layout[x][y]

    def location_free(self, location):
        """
        Checks if the location is a space Piece
        :param location: the location to check in coordinate form
        :return: returns True if the element is not a space
        """
        if self.get_element(location).not_null():
            return False
        else:
            return True

    def down(self, location):
        """
        Checks the down direction
        :param location: the starting location, should be in coordinate form
        :return: returns the mid point and the Piece at the mid point
        """
        x, y = location
        mid = (x, y + 1)
        return mid, self.get_element(mid)

    def left(self, location):
        """
        Checks the left direction
        :param location: the starting location, should be in coordinate form
        :return: the mid point and the Piece at the mid point
        """
        x, y = location
        mid = (x - 1, y)
        return mid, self.get_element(mid)

    def dial(self, location):
        """
        Checks the diagonal left direction
        :param location: the starting location, should be in coordinate form
        :return: returns the mid point and the Piece at the mid point
        """
        x, y = location
        mid = (x - 1, y + 1)
        return mid, self.get_element(mid)

    def diar(self, location):
        """
        Checks the diagonal right direction
        :param location: the starting location, should be in coordinate form
        :return: returns the mid point and the Piece at the mid point
        """
        x, y = location
        mid = (x + 1, y + 1)
        return mid, self.get_element(mid)

    def following(self, first, mid):
        """
        From two points, it follows the line and checks the next spot in the line
        :param first: the starting point, should be in coordinate form
        :param mid: the second spot in the line, should be in coordinate form
        :return: the last position in the line, in coordinate form, and the Piece at that location
        """
        x1, y1 = first
        x2, y2 = mid
        last = (2 * x2 - x1, 2 * y2 - y1)
        return last, self.get_element(last)

    def __down_check(self, location):
        """
        Checks the whole of the down line and uses the down function
        :param location: the starting location in coordinate form
        :return: True if there is a winning line in the down direction from the starting location
        """
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
        """
        Checks the whole of the down line and uses the left function
        :param location: the starting location in coordinate form
        :return: True if there is a winning line in the left direction from the starting location
        """
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
        """
        Checks the whole of the diagonal left line and uses the down function
        :param location: the starting location in coordinate form
        :return: True if there is a winning line in the diagonal left direction from the starting location
        """
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
        """
        Checks the whole of the diagonal right line and uses the down function
        :param location: the starting location in coordinate form
        :return: True if there is a winning line in the diagonal right direction from the starting location
        """
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

    def check_win(self):
        """
        Checks all the possible axises for a win
        :return: True if there is a win, False is there isn't a win
        """
        if (self.__down_check((0, 0)) or self.__diar_check((0, 0)) or self.__down_check((1, 0)) or
                self.__down_check((2, 0)) or self.__left_check((2, 0)) or self.__dial_check((2, 0)) or
                self.__left_check((2, 1)) or self.__left_check((2, 2))):
            return True
        else:
            return False

    def down_axis(self):
        """
        Checks the value of all down axises
        :return: the numeric value determined by the heuristic of the down axises
        """
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
        """
        Checks the value of all side axises
        :return: the numeric value determined by the heuristic of the side axises
        """
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
        """
        Checks the value of the diagonal left axis
        :return: the numeric value determined by the heuristic of the diagonal left
        """
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
        """
        Checks the value of the diagonal right axis
        :return: the numeric value determined by the heuristic of the diagonal right
        """
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
        """
        Computes the heuristic value of the axises
        :param xrow: the total number of 'X' in the axis
        :param orow: the total number of 'O' in the axis
        :return: 0 if there is a block or empty axis, 3^n when n is the number of pieces in the axis
        """
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
        """
        Adds the value of all axises
        :return: the total value of the board
        """
        return self.down_axis() + self.side_axis() + self.dial_axis() + self.diar_axis()


class Player:
    """
    Creates a new Player with a Piece. Defaults to 'O' and being a true player and not an ai
    :param: piece: the char that should be played, is type char, defaults to 'O'
    :param: actual: whether or not it is a player that is being controlled by an actual person
    """
    def __init__(self, piece='O', actual=True):
        self.char = Piece(piece)
        self.person = actual

    def play(self, board, location):
        """
        Has the player play thier Piece
        :param board: is type Board, it is the current Board that is being played on
        :param location: the location that they want to play the Piece, should be in coordinate form
        """
        board.__play_piece__(location, self.piece_type())

    def is_real(self):
        """
        Checks if the player is controlled by a real player
        :return: True if controlled by a person, False if it is controlled by the computer.
        """
        if self.person:
            return True
        else:
            return False

    def piece_type(self):
        """
        Checks the char that is in the Piece held by the Player
        :return: the char in the Player
        """
        return self.char

    def set_piece(self, piece):
        """
        Changed the char in the Piece held by the Player
        :param piece: the character that the current char will be changed to
        """
        self.char = piece

    @staticmethod
    def pick_position(starting):
        """
        Picks the best move by searching through the move set for a player that is computer controlled
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

    @staticmethod
    def player_input():
        """
        Handles user inputs and exceptions
        :return: the user input after making sure it is in a 1-9 int range
        """
        while True:
            try:
                res = int(input("where do you want to place a piece?, 1-9  "))
                if res < 1 or res > 9:
                    raise ValueError
                break
            except (ValueError, NameError):
                print("Numbers between 1-9 please.")
        return res


class Game:
    def __init__(self):
        """
        Creates a Board of empty Pieces, and defaults to the first player being controlled by a player, and the second
        Player is controlled by the computer. The turn is set to 0.
        """
        self.board = Board()
        self.player = [Player('X', actual=True), Player('O', actual=False)]
        self.turn = 0

    @staticmethod
    def choose_location(player, board, testing=False):
        """
        Asks the player for the location if they are a real, if they are an ai, it picks a position with its heuristic
        :param player: the Player that will be playing the Piece
        :param board: the Board that will get the Piece added to it
        :param testing: whether the game is being simulated or not, default no
        :return:
        """
        # will add input options later
        if player.is_real():
            if not testing:
                hold = Player.player_input()
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
        """
        converts the number of the move to the move in coordinate form
        :param move: the numeric in in range from 1-9
        :return: the move in coordinate form
        """
        num = move - 1
        y = 2 - (num // 3)
        x = num % 3
        loc = (int(x), int(y))
        return loc

    @staticmethod
    def convert_position(pair):
        """
        converts the coordinate form location into the int location
        :param pair: the location to be converted
        :return: the converted location in range form 1-9
        """
        x, y = pair
        return (2 - y)*3 + x + 1

    @staticmethod
    def determine_player(turn):
        """
        Figures out which Player's turn it is
        :param turn: the turn as an int
        :return: the player index and their Piece
        """
        if turn % 2 == 0:
            return 0, Piece('O')
        else:
            return 1, Piece('X')

    @staticmethod
    def player_weight(turn):
        """
        Gives the appropriate weight for each player
        :param turn: the players turn as an int
        :return: -1 if second player, 1 if the first player
        """
        if turn % 2 == 0:
            return -1
        else:
            return 1

    @staticmethod
    def win_cost(turn):
        """
        Gives the win rate weight based on whose turn it is
        :param turn: the turn after it has been modded by 2
        :return: the weight as an int
        """
        return -2*turn + 1

    def next_turn(self, testing, wins):
        """
        Progresses game forward one turn. Its deals with asking for each players move and loops over all turns
        until the game is over.
        :param testing: the bool if it is testing or not
        :param wins: the list of wins
        """
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
                print(self.player[play].piece_type().character_type(), "WINS!")
                wins.append(self.win_cost(play))
                return False

            if self.turn == 9:
                print("Its a tie!")
                wins.append(0)
                return False
        else:
            if self.board.check_win():
                if self.player[play].piece_type() == 'X':
                    print(self.player[play].piece_type().character_type(), "WINS!")
                wins.append(self.win_cost(play))
                return False

            if self.turn == 9:
                wins.append(0)
                return False
        return True

    def start_game(self, wins, testing=False):
        """
        Starts the game and assumes the game is on turn 0
        :param wins: the list of all wins
        :param testing: bool to determine if the game is simulated or not
        :return:
        """
        start = True

        while start:
            position = 1
            self.board.clear()
            self.turn = 0

            num = Game.game_type()
            if num == 1:
                position = Game.goes_first()
            self.set_ai(num, position)

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

    def set_ai(self, num, turn=1):
        """
        Sets how many players are playing the game
        :param num: the number of real players
        :param turn: the turn that the real person will be playing in
        """
        if num == 0:
            self.player = [Player('X', actual=False), Player('O', actual=False)]
        elif num == 2:
            self.player = [Player('X', actual=True), Player('O', actual=True)]
        else:
            if turn == 1:
                self.player = [Player('X', actual=True), Player('O', actual=False)]
            if turn == 2:
                self.player = [Player('X', actual=False), Player('O', actual=True)]


    @staticmethod
    def game_type():
        """
        asks for how many players
        :return: how many real players after making sure it is in a 0-2 int range
        """
        while True:
            try:
                res = int(input("How many players are playing? (0,1,2) "))
                if res < 0 or res > 2:
                    raise ValueError
                break
            except (ValueError, NameError):
                print("Numbers between 0-2 please.")
        return res

    @staticmethod
    def goes_first():
        """
        asks who goes first
        :return: the position that the real player chose a 0-2 int range
        """
        while True:
            try:
                res = int(input("Are you going first or second? (1,2) "))
                if res < 1 or res > 2:
                    raise ValueError
                break
            except (ValueError, NameError):
                print("Numbers between 1-2 please.")
        return res


wins = []
game = Game()
game.start_game(wins)