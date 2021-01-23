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
        #Création des boutons
        self.quit = tk.Button(self.frm, text='Quitter', #bouton pour quitter
                              command=self.wnd.destroy)
        self.quit.pack(side=tk.RIGHT, pady=5)
        self.start = tk.Button(self.frm, text='Start', command = self.timer)
        self.start.pack(side=tk.LEFT, pady=5) #bouton pour commencer à jouer
        self.sc = tk.Label(self.frm, text = 'Votre score: ', width = 10)
        self.long = tk.Label(self.frm, text = 'Temps:' , width = 10)
        self.attempt = tk.Label(self.frm, text = 'Coups: ' , width = 10)
        #remise à zéro du chrono
        self.sec = 0
        self.chrono = tk.Label(self.frm, text= 'Temps écoulé :' )
        self.chrono.pack(side = tk.LEFT)
        self.nbcoup = 3
        
    def timer(self):      
        """ Méthode permettant le suivi du temps écoulé après le lancement du jeu """
        self.sec += 1
        self.chaine = 'Temps écoulé: ' + str(self.sec)
        self.chrono.after(1000, self.timer)
        self.chrono.config(text = self.chaine)
        self.start.destroy()

    def score(self):
        '''Méthode affichant le score du joueur'''
        if(self.sec == 10):
            self.coup = 'Coups: ' + str(self.sec)
            self.temps = 'Temps: ' + str(self.nbcoup)
            self.attempt.config(text = self.coup)
            self.long.config(text = self.temps)

a = Application(50, 300, 200, 6, 6)
