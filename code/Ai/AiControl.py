#! /usr/bin/env python
# -*- coding:Utf-8 -*-
__author__ = "Michel Tremblay"


import random
from dames.partie import Partie

class AiControl:
    """Une classe pour generer un AI"""

    def __init__(self, partie, depth):
        self.currentdamier = partie.damier
        self.tempGame = Partie()
        self.depth = depth
        self.history = []
    
    def resetTempGames(self):
        self.tempGame.damier.cases.clear()
        for key in self.currentdamier.cases.keys():
            self.tempGame.damier.cases[key] = self.currentdamier.cases[key]
        return self.tempGame.damier.cases
    
    def GetPossibleSource(self):
        couleur = self.tempGame.couleur_joueur_courant
        possibleSource = []
        doitPrendre = self.tempGame.joueur_courant_peut_prendre_piece_adverse()
        for key in self.tempGame.damier.cases.keys():
            try:
                self.tempGame.valider_position_source(key)
                destpossible = self.tempGame.damier.lister_deplacements_possibles_a_partir_de_position(key)
                if destpossible != []:
                    possibleSource.append(key)
            except Exception as e:
                message = e.msg
        return possibleSource

    def testPossibilities(self):
        randomCheck = 5
        tested = 0
        testedDepth = 0
        firstHistory = []
        currentHistory = []
        BigHistory = []
        #while testedDepth < depth:
        while tested < randomCheck:
            testrun = self.RunThisTest()
            if testrun:
                firstHistory.append(testrun)
                self.tempGame.passer_au_joueur_suivant()
                testrun2 = self.RunThisTest()
                if testrun2:
                    currentHistory.append((firstHistory.copy(),testrun2,self.gameWeight()))
                    firstHistory.clear()
                    self.resetTempGames()
                    tested = tested + 1
        BigHistory.append(currentHistory)
        return BigHistory


    def GetBestMove(self,history):
        white,black = self.gameWeight()
        points = []
        bestMove = []
        bestPowerPossible = 0
        TheRealBestMove = []
        for i in history[0]:
            points.append(i[2][1])
        pointBlackToGet = max(points)
        points.clear()
        for i in history[0]:
            points.append(i[2][0])
        pointWhiteToGet = min(points)
        for i in history[0]:
            if i[2][1] == pointBlackToGet or i[2][0] == pointWhiteToGet:
                bestMove.append((i[1][1],i[1][2], self.GetPowerOfTheMove(white,black,pointBlackToGet,pointWhiteToGet)))
        bestPowerPossible = max(c for (a,b,c) in bestMove)
        
        for i in bestMove:
            if i[2] == bestPowerPossible:
                TheRealBestMove.append((i[0],i[1]))
        return random.choice(TheRealBestMove)


    def GetPowerOfTheMove(self,white,black,resultBlack,resultWhite):
        whitePower = white - resultWhite
        blackPower = black - resultBlack
        return blackPower + whitePower
            
          

                

    def RunThisTest(self):
        possibleSource = self.GetPossibleSource() 
        doitPrendre = self.tempGame.joueur_courant_peut_prendre_piece_adverse()
        ChoosedSource = random.choice(possibleSource)
        PossibleDest = self.tempGame.damier.lister_deplacements_possibles_a_partir_de_position(ChoosedSource,doitPrendre)
        if PossibleDest != []:
            ChoosedDest = random.choice(PossibleDest)
            self.tempGame.damier.deplacer(ChoosedSource,ChoosedDest)
            return self.tempGame.couleur_joueur_courant,ChoosedSource,ChoosedDest
        else: 
            return False

    def gameWeight(self):
        """ Weight is the points each piece is worth
            pion = 1 points
            dame = 2 points
        """
        white = 0
        black = 0
        for item in self.tempGame.damier.cases.values():
            if str(item) == "x" or str(item) == "o":
                if str(item) == "x":
                    black = black + 1
                else:
                    white = white + 1
            if str(item) == "X" or str(item) == "O":
                if str(item) == "X":
                    black = black + 2
                else:
                    white = white + 2
        pointage = (white,black)
        return pointage



               
        

        


