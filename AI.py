import Game
import math


class Ai:
    def __init__(self, turn=0):
        self.board = Game.Board()
        self.turn = turn

    def __set_board(self, board):
        self.board = board

    @staticmethod
    def search(moves):
        """
        checks each move and returns a value that is a weighted win ratio.
        Assumes that there is a move in the moves list
        :param moves: the moves that have already been done or test. It is also the list of moves to not test.
        :return: the "weight" of winning form the current position. Positive is victory to 'O'
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
                board = Game.Board.copy(move)
                turn = len(moves)
                if board.check_win():
                    cost = cost + Game.Game.win_cost(turn) * math.factorial(10 - turn)
                else:
                    cost = cost + Ai.search(move)
                del board
                if turn >= 9:
                    return 0
            else:
                continue
        return cost

    def pick_position(self, starting):
        """
        picks the best move by searching through the move set
        :param starting: the moves that have already happened before the AI's turn
        :return: the [1-9] position that is the best for the Ai
        """
        turn = len(starting) + 1
        weight = Game.Game.player_weight(turn)
        bmove, bcost = 0, -100000000
        for num in range(10):
            if num not in starting:
                # search through each move
                move = list(starting)
                move.append(num)
                cost = Ai.search(move) * weight
                if cost > bcost:
                    # pick the move with the highest points
                    bmove = num
            else:
                continue
        return bmove




    def turn(self, current_board):
        self.__set_board(current_board)

