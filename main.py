#
# J Wells - wellsjason543 at gmail dot com - jwellsuhhuh (Discord)
#

from os.path import isfile
import csv
import copy
import re

# for folder creation
from datetime import datetime
import os

# debug only
from cmu_cpcs_utils import prettyPrint

class Member:
    def __init__(self, name: list):
        self.name: str = name
        self.pieces: list[tuple] = [] # (piece, instrument)
        
    def __str__(self):
        return f'{self.name}: {self.pieces}'
    
    def __repr__(self): # not true repr
        return f'{self.name}: {self.pieces}' 

    def addPiece(self, piece: str, instrument: str):
        self.pieces.append((piece, instrument))

pieces: list[str] = []

def addSymphonyMembers(members: list[Member], symphony2dList: list[list[str]], pieces: list[str]):
    # find all cells that end with "conductor" (anchor for piece and member names)
    conductorCells: list[tuple] = []
    for rowIndex in range(0,len(symphony2dList)):
        for colIndex in range(0,len(symphony2dList[0])):
            if symphony2dList[rowIndex][colIndex].lower().endswith('conductor'):
                conductorCells.append((rowIndex, colIndex))
    
    # rearrange conductorCells so that 1st,3rd... are at beginning and 2nd,4th... are at end
    # since code scans the spreadsheet left-right top-down and we want to transform it to top-down left-right 
    evenIndexes = conductorCells[::2]
    oddIndexes = conductorCells[1::2] 
    conductorCells = evenIndexes + oddIndexes
                
    # for each "conductor" cell
    for conductorCellIndex in range(0,len(conductorCells)):
        piece: str = symphony2dList[conductorCells[conductorCellIndex][0]-1][conductorCells[conductorCellIndex][1]]
        pieces.append(piece)
        currentNameCell: list[int] = [conductorCells[conductorCellIndex][0], conductorCells[conductorCellIndex][1]+2]
        while True: # while not yet 3 consecutive empty rows
            if (symphony2dList[currentNameCell[0]][currentNameCell[1]] == '' and
                symphony2dList[currentNameCell[0]+1][currentNameCell[1]] == '' and
                symphony2dList[currentNameCell[0]+2][currentNameCell[1]] == ''):
                break
            
            # get instrument pertaining to the currentNameCell
            currentInstrumentCell: list[int] = [currentNameCell[0], currentNameCell[1]-1]
            while symphony2dList[currentInstrumentCell[0]][currentInstrumentCell[1]] == '':
                currentInstrumentCell[0] -= 1 # scroll up until instrument is there

            # get and filter instrument name
            instrument: str = symphony2dList[currentInstrumentCell[0]][currentInstrumentCell[1]]
            endIndex = instrument.find(' =')
            if endIndex != -1: instrument = instrument[:endIndex] # strip at " =" if applicable
            if instrument[0] in '0123456789': instrument = instrument[2:] # remove leading numbers and a space (eg. in "3 percussion")

            # get and filter member name
            name: str = symphony2dList[currentNameCell[0]][currentNameCell[1]]
            endIndex = max(name.find(','), name.find(' ('), name.find(' ['))
            if endIndex != -1: name = name[:endIndex] # strip stuff after end of name

            # skip names that start with these words
            namesToSkip = ['vacant', 'guest', 'tbd']
            for nameToSkip in namesToSkip:
                if name.lower().startswith(nameToSkip):
                    currentNameCell[0] += 1 # go to next row
                    continue

            # skip names that are empty or '--'
            if name == '' or name == '--':
                currentNameCell[0] += 1 # go to next row
                continue

            # deal with "same roster as above" names,
            # does NOT consider exceptions eg. "same roster as above (minus a, b and c)"
            if name.startswith("same roster as above"):
                # get name of previous piece
                abovePiece: str = symphony2dList[conductorCells[conductorCellIndex-1][0]-1][conductorCells[conductorCellIndex-1][1]]
                # add every member on that instrument from previous piece to this piece
                for member in members:
                    for piecePlaying in member.pieces:
                        if piecePlaying[0] == abovePiece and piecePlaying[1] == instrument:
                            member.addPiece(piece, instrument)
                currentNameCell[0] += 1 # go to next row
                continue
            
            # add name to members
            createNewEntry = True
            for memberIndex in range(0,len(members)):
                if members[memberIndex].name == name:
                    createNewEntry = False
                    # add piece playing to existing member
                    members[memberIndex].addPiece(piece, instrument)
            if createNewEntry:
                # create new member and add piece playing
                members.append(Member(name))
                members[-1].addPiece(piece, instrument)
            
            currentNameCell[0] += 1 # go to next row

