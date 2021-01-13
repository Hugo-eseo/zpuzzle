# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:29:46 2021

@author: hugob
"""

import tkinter as tk

class Application():
    '''Contients des objets correspondant à une fenêtre de jeu'''
    def __init__(self, margin, pctW, pctH, nPieceW, nPieceH):
        '''Crée une fenêtre tkinter. Prend en paramètres :
            margin : marge autour du puzzle
            pctW : largueur de l'image
            pctH : hauteur de l'image
            nPieceW : nombre de pièces en largeur
            nPieceH : nombre de pièces en hauteur'''
        #Mémorisation des paramètres
        self.margin, self.pctW, self.pctH = margin, pctW, pctH
        self.width = self.pctW*2 + margin*(nPieceW+2)
        self.height = self.pctH + margin*2
        #Création de la fenêtre
        self.wnd = tk.Tk()
        self.wnd.title("ZPuzzle")
        #Création de la zone de dessin
        self.cnv = tk.Canvas(self.wnd, width = self.width, height = self.height, 
            bg='white')
        self.cnv.pack(side = tk.TOP)
        #Création de la zone de commande du jeu
        self.frm = tk.Frame(self.wnd, height = 200, width = self.width)
        self.frm.pack_propagate(0)
        self.frm.pack(side=tk.BOTTOM, expand = True)
        self.nMove = tk.Label(self.frm, text = "N/A")
        self.nMove.pack()
        self.wnd.mainloop()
        
boite=Application(50, 500, 500, 5, 5)