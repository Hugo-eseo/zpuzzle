# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:20:53 2021

@author: Tristan
"""

import tkinter as tk

class Application():
    '''Créer une fenêtre de l'application avec ses paramètres
        margin: marge de la fenêtre
        pctW: longueur de l'image
        pctH: largeur de l'image
        piecesW: nombre de pièces en longueur
        piecesH: nombre de pièces en largeur'''
    def __init__(self, margin, pctW, pctH, piecesW, piecesH):
        #Mémorisation des paramètres
        self.margin, self.pctW, self.pctH = margin, pctW, pctH
        self.width, self.height = 2*pctW + margin*(piecesW +2), pctH + margin
        #la fenêtre de l'application
        self.wnd = tk.Tk()
        self.wnd.title('Puzzle')
        self.cnv = tk.Canvas(self.wnd, width = self.width, height = self.height
                             , bg='white')
        self.cnv.pack(side=tk.TOP)
        #Création de la frame contenant le score, le niveau, ...
        self.frm = tk.Frame(self.wnd, width = self.width, height = 150)
        self.frm.pack(side=tk.BOTTOM)
        self.nbMove = tk.Label(self.frm, text='A déterminer')
        self.nbMove.pack()
        self.wnd.mainloop()
        
    def planche():
        self.x=x
        self
    
a = Application(50, 300, 200, 6, 6)
        
        
        