def addChamberMembers(members: list[Member], chamber2dList: list[list[str]], pieces: list[str]):
    chamberPieces: list[str] = [] # to store pieces that will be added to all strings players
    
    for rowIndex in range(0,len(chamber2dList)):
        for colIndex in range(0,len(chamber2dList[0])):
            if chamber2dList[rowIndex][colIndex].lower().find('name') != -1:
                # find cell called "name" (anchor for string member names)
                nameCell: tuple = (rowIndex, colIndex)
            elif chamber2dList[rowIndex][colIndex].lower().find('flute 1') != -1:
                # find cell called "flute 1" (anchor for piece names and wind member names)
                flute1Cell: tuple = (rowIndex, colIndex)
                instrumentColumn = flute1Cell[1] # fixed column for getting instrument for currentNameCell
             
    # get first piece name from "Flute 1" cell
    currentPieceCell: list[int] = [flute1Cell[0]-1, flute1Cell[1]+1]
    while chamber2dList[currentPieceCell[0]][currentPieceCell[1]] != '':
        # add piece
        piece: str = chamber2dList[currentPieceCell[0]][currentPieceCell[1]]
        pieces.append(piece)
        chamberPieces.append(piece) # to store pieces that will be added to all strings players

        # add wind/percussion players for the piece
        currentNameCell: list[int] = [currentPieceCell[0]+1, currentPieceCell[1]]
        while True: # while not yet 3 consecutive empty rows
            if (chamber2dList[currentNameCell[0]][currentNameCell[1]] == '' and
                chamber2dList[currentNameCell[0]+1][currentNameCell[1]] == '' and
                chamber2dList[currentNameCell[0]+2][currentNameCell[1]] == ''):
                break

            # get instrument pertaining to the currentNameCell
            currentInstrumentCell: list[int] = [currentNameCell[0], instrumentColumn]
            while chamber2dList[currentInstrumentCell[0]][currentInstrumentCell[1]] == '':
                currentInstrumentCell[0] -= 1 # scroll up until instrument is there

            # get and filter instrument name
            instrument: str = chamber2dList[currentInstrumentCell[0]][currentInstrumentCell[1]]
            endIndex = instrument.find(' =')
            if endIndex != -1: instrument = instrument[:endIndex] # strip at " =" if applicable
            if instrument[0] in '0123456789': instrument = instrument[2:] # remove leading numbers and a space (eg. in "3 percussion")

            # get and filter member name
            name: str = chamber2dList[currentNameCell[0]][currentNameCell[1]]
            endIndex = max(name.find(','), name.find(' ('), name.find(' ['))
            if endIndex != -1: name = name[:endIndex] # strip stuff after end of name

            # skip names that start with these words
            namesToSkip = ['vacant', 'guest', 'tbd']
            for nameToSkip in namesToSkip:
                if name.lower().startswith(nameToSkip):
                    currentNameCell[0] += 1 # go to next row
                    continue

            # skip names that are empty or '--'
            if name == '' or name == '--':
                currentNameCell[0] += 1 # go to next row
                continue

            # add name to members
            createNewEntry = True
            for memberIndex in range(0,len(members)):
                if members[memberIndex].name == name:
                    createNewEntry = False
                    # add piece playing to existing member
                    members[memberIndex].addPiece(piece, instrument)
            if createNewEntry:
                # create new member and add piece playing
                members.append(Member(name))
                members[-1].addPiece(piece, instrument)
            
            currentNameCell[0] += 1 # go to next row
        
        currentPieceCell[1] += 1 # go to next piece

    # add string players to ALL chamber pieces
    currentNameCell: list[int] = [nameCell[0]+1, nameCell[1]] # using "name" cell as anchor
    while True: # while not yet 3 consecutive empty rows
        if (chamber2dList[currentNameCell[0]][currentNameCell[1]] == '' and
            chamber2dList[currentNameCell[0]+1][currentNameCell[1]] == '' and
            chamber2dList[currentNameCell[0]+2][currentNameCell[1]] == ''):
            break

        # get instrument pertaining to the currentNameCell
        currentInstrumentCell: list[int] = [currentNameCell[0], currentNameCell[1]-1]
        while chamber2dList[currentInstrumentCell[0]][currentInstrumentCell[1]] == '':
            currentInstrumentCell[0] -= 1 # scroll up until instrument is there

        # get and filter instrument name
        instrument: str = chamber2dList[currentInstrumentCell[0]][currentInstrumentCell[1]]
        endIndex = instrument.find(' =')
        if endIndex != -1: instrument = instrument[:endIndex] # strip at " =" if applicable
        if instrument[0] in '0123456789': instrument = instrument[2:] # remove leading numbers and a space (eg. in "3 percussion")

        # get and filter member name
        name: str = chamber2dList[currentNameCell[0]][currentNameCell[1]]
        endIndex = max(name.find(','), name.find(' ('), name.find(' ['))
        if endIndex != -1: name = name[:endIndex] # strip stuff after end of name

        # skip names that start with these words
        namesToSkip = ['vacant', 'guest', 'tbd']
        for nameToSkip in namesToSkip:
            if name.lower().startswith(nameToSkip):
                currentNameCell[0] += 1 # go to next row
                continue

        # skip names that are empty or '--'
        if name == '' or name == '--':
            currentNameCell[0] += 1 # go to next row
            continue

        # add name to members
        createNewEntry = True
        for memberIndex in range(0,len(members)):
            if members[memberIndex].name == name:
                createNewEntry = False
                # add all chamber pieces to existing member
                for piece in chamberPieces:
                    members[memberIndex].addPiece(piece, instrument)
        if createNewEntry:
            # create new member and add all chamber pieces
            members.append(Member(name))
            for piece in chamberPieces:
                members[-1].addPiece(piece, instrument)
        
        currentNameCell[0] += 1 # go to next row

