from superTicTacNodes import *
from superTicTacConsole import *
from superTicTacMonte import * 

def startNewGame():
    
    # initial_board = [[0, 1, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 1, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0], 
    # [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 1, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 1, 0], 
    # [0, 1, 0, 0, 1, 2, 0, 1, 0], [0, 0, 0, 0, 0, 2, 0, 1, 0]]

    initial_board = [ [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
    initial_history = []
    game = GameNode(initial_board, initial_history)
    playGame(game)

def playGame(node):
    printGameState(node)

    if node.winState == 0 and len(node.validMoves) != 0:
        getUserInput(node)
        printGameState(node)
        monte_runner(node)
         

    else: 
        if node.winState == 0:
            printGameState(node)
            print("DRAW! No winner, no legal moves!")
        else:
            printGameState(node)
            print("!!!! PLAYER {} WINS !!!!".format(node.winState))

startNewGame()
