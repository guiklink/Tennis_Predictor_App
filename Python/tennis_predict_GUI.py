#!/usr/bin/python

import Tkinter as tk
#from PIL import Image
from createTestCase import *
from machineLearning import *
import csv

def exportPlayerDataCSV():
	global tree

	player1 = textBoxP1.get()
	player2 = textBoxP2.get()

	# Load the avg weighted data for each player
	if tree == None:
		msg = "You need to predict at least once before exporting players' data."
		labelExportStatus.configure(bg = "red", text = msg)
	else:
		dataP1 = retrievePlayerData(player1, 1, tournament)
		dataP2 = retrievePlayerData(player2, 2, tournament)
		path = textBoxPath.get()

		file = open(path + '.csv', 'w+')

		# Write P1 Data
		columns = sorted(dataP1.keys())
		columnsToWrite = ''
		dataToWrite = ''
		for item in columns:
			columnsToWrite += str(item) + ','
			dataToWrite += str(dataP1[item]) + ','
		columnsToWrite = columnsToWrite[0:-1]		#remove the extra comma
		file.write(columnsToWrite + '\n')
		dataToWrite = dataToWrite[0:-1]
		file.write(dataToWrite + '\n')

		# Write P2 Data
		columns = sorted(dataP2.keys())
		columnsToWrite = ''
		dataToWrite = ''
		for item in columns:
			columnsToWrite += str(item) + ','
			dataToWrite += str(dataP2[item]) + ','
		columnsToWrite = columnsToWrite[0:-1]		#remove the extra comma
		file.write(columnsToWrite + '\n')
		dataToWrite = dataToWrite[0:-1]
		file.write(dataToWrite + '\n\n')

		file.write('Player1,Player2\n' + player1 + ',' + player2)		
		file.close() 
		msg = "Players' data exported in a .CSV!"
		labelExportStatus.configure(bg = "green", text = msg)
		


def exportTreePDF():
	global tree
	path = textBoxPath.get()
	if tree == None:
		msg = 'You need to predict at least once before exporting a tree.'
		labelExportStatus.configure(bg = "red", text = msg)
	else:
		tree.printTreePDF(path + '.pdf')
		msg = "Tree exported in a .PDF!"
		labelExportStatus.configure(bg = "green", text = msg)

def predict(player1, player2):
	global tournament, tree

	if tree == None:
		tree = Tree()
		tree.train()
	print '\n\nPredicting: ' + player1 + ' | ' + player2 + ' (' + tournament + ')'
	ans, instance, pct = tree.predict(player1, player2, tournament)
	print '\n\nAnswers:'
	print ans
	print pct
	result1 = str(ans[0]) + ' will WIN!'
	resultsLabel.configure(text=result1)
	result2 = 'Dataset used: ' + str(instance)
	print '\n\n>>>' + result2

	#instanceLabel1.configure(bg = "white", text=resultP1)
	#instanceLabel2.configure(bg = "white", text=resultP2)
	statusLabel.configure(bg = "green", text = "Press Predict to start!")

def predButtonCallBack():
	player1 = textBoxP1.get()
	player2 = textBoxP2.get()

	status = ''
	playersAreValid = True

	if player1.lower() == player2.lower():
		status += '[Both players have the same name]'
		playersAreValid = False
	if not isValidPlayer(player1, tournament):
		status += '[Player 1 is not a valid name for this tournament]'
		playersAreValid = False
	if not isValidPlayer(player2, tournament):
		status += '[Player 2 is not a valid name for this tournament]'
		playersAreValid = False
	if tournament == None:
		status += '[No tournament was selected]'
		playersAreValid = False

	if not playersAreValid:
		statusLabel.configure(bg = "red", text=status)
	else:
		statusLabel.configure(bg = "green", text="Predicting...")
		predict(player1, player2)

def AusOpen():
	global tournament
	tournament = 'AUS_OPEN'
	ausButton.configure(bg = "blue")
	usButton.configure(bg = "grey")
	frenchButton.configure(bg = "grey")
	wimbButton.configure(bg = "grey")

def USOpen():
	global tournament
	tournament = 'US_OPEN'
	ausButton.configure(bg = "grey")
	usButton.configure(bg = "blue")
	frenchButton.configure(bg = "grey")
	wimbButton.configure(bg = "grey")

