#! /usr/bin/env python
# -*- coding:Utf-8 -*-

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
from dames.partie import Partie

        

class InterfaceDamier(tk.Frame):
    """
    Classe permettant l'affichage d'un damier. À modifier!
    @author: Bryan Oakley, Camille Besse, Jean-Francis Roy
    """

    def __init__(self, parent, taille_case,damier):
        """taille_case est la taille d'un côté d'une case en pixels."""
        # Definition du damier : # de cases
        self.n_lignes = 8
        self.n_colonnes = 8

        # Definition du damier : taille des cases (en pixels)
        self.taille_case = taille_case

        # Definition du damier : couleur de cases
        self.couleur1 = "white"
        self.couleur2 = "gray"

        # Pièces sur le damier
        self.damier = damier

        # Calcul de la taille du dessin
        canvas_width = self.n_colonnes * self.taille_case
        canvas_height = self.n_lignes * self.taille_case

        # Initialisation de la fenêtre parent contenant le canvas
        tk.Frame.__init__(self, parent)
        
        
        # Initialisation du canvas
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=canvas_width, height=canvas_height,
                               background="white")

        # On place le canvas et le plateau (self) à l'aide de "grid".
        self.canvas.grid(padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W) #redim la fenetre 
        self.grid(padx=4, pady=4, sticky=tk.N + tk.S + tk.E + tk.W) # redim le plateau

        # Fait en sorte que le redimensionnement de la fenêtre redimensionne le damier
        self.canvas.bind("<Configure>", self.actualiser)
        
    

    def ajouter_piece(self, position, piece):
        """
        Ajoute une pièce sur le damier.
        """

        tempfont = ('Helvetica', self.taille_case//2)
        #piece_unicode = caracteres_unicode_pieces[nom_piece[0:2]]

        # On "dessine" la pièce
        ligne, colonne = position
        nom_piece = piece.nom
        self.canvas.create_text(ligne, colonne, text=piece, tags=(nom_piece, "piece"), font=tempfont)
        
        # On place la pièce dans le canvas (appel de placer_piece)
        self.placer_piece((ligne, colonne), nom_piece)


    def placer_piece(self, position, nom_piece):
        """
        Place une pièce à la position donnée (ligne, colonne).
        """
        #tk.messagebox.showinfo("wow",self.canvas.itemcget(nom_piece, 'text')) 
        ligne, colonne = position

        # Placer les pieces au centre des cases.
        x = (colonne * self.taille_case) + int(self.taille_case / 2)
        y = (ligne * self.taille_case) + int(self.taille_case / 2)

        # On change la taille de la police d'écriture selon la taille actuelle des cases.
        tempfont = ('Helvetica', self.taille_case//2)
        self.canvas.itemconfigure(nom_piece, font=tempfont)
        self.canvas.coords(nom_piece, x, y)
    
    def selectCase(self, position):
        # Selection de la case (afficher d'une manière graphique la case selectionné)
        x1 = position[0] * self.taille_case
        x2 = x1+self.taille_case
        y1 = position[1]*self.taille_case
        y2 = y1+self.taille_case
        color = "yellow"
        self.canvas.delete("selected")
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="selected")
        # on met les pièces au dessus de la selection de case
        self.canvas.tag_raise("piece")

    def ActualiserPieces(self,Create,new):
        # On redessine les pieces
        if new:
            self.damier.initialiser_damier_par_default()
        if Create:
            self.canvas.delete("piece")
            for position, piece in self.damier.cases.items():
                self.ajouter_piece(position, piece)
        else:
            for position, piece in self.damier.cases.items():
                self.placer_piece(position, piece.nom)

        # On mets les pieces au dessus des cases
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("case")    

    def actualiser(self, event):
        """
        Redessine le damier lorsque la fenetre est redimensionnée.
        """
        
        # Calcul de la nouvelle taille du damier
        x_size = int((event.width - 1) / self.n_colonnes)
        y_size = int((event.height - 1) / self.n_lignes)
        self.taille_case = min(x_size, y_size)

        # On efface les cases
        self.canvas.delete("case")
        # On efface la case selected si il y en a une
        self.canvas.delete("selected")

        # On les redessine
        color = self.couleur2
        for row in range(self.n_lignes):
            #Alternance des couleurs
            if color == self.couleur2:
                color = self.couleur1
            else:
                color = self.couleur2

            for col in range(self.n_colonnes):
                x1 = col * self.taille_case
                y1 = row * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="case")

                #Alternance des couleurs
                if color == self.couleur2:
                    color = self.couleur1
                else:
                    color = self.couleur2
        self.ActualiserPieces(False,False)



