#
# J Wells - wellsjason543 at gmail dot com - jwellsuhhuh (Discord)
#

from os.path import isfile
import csv
import copy

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

def addSymphonyMembers(members: list[Member], symphony2dList, pieces):
    # find all cells that end with "conductor"
    conductorCells: list[tuple] = []
    for rowIndex in range(0,len(symphony2dList)):
        for colIndex in range(0,len(symphony2dList[0])):
            if symphony2dList[rowIndex][colIndex].endswith('conductor'):
                conductorCells.append((rowIndex, colIndex))
                
    # for each "conductor" cell
    for conductorCellIndex in range(0,len(conductorCells)):
        piece: str = symphony2dList[conductorCells[conductorCellIndex][0]-1][conductorCells[conductorCellIndex][1]]
        pieces.append(piece)
        currentNameCell: list = [conductorCells[conductorCellIndex][0], conductorCells[conductorCellIndex][1]+2]
        while True: # while not yet 3 consecutive empty rows
            if (symphony2dList[currentNameCell[0]][currentNameCell[1]] == '' and
                symphony2dList[currentNameCell[0]+1][currentNameCell[1]] == '' and
                symphony2dList[currentNameCell[0]+2][currentNameCell[1]] == ''):
                break
            
            # get instrument pertaining to the currentNameCell
            currentInstrumentCell: list = [currentNameCell[0], currentNameCell[1]-1]
            while symphony2dList[currentInstrumentCell[0]][currentInstrumentCell[1]] == '':
                currentInstrumentCell[0] -= 1 # scroll up until instrument is there

            # get and filter instrument name
            instrument: str = symphony2dList[currentInstrumentCell[0]][currentInstrumentCell[1]]
            endIndex = instrument.find('=') - 1
            if 0 <= endIndex: instrument = instrument[0:endIndex] # strip at " =" if applicable

            # get and filter member name
            name: str = symphony2dList[currentNameCell[0]][currentNameCell[1]]
            endIndex = max(name.find(','), name.find(' ('))
            if 0 <= endIndex: name = name[0:endIndex] # strip stuff after end of name

            # deal with "same as above" names
            if name.startswith("same as above"):
                # get name of piece 2 pieces ago
                abovePiece: str = symphony2dList[conductorCells[conductorCellIndex-2][0]-1][conductorCells[conductorCellIndex-2][1]]
                # add every member on that instrument from 2 pieces ago to this piece
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

def addChamberMembers(members: list[Member], chamber2dList):
    pass

def createPieces2dList(members: list[Member], pieces: list[str]):
    pieces2dList: list[list] = [pieces] + [[''] * len(pieces) for _ in range(len(members))]
    for memberIndex in range(0,len(members)): # each member
        for pieceIndex in range(0,len(pieces)): # each of all pieces
            for piecePlayingIn in members[memberIndex].pieces: # each piece the member is playing in
                if piecePlayingIn[0] == pieces[pieceIndex]:
                    # insert instrument name into the index for the piece they're playing in
                    pieces2dList[memberIndex+1][pieceIndex] = piecePlayingIn[1]
    
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
        symphony2dList: list[list] = list(csv.reader(file, delimiter='\t'))
    addSymphonyMembers(members, symphony2dList, pieces)

    # Process chamber roster
    chamberFilename = getFilename('Chamber Orchestra Roster Filename: ')
    with open(chamberFilename) as file:
        chamber2dList: list[list] = list(csv.reader(file, delimiter='\t'))
    # addChamberMembers(members, chamber2dList, pieces)

    # Process board member list
    boardFilename = getFilename('Board Members List Filename: ')
    boardMembersList: list = []
    with open(boardFilename) as file:
        for line in file.readlines():
            boardMembersList.append(line.strip())
        
    # recreate the member list with filters
    oldMembers = copy.deepcopy(members)
    members: list[Member] = []
    for member in oldMembers:
        # skip "guest musician" and "" members
        if member.name.startswith('Guest Musician') or member.name == '':
            continue
        # move board members to beginning of member list
        if member.name in boardMembersList:
            members.insert(0, member)
        # append rest of members as usual
        else: members.append(member)

    folderPath = createFolderInPrivate()

    # export Member names.txt
    filename = 'names.txt'
    with open(f'{folderPath}/{filename}', 'w') as file:
        for member in members:
            file.write(f'{member.name}\n')
    
    # export Member pieces.txt
    filename = 'pieces.txt'
    pieces2dList = createPieces2dList(members, pieces)
    with open(f'{folderPath}/{filename}', 'w') as file:
        csvWriter = csv.writer(file,delimiter=',')
        csvWriter.writerows(pieces2dList)

if __name__ == "__main__":
    main()

        