def FrenchOpen():
	global tournament
	tournament = 'FRENCH_OPEN'
	ausButton.configure(bg = "grey")
	usButton.configure(bg = "grey")
	frenchButton.configure(bg = "blue")
	wimbButton.configure(bg = "grey")

def WimbOpen():
	global tournament
	tournament = 'WIMBLEDOM_OPEN'
	ausButton.configure(bg = "grey")
	usButton.configure(bg = "grey")
	frenchButton.configure(bg = "grey")
	wimbButton.configure(bg = "blue")


# MAIN #############################################################
tournament = None
tree = None

root = tk.Tk()
root.title("The tennis match predictor.")

# Load picture #####################################################

imageCanvas = tk.Canvas(bg = "black", height = 400, width = 700)
imageCanvas.pack(side=tk.TOP)

photo = tk.PhotoImage(file = "../images/logo.gif")

image = imageCanvas.create_image(0,0, anchor = tk.NW, image = photo)
imageCanvas.pack()

####################################################################

# Load Textboxes ###################################################

textBoxFrame = tk.Frame(height = 200, width = 700)
textBoxFrame.pack()

labelP1 = tk.Label(textBoxFrame,text = "Enter player 1 name: ")
labelP1.pack(side=tk.LEFT)
textBoxP1 = tk.Entry(textBoxFrame, bd = 5)
textBoxP1.pack(side=tk.LEFT)

labelP2 = tk.Label(textBoxFrame,text = "Enter player 2 name: ")
labelP2.pack(side=tk.LEFT)
textBoxP2 = tk.Entry(textBoxFrame, bd = 5)
textBoxP2.pack(side=tk.LEFT)	

predictButton = tk.Button(textBoxFrame, text = "Predict", command = predButtonCallBack)
predictButton.pack(side = tk.LEFT)

# Menu Frame #####################################################
menuFrame = tk.Frame(height = 200, width = 700)
menuFrame.pack()

## Tournament Menu Box
ausButton = tk.Button(menuFrame, text = "Australian Open", command = AusOpen, bg = "grey")
ausButton.pack(side = tk.LEFT)
usButton = tk.Button(menuFrame, text = "US Open", command = USOpen, bg = "grey")
usButton.pack(side = tk.LEFT)
frenchButton = tk.Button(menuFrame, text = "French Open", command = FrenchOpen, bg = "grey")
frenchButton.pack(side = tk.LEFT)
wimbButton = tk.Button(menuFrame, text = "Wimbledom", command = WimbOpen, bg = "grey")
wimbButton.pack(side = tk.LEFT)
####################################################################

# Status Frame #####################################################
statusFrame = tk.Frame(height = 200, width = 700)
statusFrame.pack()

## Status Label
statusLabel = tk.Label(statusFrame,bg = "green", text = "Press Predict to start!")
statusLabel.pack(side = tk.TOP)

####################################################################

# Results Frame #####################################################
resultsFrame = tk.Frame(height = 200, width = 700)
resultsFrame.pack()

## Status Label
resultsLabel = tk.Label(resultsFrame,bg = "white", text = "Results!")
resultsLabel.pack(side = tk.TOP)

#instanceLabel1 = tk.Label(text = "")
#instanceLabel1.pack()
#instanceLabel2 = tk.Label(text = "")
#instanceLabel2.pack()

## Export Frame
exportFrame = tk.Frame(height = 200, width = 700)
exportFrame.pack()

## Structures for exporting path
labelPath = tk.Label(exportFrame,text = "Export Path: ")
labelPath.pack(side=tk.LEFT)
textBoxPath = tk.Entry(exportFrame, width = 40, bd = 5)
textBoxPath.pack(side=tk.LEFT)
textBoxPath.insert(0,'../Output/')

## Export buttons
playerDataButton = tk.Button(exportFrame, text = "Export Player Data", command = exportPlayerDataCSV)
playerDataButton.pack(side = tk.LEFT)

treePdfButton = tk.Button(exportFrame, text = "Export Tree to PDF", command = exportTreePDF)
treePdfButton.pack(side = tk.LEFT)

## Export Status Label
labelExportStatus = tk.Label(root,text = "")
labelExportStatus.pack(side=tk.BOTTOM)
####################################################################

root.mainloop()