# Ajouts pour le TP4, idée de base...

class JeuDeDames:
    def __init__(self):
        # On a besoin d'une fenêtre.
        self.fenetre = tk.Tk()
        self.fenetre.title("Jeux de dames de Michel Tremblay et Jean-Francois Paty")
        self.historiqueCharge = []
        self.partieCharge = []
               
        "définition des menus:"
        self.MenuJeu(self.fenetre)
        
        # On a besoin d'une partie.
        self.partie = Partie()

        # On a besoin d'un damier, qu'on placera dans notre fenêtre...
        self.interface_damier = InterfaceDamier(self.fenetre, 64,self.partie.damier)
        self.interface_damier.grid()

        # Affichage du jouer à jouer ainsi que du nombre de pièces que chacun à mangé.
        # Variable à utiliser pour afficher le joueur à jouer :
        # self.etiq_joueur["text"] = ""
        # Variable à utiliser pour afficher le pointage :
        # joueur blanc : self.pointBlanc["text"] = ""
        # joueur noir : self.pointNoir["text"] = ""
        # message au joueur : self.message["text"] = "" ne pas mettre un message trop long ie : vous devez prendre\n un pion (un saut de ligne doit être là pour wrapper le text)
        # historique de jeux : self.historique["text"] = ""   N'aficher que les 15 dernier move ie : blanc : 1,2 -> 2,3\nnoir : 5,4 -> 6,3\n
        self.interface_droite = tk.LabelFrame(self.fenetre, borderwidth=1,relief=RAISED)
        self.interface_droite 
        #Joueur
        self.joueur = tk.LabelFrame(self.interface_droite, borderwidth=1,relief=SUNKEN)
        self.afich_joueur = tk.Label(self.joueur,text="Joueur à jouer:" , width=20)
        self.etiq_joueur = tk.Label(self.joueur,text="", width=20)
        self.afich_joueur.grid()
        self.etiq_joueur.grid()
        self.joueur.grid(row=0,column=0,padx=5,pady=5,sticky="n")
        # Pointage
        self.pointage = tk.LabelFrame(self.interface_droite, borderwidth=1,relief=SUNKEN,text="Pointage")
        self.nomBlanc = tk.Label(self.pointage,text="Blanc: ", width=10)
        self.nomNoir = tk.Label(self.pointage,text="Noir: ",width=10)
        self.pointBlanc = tk.Label(self.pointage,text="0", width=9)
        self.pointNoir = tk.Label(self.pointage,text="0",width=9)
        self.nomBlanc.grid(row=0,column=0)
        self.nomNoir.grid(row=1,column=0)
        self.pointBlanc.grid(row=0,column=1)
        self.pointNoir.grid(row=1,column=1)
        self.pointage.grid(row=1,column=0,padx=5,pady=20)
        # Message
        self.messageframe = tk.LabelFrame(self.interface_droite, borderwidth=1,relief=SUNKEN,text="Message")
        self.message = tk.Label(self.messageframe,text="",width=20)
        self.messageframe.grid(padx=5,pady=15)
        self.message.grid()
        # Historique
        self.historiqueframe = tk.LabelFrame(self.interface_droite, borderwidth=1,relief=SUNKEN,text="Historique")
        self.historique = tk.Text(self.historiqueframe,width=20,height=13)
        self.historiqueframe.grid(sticky="s",padx=5,pady=15)
        self.historique.grid()
        self.scrollbar = tk.Scrollbar(self.historiqueframe,command=self.historique.yview)
        self.scrollbar.grid(row=0,column=1,sticky='nse')
        self.historique['yscrollcommand'] = self.scrollbar.set
        self.etiquettetest = tk.Label(self.interface_droite,text="")
        self.etiquettetest.grid()
        self.interface_droite.grid(row=0,column=1,sticky="ne", padx=5, pady=5)
        self.fenetre.bind("<Button-1>",self.click)

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.fenetre.grid_columnconfigure(0, weight=1)
        self.fenetre.grid_rowconfigure(0, weight=1)

        # Truc pour le redimensionnement automatique des éléments du plateau.
        self.interface_damier.grid_columnconfigure(0, weight=1)
        self.interface_damier.grid_rowconfigure(0, weight=1)


        # Boucle principale.
        self.fenetre.mainloop()

    def getDamierSize(self):
        # Le damier est carré donc on veut juste avoir la plus petite grosseur du damier pour connaitre sa grosseur
        damierwidth = self.interface_damier.winfo_width()
        damierheight = self.interface_damier.winfo_height()
        if damierwidth>damierheight:
            return damierheight-12
        else:
            return damierwidth-12

    def getClickPosition(self, size, event):
        # On trouve dans quel case exactement on click (Coordonnée x,y)
        x =   event.x // (size/8)
        y =   event.y // (size/8)
        return (int(x), int(y))

    def click(self, event):
        # Au click (donc selection d'une piece) on trouve avec le click qu'elle case on a clicker et on "HighLight" cette case
        if event.widget.widgetName == "canvas":
            damierSize = self.getDamierSize()
            damierPosition = self.getClickPosition(damierSize,event)
            if damierPosition[0] < 8 and damierPosition[1] < 8:
                self.interface_damier.selectCase(damierPosition)
                self.etiquettetest["text"] = "({},{},{})".format(event.x,event.y,damierPosition)
            
    def MenuJeu(self, fenetre):
        
        mainmenu = tk.Menu(fenetre)  ## Barre de menu 
        menuPartie = tk.Menu(mainmenu)  ## Menu fils menuExample 
        menuPartie.add_command(label="Nouvelle Partie", command=self.NouveauJeu)
        menuPartie.add_command(label="Charger une Partie", command=self.ChargerJeu)
        menuPartie.add_command(label="Charger une Partie avec historique", command=self.ChargerJeuHistorique)
        menuPartie.add_command(label="Sauvegarder une partie", command=self.SauveJeu)
        menuPartie.add_command(label="Sauvegarder une partie avec historique", command=self.SauveJeuHistorique)
        menuPartie.add_command(label="Quitter", command=fenetre.destroy) 
  
        menuHelp = tk.Menu(mainmenu) ## Menu Fils 
        menuHelp.add_command(label="A propos", command=self.aPropos) 
  
        mainmenu.add_cascade(label = "Partie", menu=menuPartie) 
        mainmenu.add_cascade(label = "Aide", menu=menuHelp)
        fenetre.config(menu = mainmenu)
        
         
    def aPropos(self):
        tk.messagebox.showinfo("A propos", "                     Version 1.0\n                     Conçu par\nJean-Francois Paty et Michel Tremblay")
    
    def NouveauJeu(self):
        #Partie.nouvelle_partie
        self.historique.delete(1.0,END)
        self.interface_damier.ActualiserPieces(True,True)
        self.partie.historique = ""

    def ChargerJeu(self):
        self.partie.historique = ""
        self.historique.delete(1.0,END)
        fileName = filedialog.askopenfile(filetypes=[("Save Games", "*.sav")])
        self.partie.charger(fileName.name)
        self.interface_damier.ActualiserPieces(True,False)

    def ChargerJeuHistorique(self):
        self.partie.historique = ""
        self.historique.delete(1.0,END)
        fileName = filedialog.askopenfile(filetypes=[("Save Games", "*.sav")])
        self.partie.charger(fileName.name)
        self.interface_damier.ActualiserPieces(True,False)
        self.historique.insert(END, self.partie.historique)
        

    def SauveJeu(self):
        """ A Faire JF """
        pass

    def SauveJeuHistorique(self):
        """ A Faire JF """
        pass