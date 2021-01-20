# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:29:46 2021

@author: hugob
"""

import tkinter as tk

class Application():
    '''Contients des objets correspondant à une fenêtre de jeu'''
    frameHight=200 #Hauteur de la zone de commande
    def __init__(self, margin, pcW, pcH, nPcW, nPcH):
        '''Crée une fenêtre tkinter. Prend en paramètres :
            margin : marge autour du puzzle
            pcW : largueur de la pièce
            pcH : hauteur de la pièce
            nPcW : nombre de pièces en largeur
            nPcH : nombre de pièces en hauteur'''
        #Mémorisation des paramètres
        self.margin, self.pcW, self.pcH = margin, pcW, pcH
        self.nPcW, self.nPcH = nPcW, nPcH
        '''Width et height : Largeur et hauteur du canvas'''
        self.width = self.pcW*self.nPcW*2 + self.margin/2*(self.nPcW + 5)
        self.height = self.pcH*self.nPcH + self.margin*4
        #Création de la fenêtre
        self.wnd = tk.Tk()
        self.wnd.title("ZPuzzle")
        #Création de la zone de dessin
        self.cnv = tk.Canvas(self.wnd, width = self.width, height = self.height, 
            bg='white')
        self.cnv.pack(side = tk.TOP)
        #Création de la zone de commande du jeu
        self.frm = tk.Frame(self.wnd, height = self.frameHight, width = self.width)
        self.frm.pack_propagate(0)
        self.frm.pack(side=tk.BOTTOM, expand = True)
        self.nMove = tk.Label(self.frm, text = "N/A")
        self.nMove.pack()
        #Création des éléments de jeux
        for i in range (self.nPcH):
            for j in range (self.nPcW):
                #Création du plateau
                x, y = i*self.pcW + self.margin, j*self.pcH + self.margin*2
                self.cnv.create_rectangle(x, y, x + self.pcW, y + self.pcH)
                #Affichage des images découpés
                xi = self.pcW*self.nPcW + self.margin*2 + i*(self.pcW + self.margin/2)
                yi = j*(self.pcH + self.margin/2) + self.margin
                self.cnv.create_rectangle(xi, yi, xi + self.pcW, yi + self.pcH, fill='red')
        self.wnd.mainloop()
        
boite=Application(50, 100, 100, 5, 5)