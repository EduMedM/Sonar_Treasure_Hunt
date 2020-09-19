'''
	Sona Treasure Hunt
	EduMedM
'''

from math import sqrt
from random import randint, choice
import sys
from os import system, name
from time import sleep

def clear():

	if (name == 'nt'): #for Windows
		_ = system('cls')

	else:              #for Linux or Mac (name is 'posix')
		 _ = system('clear')

def menu():

	while True:
		print("\n\n#### SONAR TREASURE HUNT ####")
		print("\nEnter an option (name or number): ")
		print("\n1.- Play.")
		print("\n2.- Instructions.")
		print("\n3.- Exit.")

		option = input("\nOption: ").lower()

		if (option.startswith('p') or option == '1'):
			mode = selectMode()
			if mode is None:
				continue
			else:
				clear()
				return [mode*5, (mode*2+1)*10, mode] # n*5: numbers of rows depending on level
											   		 # (mode*2+1)*10: numbers of columns depending on level.

		elif(option.startswith('i') or option == '2'):
			instructions()

		elif(option.startswith('e') or option == '3'):
			clear()
			sys.exit()

		else:
			print("\n\nChoose a correct option. ",end='')
			sleep(1)

def selectMode():

	while True:
		clear()
		print("\n\n#### SONAR TREASURE HUNT ####")
		print("\nEnter an option (name or number): ")
		print("\n1.- Easy.")
		print("\n2.- Normal.")
		print("\n3.- Hard.")
		print("\n4.- Exit.")

		option = input("\nOption: ").lower()

		if (option.startswith('ea') or option == '1'):
			return 1
		elif(option.startswith('n') or option == '2'):
			return 2
		elif(option.startswith('h') or option == '3'):
			return 3	
		elif(option.startswith('ex') or option == '4'):
			clear()
			return None
		else:
			print("\n\nChoose a correct option. ",end='')
			sleep(1)

def createABoard(rows, columns):

	new_board = []
	for i in range(rows):
		new_board.append([])
		for j in range(columns):
			caracter = choice(['~','`'])
			new_board[i].append(caracter)

	return new_board

def displayBoard(board, rows, columns):

	board_row = ''
	spaces = ' '*9
	# X axis
	x_tens = '    '
	x_numbers = '   ' + '0123456789' * (columns//10)

	for i in range(1,(columns//10)):
		x_tens += spaces + str(i)
	
	print()
	print(x_tens)
	print(x_numbers)
	print()

	for row in range(rows):
		board_row = ''
		if row < 10: extra_space = ' '
		else: extra_space = ''

		for column in range(columns):
			board_row += board[row][column]

		print("{0:2} {1:} {2:2}".format(row, board_row, row))
		
	print()
	print(x_numbers)
	print(x_tens)
	print()

def userMove(moves_used):

	while True:
		move = input().lower()
		if move.startswith('e'):
			sys.exit()

		move = move.split()
		if len(move) == 2:
			try:
				x = int(move[0])
				y = int(move[1])
			except ValueError:
				print("Enter a integer.")
				continue	
			if isOnBoard(x,y) is True:
				print("\nThe coordenate is not on the board.")
				continue
			if(x,y) not in moves_used:
				return [x,y]
			else:
				print("Coordenate used.")	
		else:
			print("Must be 2 values, x and y.")

def isOnBoard(x,y):

	global nrows, ncolumns
	return x >= ncolumns or y >= nrows

def getChests(n, rows, columns):

	chests = []
	i = 0
	while i < n:
		temp_chest = (randint(0, columns-1), randint(0, rows-1))
		if temp_chest not in chests:
			chests.append(temp_chest)
			i += 1
	return chests

def numberOfSonars(n):

	if mode == 1:	return 10
	elif mode == 2: return 17
	elif mode == 3: return 20;

def foundChest(board, x, y, chests):

	distance = 0
	small_distance = 99

	for x_chest, y_chest in chests:
		distance = round(sqrt((x_chest - x)**2 + (y_chest - y)**2))

		if distance < small_distance:
			small_distance = distance

	if small_distance < 10:
		if small_distance == 0:
			chests.remove((x,y))
			phrase = "\n*** You have found a chest! ***\n"

			return phrase, True
		else:
			board[y][x] = str(small_distance)
			phrase = "\n*** Treasure detected at %s from this sonar. ***\n" % (small_distance)
			return phrase, False
	else:
		board[y][x] = 'X'
		phrase = "\n*** The sonar didn't detect a treasure at (%s, %s). ***\n" % (x, y)
		return phrase, False

def instructions():
	
	print('''
	Your mission is to use sonar devices to find a number 
	of sunken treasure chests (that change depending on 
	the level) at the bottom of the ocean. But the sonar 
	only finds distance, not direction.

	Enter the coordinates (x and y) to drop a sonar device. 
	The ocean map will be marked with how far away the 
	nearest chest is, or an X if it's beyond the sonar 
	device's range. For example, the C marks are where 
	chests are. The sonar device shows the distance of the
	closest chest.

                    1         2 		
	  012345678901234567890123456789

	0 ~~~~`~```~`~``~~~``~`~~``~~~`` 0
	1 ~`~`~``~~`~```~~~``6~~`~`~~~`~ 1
	2 `~`C``3`~~~~`C`~~~~`````~~``~~ 2
	3 ````````~~~`````~~~`~`````~`~` 3
	4 ~`~~~~`~~`~~`C`~``~~7~~~`~```~ 4

	  012345678901234567890123456789
                    1         2 				

    You can also enter 'exit' to exit.
			''')
	input("\nPress Enter to continue...")

def playAgain():

	print("\n\nDo you want to play again (y/n)?:  ",end='')
	return input().lower().startswith('y')

### Main Loop ###
while True:
	clear()
	nrows, ncolumns, mode = menu()
	nchests = mode
	moves_used = []
	status = False #True if a chest is found, False otherwise.
	phrase = '' # Status phrase: distance or if a chest is found.
	sonar_devices = numberOfSonars(mode)
	board = createABoard(nrows, ncolumns)
	chests = getChests(nchests, nrows, ncolumns)
	displayBoard(board, nrows, ncolumns)

	while sonar_devices > 0:

		print("%s sonar devices left. %s treasures yet to be found." % (sonar_devices, len(chests)))
		print("Coordenates:  ",end='')
		x , y = userMove(moves_used)
		moves_used.append((x,y))
		phrase, status = foundChest(board, x, y, chests)

		if status:
			for x, y in moves_used:
				foundChest(board, x, y, chests)

		displayBoard(board, nrows, ncolumns)
		print(phrase)
		print("chests", chests)

		if len(chests) == 0:
			print("\n*** You won!!! ***")
			break

		sonar_devices -= 1

	if sonar_devices == 0:
		print("You have run out of devices!\nGame Over!")
		print("\nThe chests were here: ")
		for x_chest, y_chest in chests:
			print("({0:2}, {1:2})".format(x_chest, y_chest))

	if(not(playAgain())): exit()
	else: clear()