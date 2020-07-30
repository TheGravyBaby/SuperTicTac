import os
import sys
from superTicTacNodes import *

# Graphical Funtions!
############################################################################
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# create some colors to help with game
# taken from https://www.geeksforgeeks.org/print-colors-python-terminal/
class colors:
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'

    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'


def printGameState(node):
    board = node.boardState
    validMoves = node.validMoves

    clear()
    print("--------------------------------")
    print("         SUPER TIC TAC TOE      ")
    print("--------------------------------")
    print("    1 2 3      4 5 6      7 8 9 ")
    print("--------------------------------")

    # for every row of the array
    for i in range(len(board)):
        if i == 0:
            print("{} | ".format(i + 1), end="")
        # if it factorable by 3, print an extra line as spacer
        if i != 0 and i % 3 != 0:
            print("")
            print("{} | ".format(i + 1), end="")
        if i != 0 and i % 3 == 0 :
            print("")
            print("  | ")
            print("{} | ".format(i + 1), end="")

        for j in range(len(board[i])):
            if (j + 1) % 3 != 0:
                if board[i][j] == 1:
                    print(colors.bg.red + str(board[i][j]) + colors.reset, end=' ')
                if board[i][j] == 2:
                    print(colors.bg.blue + str(board[i][j]) + colors.reset, end=' ')
                if board[i][j] == 0:
                    if [i,j] in validMoves:
                        print(colors.fg.yellow + str(board[i][j]) + colors.reset, end=' ')
                    else:
                        print(str(board[i][j]), end=' ')

            # if it factorable by 3, print extra space
            else:
                if board[i][j] == 1:
                    print(colors.bg.red + str(board[i][j]) + colors.reset, end='      ')
                if board[i][j] == 2:
                    print(colors.bg.blue + str(board[i][j]) + colors.reset, end='      ')
                if board[i][j] == 0:
                    if [i,j] in validMoves:
                        print(colors.fg.yellow + str(board[i][j]) + colors.reset, end='      ')
                    else:
                        print(str(board[i][j]), end='      ')
    print("")
    print("---------------------------------")


def getUserInput(node):
    if len(node.validMoves) > 0:
        if len(node.moveHistory) % 2 == 0:
            print(colors.bg.red + "Player 1" + colors.reset, end = ' ')
        else:
            print(colors.bg.blue + "Player 2" + colors.reset, end = ' ')
        print("please enter in a valid coordinate, or enter r for rules, or v for valid moves...")

        coordinate = input()
        if coordinate == "v":
            numberList = ""
            validMoves = node.validMoves
            for move in validMoves:
                numberList += str(move[1] + 1)
                numberList += str(move[0] + 1)
                numberList += "  "
            print("Coordinates are inputed as xy. No commas, no spaces, no nothin!")
            print("Valid moves:")
            print("")
            print(numberList)
            print("")
            getUserInput(node)
        if coordinate == "r":
            print("1. The goal of the game is to win Tic Tac Toe on the large game board")
            print("2. To win a tile on the large board, you must win Tic Tac Toe on its respective smaller board")
            print("3. The previous move will determine which board will be in play for the next move")
            print("   For example, if you play the upper right hand corner on a small board the next")
            print("   big board play will be the upper right hand board")
            print("4. If sent to a board which has already been won, all available tiles will be playable")
            print("")
            getUserInput(node)

        else:
            coordinateArray = []
            
            if len(coordinate) == 2 :
                try:
                    coordinateArray.append(int(coordinate[1]) - 1)
                    coordinateArray.append(int(coordinate[0]) - 1)
                except:
                    printGameState(node)
                    print("Invalid Input : " + coordinate)
                    getUserInput(node)

                if coordinateArray in node.validMoves:
                    try:
                        makeMove(node, coordinateArray)
                    except:
                        printGameState(node)
                        print("Some fubar shit is afoot...")
                        getUserInput(node)
                else:
                    printGameState(node)
                    print("Invalid Input : " + coordinate)
                    getUserInput(node) 
            else: 
                printGameState(node)
                print("Invalid Input : " + coordinate)
                getUserInput(node) 


def startNewGame():
    initial_board = [ [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]
    initial_history = []
    game = GameNode(initial_board, initial_history)
    playGame(game)


def playGame(node):
    printGameState(node)
    getUserInput(node)
    if node.winState == 0 and len(node.validMoves) != 0:
        playGame(node)
    else: 
        if node.winState == 0:
            printGameState(node)
            print("DRAW! No winner, no legal moves!")
        else:
            printGameState(node)
            print("!!!! PLAYER {} WINS !!!!".format(node.winState))

# initialize the game!
startNewGame()