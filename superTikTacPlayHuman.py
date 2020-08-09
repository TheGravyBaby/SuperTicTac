from superTicTacNodes import *
from superTicTacConsole import *

def startNewGame():
    
    # initial_board = [[0, 1, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 1, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0], 
    # [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 1, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 1, 0], 
    # [0, 1, 0, 0, 1, 2, 0, 1, 0], [0, 0, 0, 0, 0, 2, 0, 1, 0]]

    initial_board = [ [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
    initial_history = []
    game = GameNode(initial_board, initial_history)
    playGame(game)

startNewGame()