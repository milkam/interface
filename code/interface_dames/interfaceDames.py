#! /usr/bin/env python
# -*- coding:Utf-8 -*-

import tkinter as tk
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
        
        # Ajout de menu
        mainmenu = tk.Menu(parent)  ## Barre de menu
        menuPartie = tk.Menu(mainmenu)  ## Menu fils menuPartie 
        menuPartie.add_command(label="Nouvelle Partie", command="A FAIRE")  ## Ajout d'une option au menu fils menuFile 
        menuPartie.add_command(label="Charger une Partie", command="A faire")
        menuPartie.add_command(label="Sauvegarder une Partie", command="A faire")
        menuPartie.add_command(label="Quitter", command=parent.quit)  
  
        menuHelp = tk.Menu(mainmenu) ## Menu Fils 
        menuHelp.add_command(label="A propos", command="A faire") 
  
        mainmenu.add_cascade(label = "Partie", menu=menuPartie) 
        mainmenu.add_cascade(label = "Aide", menu=menuHelp)
        parent.config(menu = mainmenu)
        
        # Initialisation du canvas
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=canvas_width, height=canvas_height,
                               background="white")

        # On place le canvas et le plateau (self) à l'aide de "grid".
        self.canvas.grid(padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W) #redim la fenetre 
        self.grid(padx=4, pady=4, sticky=tk.N + tk.S + tk.E + tk.W) # redim le plateau

        # Fait en sorte que le redimensionnement de la fenêtre redimensionne le damier
        self.canvas.bind("<Configure>", self.actualiser)
        
       
        

    def ajouter_piece(self, position, nom_piece):
        """
        Ajoute une pièce sur le damier.
        """

        tempfont = ('Helvetica', self.taille_case//2)
        piece_unicode = caracteres_unicode_pieces[nom_piece[0:2]]

        # On "dessine" la pièce
        ligne, colonne = position
        self.canvas.create_text(ligne, colonne, text=piece_unicode, tags=(nom_piece, "piece"), font=tempfont)

        # On place la pièce dans le canvas (appel de placer_piece)
        self.placer_piece((ligne, colonne), nom_piece)


    def placer_piece(self, position, nom_piece):
        """
        Place une pièce à la position donnée (ligne, colonne).
        """

        ligne, colonne = position

        # Placer les pieces au centre des cases.
        x = (colonne * self.taille_case) + int(self.taille_case / 2)
        y = (ligne * self.taille_case) + int(self.taille_case / 2)

        # On change la taille de la police d'écriture selon la taille actuelle des cases.
        tempfont = ('Helvetica', self.taille_case//2)
        self.canvas.itemconfigure(nom_piece, font=tempfont)

        self.canvas.coords(nom_piece, x, y)


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

        # On redessine les pieces
        for position, piece in self.damier.cases.items():
            self.placer_piece(position, piece.nom)

        # On mets les pieces au dessus des cases
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("case")



# Ajouts pour le TP4, idée de base...

class JeuDeDames:
    def __init__(self):
        # On a besoin d'une fenêtre.
        self.fenetre = tk.Tk()

        # On a besoin d'une partie.
        self.partie = Partie()

        # On a besoin d'un damier, qu'on placera dans notre fenêtre...
        self.interface_damier = InterfaceDamier(self.fenetre, 64,self.partie.damier)
        self.interface_damier.grid()

        # Par contre on aura probablement à modifier la classe InterfaceDamier pour
        # y inclure notre partie! À vous de jouer!
        self.cadre = tk.LabelFrame(self.fenetre, text="cadre")
        self.etiquette_test = tk.Label(self.cadre,text="bonjour", width=20)
        self.etiquette_test.grid()
        self.cadre.grid(row=0,column=1)
        
        self.fenetre.bind("<Button-1>",self.click)



        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.fenetre.grid_columnconfigure(0, weight=1)
        self.fenetre.grid_rowconfigure(0, weight=1)

        # Truc pour le redimensionnement automatique des éléments du plateau.
        self.interface_damier.grid_columnconfigure(0, weight=1)
        self.interface_damier.grid_rowconfigure(0, weight=1)


        # Boucle principale.
        self.fenetre.mainloop()

    def click(self, event):
        
        self.etiquette_test["text"] = "({},{},{})".format(event.x,event.y,event.widget.widgetName)
