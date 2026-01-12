#
# J Wells - wellsjason543 at gmail dot com - jwellsuhhuh (Discord)
#

from datetime import datetime
import os # for folder creation
from os.path import isfile
import csv

class Member:
    def __init__(self, name: list):
        self.name = name
        self.pieces: list = []
        
    def __str__(self):
        return f'{self.name}: {self.pieces}'

def addSymphonyMembers(members: list[Member], symphony2dList):
    pass

def addChamberMembers(members: list[Member], chamber2dList):
    pass

def createPieces2dList(members):
    pass

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

    # Process symphony roster
    symphonyFilename = getFilename('Symphony Roster Filename: ')
    with open(symphonyFilename) as file:
        symphony2dList: list[list] = list(csv.reader(file, delimiter='\t'))
    addSymphonyMembers(members, symphony2dList)

    # Process chamber roster
    chamberFilename = getFilename('Chamber Orchestra Roster Filename: ')
    with open(chamberFilename) as file:
        chamber2dList: list[list] = list(csv.reader(file, delimiter='\t'))
    addChamberMembers(members, chamber2dList)

    # Process board member list
    boardFilename = getFilename('Board Members List Filename: ')
    with open(boardFilename) as file:
        boardMembersList: list = file.readlines()

    # Move board members to beginning of members list
    memberIndex = 0
    while memberIndex < len(members): # loop through every member
        memberName = members[memberIndex].name
        if memberName in boardMembersList:
            members.insert(members[memberIndex], 0) # move it to beginning of list
            del members[memberIndex+1]
        memberIndex += 1

    folderPath = createFolderInPrivate()

    # export Member names.txt
    filename = 'names.txt'
    with open(f'{folderPath}/{filename}', 'w') as file:
        for member in members:
            file.write(member.name)
    
    # export Member pieces.txt
    filename = 'pieces.txt'
    pieces2dList = createPieces2dList(members)
    with open(f'{folderPath}/{filename}', 'w') as file:
        csvWriter = csv.writer(file,delimiter=',')
        csvWriter.writerows(pieces2dList)

if __name__ == "__main__":
    main()

        