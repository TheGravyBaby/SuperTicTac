import os
import sys

# state of game with all the needed information to progress
class GameNode:
    # nodes can be constructed using a gameState, a move history
    def __init__(self, board, history):
        self.boardState = board
        self.moveHistory = history
        self.winState = checkForWin(self)
        self.validMoves = listValidMoves(self)

# given a node and a move, we output the conditions of a node
# we can either set the current node equal to this new node (new turn)
# or we can use this to create any additional nodes needed for the Monte
def makeMove(node, move):
    if move in node.validMoves:
        node.moveHistory.Add(move)
        if len(node.moveHistory) % 2 == 0:
            node.boardState[move[0]][move[1]] = 1
        else:
            node.boardState[move[0]][move[1]] = 2
    return node

# will list all valid moves given a board state and a history
# moves are listed as [y, x]
def listValidMoves(node):
    validMoves = []
    if node.winState != 0:                                                              # if the game is won then return no valid moves
        return validMoves
    if len(node.moveHistory) > 0:
        bigBoard = projectCoordinateToNextBoardZone(node.moveHistory[-1])
        bb0 = bigBoard[0]
        bb1 = bigBoard[1]
        wins = makeWinArray(node.boardState)
        if wins[bb0][bb1] == 1 or wins[bb0][bb1] == 2:                                      # if the return board has already been won by either 1 or 2
            validMoves = validateAllPossible(node)
        else:                                                                               # if we weren't sent back to an invalid board, select all tiles from that board
            for i in range(3):
                for j in range(3):
                    move = []
                    move.append(3 * bigBoard[0] + i)
                    move.append(3 * bigBoard[1] + j)
                    if move not in node.moveHistory:
                        validMoves.append(move)
    else:
        validMoves = validateAllPossible(node)
    return validMoves

# usually called when sent to an invalid square or at the start of a game
# validates any coordinate that hasn't been played on a valid board zone
def validateAllPossible(node):
    validMoves = []
    wins = makeWinArray(node.boardState)
    for i in range(9):
        for j in range(9):
            move = [i,j]                                                            # make all tiles playable
            moveBB = projectCoordinateToCurrentBoardZone(move)                      # except tiles that fall in the win zone, which is any big board win, mapped to all its smaller coordinates
            moveBB0 = moveBB[0]
            moveBB1 = moveBB[1]
            if wins[moveBB0][moveBB1] == 0 and move not in node.moveHistory:                 # so 01 bigBoard is 00. if win[0][0] is 0, make a play
                validMoves.append(move)
    return validMoves

# every move will effect the next move by projecting to a different board zone
# this takes a move and finds the next zone to be played
def projectCoordinateToNextBoardZone(move):
    output = []
    for x in move:
        if x == 0 or x == 3 or x == 6:
            output.append(0)
        if x == 1 or x == 4 or x == 7:
            output.append(1)
        if x == 2 or x == 5 or x == 8:
            output.append(2)
    return output                                                  #returns a point on the big board such as 2,2, which would be the right hand corner

# similar to the previous function, this one just finds which zone the move
# was played in, rather than projecting the next move
def projectCoordinateToCurrentBoardZone(move):
    output = []
    for x in move:
        if 0 <= x < 3:
            output.append(0)
        if 3 <= x < 6:
            output.append(1)
        if 6 <= x < 9:
            output.append(2)
    return output

# will detect if any of the board zones have been won
# it then projects those wins to a normal ticTacToe board
# exploit the +1 +2 +3 feature of a small board section
# horizontile relationship [a,b], [a+1,b], [a+2,b]
# vertical relationship [a, b], [a, b+1], [a, b+2]
# diagonal relationship [a,b], [a+1,b+1], [a+1,b+1] also works with minus
def makeWinArray(node):

    board = node.boardState
    winArray = [[0]*3, [0]*3, [0]*3]

    # imagine 1,1
    # starts wit h
    for i in range(3):
        for j in range(3):
            for k in range(3):
                #vertical, check three columns
                if board[3 * i][3 * j + k] == board[3 * i + 1][3 * j + k] == board[3 * i + 2][3 * j + k] != 0:
                    winArray[i][j] = board[3 * i][3 * j + k]
                #horizontile check three rows
                if board[3 * i + k][3 * j] == board[3 * i + k][3 * j + 1] == board[3 * i + k][3 * j + 2] != 0:
                    winArray[i][j] = board[3 * i + k][3 * j]
            # forward diagonal, only two diag tests vs three straight ones
            if board[3 * i][3 * j] == board[3 * i + 1][3 * j + 1] == board[3 * i + 2][3 * j + 2] != 0:
                    winArray[i][j] = board[3 * i][3 * j]
            # backdiagonal
            if board[3 * i + 2][3 * j] == board[3 * i + 1][3 * j + 1] == board[3 * i][3 * j + 2] != 0:
                    winArray[i][j] = board[3 * i + 2][3 * j]
    return winArray

