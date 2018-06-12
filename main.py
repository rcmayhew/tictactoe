import Game


def sim_game():
    wins = []
    attempts = 100000
    tic = Game.Game()
    for x in range(attempts):
        tic.start_game(wins, testing=True)

    x = sum(wins)
    rate = (1 - x) / (2 * attempts)
    print(x)
    print(rate)
    # negative means that X is winning more
    # positive means that O is winning more
    # zero means ties
    # completely random numbers give it to X


def real_game():
    wins = []
    tic = Game.Game()
    tic.start_game(wins, testing=False)


sim = False
if sim:
    sim_game()
else:
    real_game()