def createPieces2dList(members: list[Member], pieces: list[str]):
    # make empty matrix containing piece names
    pieces2dList: list[list[str]] = [[''] * len(pieces) for _ in range(len(members))]
    for memberIndex in range(0,len(members)): # each member
        for pieceIndex in range(0,len(pieces)): # each of all pieces
            for piecePlayingIn in members[memberIndex].pieces: # each piece the member is playing in
                if piecePlayingIn[0] == pieces[pieceIndex]:
                    # insert instrument name into the index for the piece they're playing in
                    pieces2dList[memberIndex][pieceIndex] = piecePlayingIn[1]
    
    return pieces2dList   

def getFilename(prompt: str) -> str:
    while True:
        filename = input(f'\n{prompt}')
        print()

        if not filename.endswith('.txt'): filename += '.txt'
        if not filename.startswith('private/'): filename = 'private/' + filename

        filename = f'{filename}'
        if not isfile(filename):
            print("Invalid file name. File must be in 'private' folder.")
            continue
        
        return filename

def createFolderInPrivate() -> str:
    dateTimeNow = datetime.today().strftime('%Y-%m-%d_%H;%M;%S')
    path = f'private/{dateTimeNow}'
    os.makedirs(path)
    return path

def main():
    members: list[Member] = []
    pieces: list[str] = []

    # Process symphony roster
    symphonyFilename = getFilename('Symphony Roster Filename: ')
    with open(symphonyFilename) as file:
        symphony2dList: list[list[str]] = list(csv.reader(file, delimiter='\t'))
    addSymphonyMembers(members, symphony2dList, pieces)

    # Process chamber roster
    chamberFilename = getFilename('Chamber Orchestra Roster Filename: ')
    with open(chamberFilename) as file:
        chamber2dList: list[list[str]] = list(csv.reader(file, delimiter='\t'))
    addChamberMembers(members, chamber2dList, pieces)

    folderPath = createFolderInPrivate()

    # export dashboard .txt (.csv format)
    filename = 'dashboard.txt'
    memberNames: list = [member.name for member in members] 
    pieces2dList: list[list[str]] = createPieces2dList(members, pieces)
    dashboardCSV: list[list[str]] = [['Name'] + [piece for piece in pieces]] # header
    print(dashboardCSV)

    index = 0
    for name in memberNames:
        dashboardCSV.append([name] + pieces2dList[index])
        index += 1

    with open(f'{folderPath}/{filename}', 'w') as file:
        csvWriter = csv.writer(file,delimiter=',')
        csvWriter.writerows(dashboardCSV)

if __name__ == "__main__":
    main()