# using the win array board, we check to see if there are any big board wins
def checkForWin(node):
    win = makeWinArray(node)
    for i in range(3):
        if win[i][0] == win[i][1] == win[i][2] != 0:         # check the three horizontiles
            return win[i][0]                                 # simply returns the player number for the win
        if win[0][i] == win[1][i] == win[2][i] != 0:         # check the three verticals
            return win[i][0]
    if win[0][0]  == win[1][1] == win[2][2] != 0:            # check for each diagonal
        return win[0][0]
    if win[2][0] == win[1][1] == win[0][2] != 0:
        return win[0][0]
    else:
        return 0

############################################################################
def clear():
    os.system( 'cls' )

#create some colors to help with game
#taken from https://www.geeksforgeeks.org/print-colors-python-terminal/
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
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
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

    for i in range(len(board)):                             # for every row of the array
        if i== 0:
            print("{} | ".format(i + 1), end = "")
        if i != 0 and i % 3 != 0:                           # if it factorable by 3, print an extra line as spacer
            print("")
            print("{} | ".format(i + 1), end = "")
        if i != 0 and i % 3 == 0 :
            print("")
            print("  | ")
            print("{} | ".format(i + 1), end = "")

        for j in range(len(board[i])):
                if (j + 1) % 3 != 0:
                    if board[i][j] == 1:
                        print(colors.bg.red + str(board[i][j]) + colors.reset, end = ' ')
                    if board[i][j] == 2:
                        print(colors.bg.blue + str(board[i][j]) + colors.reset, end = ' ')
                    if board[i][j] == 0:
                        if [i,j] in validMoves():
                            print(colors.fg.yellow + str(board[i][j]) + colors.reset, end = ' ')
                        else:
                            print(str(board[i][j]), end = ' ')

                #if it factorable by 3, print extra space
                else:
                    if board[i][j] == 1:
                        print(colors.bg.red + str(board[i][j]) + colors.reset, end = '      ')
                    if board[i][j] == 2:
                        print(colors.bg.blue + str(board[i][j]) + colors.reset, end = '      ')
                    if board[i][j] == 0:
                        if [i,j] in validMoves():
                            print(colors.fg.yellow + str(board[i][j]) + colors.reset, end = '      ')
                        else:
                            print(str(board[i][j]), end = '      ')
    print("")
    print("---------------------------------")

# def getUserInput(node):
#     if node.validMoves > 0:
#         if len(node.moveHistory) % 2 == 0:
#             print(colors.bg.red + "Player {}".format(player) + colors.reset, end = ' ')
#         else:
#             print(colors.bg.blue + "Player {}".format(player) + colors.reset, end = ' ')
#         print("please enter in a valid coordinate, or enter r for rules, or v for valid moves...")

#         coordinate = input()
#         if coordinate == "v":
#             numberList = ""
#             validMoves = listValidMoves()
#             for move in validMoves:
#                 numberList += str(move[1] + 1)
#                 numberList += str(move[0] + 1)
#                 numberList += "  "
#             print("Coordinates are inputed as xy. No commas, no spaces, no nothin!")
#             print("Valid moves:")
#             print("")
#             print(numberList)
#             print("")
#             getUserInputGraphical(player)
#         if coordinate == "r":
#             print("1. The goal of the game is to win Tic Tac Toe on the large game board")
#             print("2. To win a tile on the large board, you must win Tic Tac Toe on its respective smaller board")
#             print("3. The previous move will determine which board will be in play for the next move")
#             print("   For example, if you play the upper right hand corner on a small board the next")
#             print("   big board play will be the upper right hand board")
#             print("4. If sent to a board which has already been won, all available tiles will be playable")
#             print("")
#             getUserInputGraphical(player)
#         else:
#             coordinateArray = []
#             try:
#                 coordinateArray.append(int(coordinate[1]) - 1)
#                 coordinateArray.append(int(coordinate[0]) - 1)
#                 makeMove(node, coordinateArray)


initial_board = [ [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]   # do this as multiplying by 9 will copy index through the columns, weird
initial_history = []
initial_game = GameNode(initial_board, initial_history)
# getUserInput(initial_game)
printGameState(initial)
