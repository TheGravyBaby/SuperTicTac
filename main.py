import os
import sys
from superTicTacNodes import *
from superTicTacConsole import *
from superTicTacMonte import*

initial_board = [ [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
initial_history = []

print("--------------------------------")
print("         SUPER TIC TAC TOE      ")
print("--------------------------------")
print(" ")


def main():
    clear()
    print("Welcome to Super Tic Tac Toe, what would yo2u like to do?")
    print("1. Play a Human.")
    print("2. Play Monte Carlo AI.")
    x = 0
    allowed_playouts = 0
    z = 0
    
    x = input()

    if (x == "1"):
        startNewGameHuman()
    if (x == "2"):
        print("How many seconds would you like the Monte to search for a move? (1-600)")
        allowed_playouts = input()
        try:
            allowed_playouts = int(allowed_playouts)
        except: 
            print("Follow instructions plz...")
            input()
            main()
        
        print("Would you like to be player 1 or 2?")
        z = input()
        
        if (z == "1"):
            startNewGameMonte(1, allowed_playouts)

        if (z == "2"):
            startNewGameMonte(2, allowed_playouts)
        else :
            print("Follow instructions plz...")
            input()
            main()

    else:
        print("Follow instructions plz...")
        input()
        main()



def startNewGameHuman():
    gameNode = GameNode(initial_board, initial_history)
    playGame(gameNode)

def startNewGameMonte(player, iterations):
    game = GameNode(initial_board, initial_history)
    playGameMonte(game, player, iterations)


def playGame(node):
    printGameState(node)

    if node.winState == 0 and len(node.validMoves) != 0:
        getUserInput(node)
        playGame(node)
    else: 
        if node.winState == 0:
            printGameState(node)
            print("DRAW! No winner, no legal moves!")
        else:
            printGameState(node)
            print("!!!! PLAYER {} WINS !!!!".format(node.winState))


def playGameMonte(node, player, iterations):
    printGameState(node)

    while (node.winState == 0 and len(node.validMoves) != 0):
        
        if player == 2 : 
            makeMove(node, monte_runner(node, iterations))
            printGameState(node)
        else : 
            getUserInput(node)
            printGameState(node)
               
        # check if win after previous move
        if node.winState == 0 and len(node.validMoves) != 0:
            if player == 2 : 
                getUserInput(node)
                printGameState(node)
            else : 
                makeMove(node, monte_runner(node, iterations))
                printGameState(node)

    else: 
        if node.winState == 0:
            printGameState(node)
            print("DRAW! No winner, no legal moves!")
        else:
            printGameState(node)
            print("!!!! PLAYER {} WINS !!!!".format(node.winState))
    
    input()

main()