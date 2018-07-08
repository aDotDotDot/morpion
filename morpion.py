# -*- coding: utf-8 -*-
import random
from PIL import Image
class Grid:
    def __init__(self, grid=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]):
        self.grid = grid
        self.lastTurn = 0
        self.opposites = {'X': 'O', 'O': 'X'}

    def __str__(self):
        strR = "-------------"
        for i in self.grid:
            strR += "\n| "
            for p in i:
                if p == 0:
                    strR += "  | "
                else:
                    strR += p + " | "
            strR += "\n-------------"
        return strR

    def drawIt(self):
        gridBlank = Image.open('./morpion_blank.png', 'r')#240*210 pixels
        grid_X = [Image.open('./morpion_X_1.png', 'r'), Image.open('./morpion_X_2.png', 'r')]#42*39, 42*27
        grid_O = [Image.open('./morpion_O_1.png', 'r'), Image.open('./morpion_O_2.png', 'r')]#42*33, 42*42
        offset = [[(42, 44), (40, 108), (40, 168)],
                  [(116, 46), (116, 110), (114, 178)],
                  [(192, 48), (192, 110), (196, 176)]]
        #offset = [[(42, 44), (46, 116), (48, 192)],
                  #[(108, 40), (116, 110), (190, 110)],
                  #[(158, 40), (118, 172), (196, 178)]]
        for i in range(3):
            for j in range(3):
                (theOffsetX, theOffsetY) = offset[i][j]
                if self.grid[j][i] == 'X':
                    rdmImg = random.choice(grid_X)
                    (rdmX, rdmY) = rdmImg.size
                    theOffset = (theOffsetX - rdmX // 2, theOffsetY - rdmY // 2)
                    gridBlank.paste(rdmImg, theOffset)
                if self.grid[j][i] == 'O':
                    rdmImg = random.choice(grid_O)
                    (rdmX, rdmY) = rdmImg.size
                    theOffset = (theOffsetX - rdmX//2, theOffsetY - rdmY//2)
                    gridBlank.paste(rdmImg, theOffset)
        #img.size
        #gridBlank.paste(grix_O[0], theOffset)
        gridBlank.save('out.png')

    def getLine(self, nb):
        if nb in range(3):
            return self.grid[nb]

    def getColumn(self, nb):
        if nb in range(3):
            return [self.grid[0][nb], self.grid[1][nb], self.grid[2][nb]]

    def getDiagonals(self, localGrid = None):
        if not localGrid:
            localGrid = self.grid
        return [[localGrid[0][0], localGrid[1][1], localGrid[2][2]],
                [localGrid[2][0], localGrid[1][1], localGrid[0][2]]]

    def reverse(self):
        gridR = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                gridR[j][i] = self.grid[i][j]
        return gridR

    def line(self, tupleG):
        (a, b, c) = tupleG
        return a != 0 and a == b and a == c

    def isComplete(self):
        # lignes
        isF = self.line((self.grid[0][0], self.grid[0][1], self.grid[0][2]))
        isF = isF or self.line((self.grid[1][0], self.grid[1][1], self.grid[1][2]))
        isF = isF or self.line((self.grid[2][0], self.grid[2][1], self.grid[2][2]))
        # colonnes
        isF = isF or self.line((self.grid[0][0], self.grid[1][0], self.grid[2][0]))
        isF = isF or self.line((self.grid[0][1], self.grid[1][1], self.grid[2][1]))
        isF = isF or self.line((self.grid[0][2], self.grid[1][2], self.grid[2][2]))
        # diagonales
        isF = isF or self.line((self.grid[0][0], self.grid[1][1], self.grid[2][2]))
        isF = isF or self.line((self.grid[2][0], self.grid[1][1], self.grid[0][2]))
        return isF

    def isDraw(self):
        return not self.isComplete() and len(self.allEmptySpaces()) < 1

    def emptyLineSpaces(self, index):
        emptySpaces = []
        for i in range(3):
            if self.grid[index][i] == 0:
                emptySpaces.append([index, i])
        return emptySpaces

    def emptyColumnSpaces(self, index):
        emptySpaces = []
        for i in range(3):
            if self.grid[i][index] == 0:
                emptySpaces.append([i, index])
        return emptySpaces

    def emptyDiagonalSpaces(self, index, localGrid = None):
        if not localGrid:
            localGrid = self.grid.copy()[:]
        indexes = [[[0, 0], [1, 1], [2, 2]], [[2, 0], [1, 1], [0, 2]]]
        emptySpaces = indexes[index]
        ret = []
        for i in range(3):
            if localGrid[emptySpaces[i][0]][emptySpaces[i][1]] == 0:
                ret.append(emptySpaces[i])
        return ret

    def allEmptySpaces(self):
        allSpaces = []
        for i in range(3):
            for p in self.emptyLineSpaces(i):
                allSpaces.append(p)
        return allSpaces

    def play(self, item, x, y):
        if self.isComplete():
            print("Cette partie est déjà terminée")
            return True
        if item != self.lastTurn:
            if x in range(3) and y in range(3) and self.grid[x][y] == 0:
                print("Je place mon " + item + " en " + str(x) + " " + str(y))
                self.grid[x][y] = item
                self.lastTurn = item
                return True
            else:
                print("Vous ne pouvez pas placer de pion " + item + " ici " + str(x) + " " + str(y))
                return False
        else:
            print("Ce n'est pas votre tour !")
            return True

    def canIWin(self, item, localGrid = None):
        if not localGrid:
            localGrid = self.grid.copy()[:]
        cptL = 0
        for line in localGrid:
            if item+item == ''.join(str(x) for x in line).replace('0', ''):
                return self.emptyLineSpaces(cptL)
            cptL += 1
        cptC = 0
        for column in localGrid:
            if item+item == ''.join(str(x) for x in column).replace('0', ''):
                return self.emptyColumnSpaces(cptC)
            cptC += 1
        cptD = 0
        for diag in self.getDiagonals(localGrid):
            if item + item == ''.join(str(x) for x in diag).replace('0', ''):
                return self.emptyDiagonalSpaces(cptD)
            cptD += 1

    def canILose(self, item):
        return self.canIWin(self.opposites[item])

    def canIWinByPlaying(self, item, x, y):
        localGrid = self.grid.copy()[:]
        localGrid[x][y] = item
        return self.canIWin(item, localGrid)

    def botPlay(self, item):
        if self.isComplete():
            print("Cette partie est déjà terminée")
            return False
        if item == self.lastTurn:
            print("Ce n'est pas votre tour !")
            return False
        winningMove = self.canIWin(item)
        avoidingLose = self.canILose(item)
        if winningMove and len(winningMove) > 0:
            (posX, posY) = winningMove[0]
            self.play(item, posX, posY)
        elif avoidingLose and len(avoidingLose) > 0:
            (posX, posY) = avoidingLose[0]
            self.play(item, posX, posY)
        else:
            if self.grid[1][1] == 0:
                (posX, posY) = (1, 1)
                self.play(item, posX, posY)
            else:
                allEmptySpaces = self.allEmptySpaces()
                # because I'm lazy, ideally we check here where we can open the most canIWin by testing everything
                (posX, posY) = random.choice(allEmptySpaces)
                """
                self.grid[posX][posY] = item
                cpt = 0
                while not self.canIWin(item) and cpt < len(allEmptySpaces):
                    self.grid[posX][posY] = 0
                    (posX, posY) = random.choice(allEmptySpaces)
                    self.grid[posX][posY] = item
                    cpt += 1
                self.grid[posX][posY] = 0
                """
                self.play(item, posX, posY)

        if self.isComplete():
            print("Les "+item+" gagnent !")
            return False
        elif self.isDraw():
            print("Match nul")
            return False
        else:
            print("Tour suivant : "+self.opposites[item])
            return(self.opposites[item])



maGrille = Grid()
print(maGrille)
nextItem = maGrille.botPlay('O')
print(maGrille)
while not (maGrille.isComplete() or maGrille.isDraw()):
    nextItem = maGrille.botPlay(nextItem)
    print(maGrille)
maGrille.drawIt()
"""
maGrille = Grid([[0, 0, 0], [0, 'X', 0], ['O', 0, 0]])
print(maGrille)
print(maGrille.isComplete())
maGrille.botPlay('O')
maGrille.botPlay('X')
maGrille.botPlay('O')
maGrille.botPlay('O')
print(maGrille)
"""

"""
print(maGrille.getDiagonals())
print(maGrille.emptyDiagonalSpaces(0))
print(maGrille.emptyDiagonalSpaces(1))
"""

"""
print(maGrille.getLine(1))
print(maGrille.getColumn(1))
maGrille.play('O', 0, 0)
maGrille.play('O', 0, 0)
maGrille.play('X', 2, 2)
print(maGrille)
"""

"""
def ligne(tupleG):
    (a,b,c) = tupleG
    return (a != 0 and a == b and a == c)

def estFinie(grille):
    #lignes
    isF = ligne((grille[0][0], grille[0][1], grille[0][2]))
    isF = isF or ligne((grille[1][0], grille[1][1], grille[1][2]))
    isF = isF or ligne((grille[2][0], grille[2][1], grille[2][2]))
    #colonnes
    isF = isF or ligne((grille[0][0], grille[1][0], grille[2][0]))
    isF = isF or ligne((grille[0][1], grille[1][1], grille[2][1]))
    isF = isF or ligne((grille[0][2], grille[1][2], grille[2][2]))
    #diagonales
    isF = isF or ligne((grille[0][0], grille[1][1], grille[2][2]))
    isF = isF or ligne((grille[2][0], grille[1][1], grille[0][2]))
    return isF




print(estFinie(grille))
"""