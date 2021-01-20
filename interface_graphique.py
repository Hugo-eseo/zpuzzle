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
        self.nbMove.pack(side = tk.RIGHT)
        self.chrono = tk.Label(self.frm, text ='')
        self.chrono.pack(side = tk.LEFT)
        #Création des boutons
        self.quit = tk.Button(self.frm, text='Quitter', 
                              command=self.wnd.destroy)
        self.quit.pack(side=tk.RIGHT, pady=5)
        self.start = tk.Button(self.frm, text='Start',
                               command=self.timer)
        self.start.pack(side=tk.LEFT, pady=5)
        #remise à zéro du chrono
        self.error = False
        self.cpt = 0
        self.wnd.mainloop()
        
    '''Fonction retournant le temps écoulé lors du jeu'''
    def timer(self):
        self.start.destroy()
        if self.error == False:
            self.cpt += 1
        self.chrono.configure(text =('Temps:', self.cpt,'s'))
        
    
       
a = Application(50, 300, 200, 6, 6)