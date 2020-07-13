import os
import sys
from termcolor import colored, cprint

#variables
gameStateArray = [ [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9, [0]*9]   # do this as multiplying by 9 will copy index through the columns, weird
oneWin = False
twoWin = False
moveHistory = []
currentPlayer = 1

#functions
#clears text on output window
def clear():
    os.system( 'cls' )

# prints the state of the tic tac toe board
def printGameState(array):
    clear()
    print("--------------------------------")
    print("         SUPER TIC TAC TOE      ")
    print("--------------------------------")
    print("    1 2 3      4 5 6      7 8 9 ")
    print("--------------------------------")
    
    for i in range(len(array)):                             # for every row of the array
        if i== 0: 
            print("{} | ".format(i + 1), end = "")
        if i != 0 and i % 3 != 0:                           # if it factorable by 3, print an extra line as spacer
            print("")
            print("{} | ".format(i + 1), end = "")
        if i != 0 and i % 3 == 0 :
            print("")
            print("  | ")
            print("{} | ".format(i + 1), end = "")
        
        for j in range(len(array[i])):     
                if (j + 1) % 3 != 0:
                    if array[i][j] == 1:
                        cprint(str(array[i][j]), 'white', 'on_red', end = ' ')
                    if array[i][j] == 2:
                        cprint(str(array[i][j]), 'white', 'on_blue', end = ' ')
                    if array[i][j] == 0:
                        if [i,j] in listValidMoves():
                            cprint(str(array[i][j]), 'yellow', end = ' ')
                        else:
                            print(str(array[i][j]), end = ' ')
                
                #if it factorable by 3, print extra space
                else:
                    if array[i][j] == 1:
                        cprint(str(array[i][j]), 'white', 'on_red', end = '      ')
                    if array[i][j] == 2:
                        cprint(str(array[i][j]), 'white', 'on_blue', end = '      ')
                    if array[i][j] == 0:
                        if [i,j] in listValidMoves():
                            cprint(str(array[i][j]), 'yellow', end = '      ')
                        else:
                            print(str(array[i][j]), end = '      ')
    print("")
    #print("")                
    print("--------------------------------")

def getUserInput(player):
    if player == 1:
        cprint("Player {}".format(player), 'white', 'on_red', end = ' ')
    if player == 2:
        cprint("Player {}".format(player), 'white', 'on_blue', end = ' ')
    print("please enter in a valid coordinate, or enter h to list valid moves:")
    # if len(moveHistory) > 0:
    #     print(listValidMoves())
    #print(makeWinArray(gameStateArray))
    # print(moveHistory)
    coordinate = input()
    if coordinate == "h":
        numberList = ""
        validMoves = listValidMoves()
        for move in validMoves:
            numberList += str(move[1] + 1)
            numberList += str(move[0] + 1)
            numberList += "  " 
        print("Coordinates are using an xy string. No commas, no spaces, no nothin!")
        print(numberList)
        getUserInput(player)
    else:
        coordinateArray = []
        try: 
            coordinateArray.append(int(coordinate[1]) - 1)
            coordinateArray.append(int(coordinate[0]) - 1)
            if checkInputValidity(coordinateArray):
                changeGameState(gameStateArray, coordinateArray, player)
                printGameState(gameStateArray)
                if checkForWin(gameStateArray) != 0:
                    if player == 1:
                        cprint("!!!!!! PLAYER 1 WINS !!!!!!", 'white', 'on_red') 
                        input()
                    if player == 2:
                        cprint("!!!!!! PLAYER 2 WINS !!!!!!", 'white', 'on_blue') 
                        input()  
                else:  
                    getUserInput(player)
                if player == 1:
                    player = 2
                else:
                    player = 1
            else: 
                print("Invalid Input")
                getUserInput(player)

        except:
            print("Invalid Input")
            getUserInput(player)

def projectCoordinateToNextBoardZone(move):
    output = []
    for x in move: 
        if x == 0 or x==3 or x==6:
            output.append(0)
        if x == 1 or x==4 or x==7:
            output.append(1)
        if x == 2 or x==5 or x==8:
            output.append(2)
    #print(output)
    return output       #returns a point on the big board such as 2,2, which would be the right hand corner

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

def listValidMoves():
    validMoves = []
    if len(moveHistory) > 0:
        bigBoard = projectCoordinateToNextBoardZone(moveHistory[-1])
        bb0 = bigBoard[0]
        bb1 = bigBoard[1]
        wins = makeWinArray(gameStateArray)
        

        if wins[bb0][bb1] == 1 or wins[bb0][bb1] == 2:                                      # if the return board has already been won by either 1 or 2
            for i in range(9):
                for j in range(9):                                                         
                    move = [i,j]                                                            # make all tiles playable
                    moveBB = projectCoordinateToCurrentBoardZone(move)                      # except tiles that fall in the win zone, which is any big board win, mapped to all its smaller coordinates
                    moveBB0 = moveBB[0]                                                     
                    moveBB1 = moveBB[1]
                    # print(wins[moveBB0][moveBB1])
                    if wins[moveBB0][moveBB1] == 0 and move not in moveHistory:             # so 01 bigBoard is 00. if win[0][0] is 0, make a play
                        validMoves.append(move)     
        else:                                                                                # if we weren't sent back to an invalid board, select all tiles from that board                              
            for i in range(3):
                for j in range(3):
                    move = []
                    move.append(3 * bigBoard[0] + i)
                    move.append(3 * bigBoard[1] + j)
                    if move not in moveHistory:
                        validMoves.append(move)  
    else:
        for i in range(9):
            for j in range(9):
                move = [i,j]
                validMoves.append(move)
    return validMoves

def checkInputValidity(move):
    if 0 <= move[0] < 9 and 0 <= move[1] < 9:
        if len(moveHistory) > 0:
            if move in listValidMoves():
                moveHistory.append(move)
                return True
            else:
                return False
        else:
            moveHistory.append(move)
            return True
    else:
        return False

def changeGameState(array, coordinate, player):
    array[ coordinate[0] ][ coordinate[1] ] = player

# exploit the +1 +2 +3 feature of a small board section
# horizontile relationship [a,b], [a+1,b], [a+2,b]
# vertical relationship [a, b], [a, b+1], [a, b+2] 
# diagonal relationship [a,b], [a+1,b+1], [a+1,b+1] also works with minus
# loopy loopy loops
def makeWinArray(array):
    winArray = [[0]*3, [0]*3, [0]*3]

    # imagine 1,1
    # starts wit h
    for i in range(3):
        for j in range(3):     
            for k in range(3):
                #vertical, check three columns 
                if array[3 * i][3 * j + k] == array[3 * i + 1][3 * j + k] == array[3 * i + 2][3 * j + k] != 0:
                    winArray[i][j] = array[3 * i][3 * j + k]
                #horizontile check three rows
                if array[3 * i + k][3 * j] == array[3 * i + k][3 * j + 1] == array[3 * i + k][3 * j + 2] != 0:
                    winArray[i][j] = array[3 * i + k][3 * j]
            # forward diagonal, only two diag tests vs three straight ones 
            if array[3 * i][3 * j] == array[3 * i + 1][3 * j + 1] == array[3 * i + 2][3 * j + 2] != 0:
                    winArray[i][j] = array[3 * i][3 * j]
            # backdiagonal
            if array[3 * i + 2][3 * j] == array[3 * i + 1][3 * j + 1] == array[3 * i][3 * j + 2] != 0:
                    winArray[i][j] = array[3 * i + 2][3 * j]
    return winArray

def checkForWin(array):
    win = makeWinArray(array)
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

#initialization
printGameState(gameStateArray)
getUserInput(1)