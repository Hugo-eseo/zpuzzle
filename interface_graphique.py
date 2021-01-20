# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:29:46 2021

@author: hugob
"""

import tkinter as tk
from operator import itemgetter, attrgetter

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
        self.objectList=list() #On mémorise les caractéristques de chaque objet du canvas dans cette liste
        idP=0
        for i in range (self.nPcH):
            for j in range (self.nPcW):
                #Création du plateau
                x, y = i*self.pcW + self.margin, j*self.pcH + self.margin*2
                self.cnv.create_rectangle(x, y, x + self.pcW, y + self.pcH)
        for i in range (self.nPcH):
            for j in range (self.nPcW):
                #Affichage des images découpés
                xi = self.pcW*self.nPcW + self.margin*2 + i*(self.pcW + self.margin/2)
                yi = j*(self.pcH + self.margin/2) + self.margin
                tag="Object"+str(idP)
                self.cnv.create_rectangle(xi, yi, xi + self.pcW, yi + self.pcH, fill='red', tag=tag)
                #ATTENTION SUITE A MERGE SUR LE MAIN
                #Sauvegarde les coordonées et l'id de l'objet pour déplacement ultérieur
                self.objectList.append(ObjectCanvas(xi, yi, tag))
                idP+=1
        self.cnv.bind('<Button-1>',self.getCords)
        self.cnv.bind('<B1-Motion>', self.moveImage)
        self.cnv.bind('<ButtonRelease-1>', self.test)
        self.wnd.mainloop()
        
    def test(self,event):
        print("Done")
        
    def getCords(self,event):
        '''Mémorise l'objet sélectionné'''
        self.object = self.findObject(event.x,event.y)
        '''for i in range (len(self.objectList)):
            print(self.objectList[i])'''
               
    def moveImage(self, event):
        '''Déplace l'objet séléctionné dans le canvas'''
        if (self.object == False):
            return
        difx = - (self.object.x-event.x)
        dify = - (self.object.y-event.y)
        self.object.x = event.x
        self.object.y = event.y
        self.cnv.move(self.object.tag, difx, dify)
        
    def findObject(self, x, y):
        '''Retourne l'objet si le clic a été effectué sur un objet déplacable. Retourne False sinon'''
        self.objectList.sort(key=lambda e: (e.x, e.y))
        for i in range (len(self.objectList)):
            if (x>=self.objectList[i].x) and (x<=self.objectList[i].x + self.pcW):
                if (y>=self.objectList[i].y) and (y<=self.objectList[i].y + self.pcH):
                    return(self.objectList[i])
        return False
        
class ObjectCanvas():
    '''Contients les caractéristiques d'objets du canvas'''
    def __init__(self, x, y, tag):
        '''Mémorise les caractéristique de l'objet :
            x, y : coordonnée du coin supérieur gauche
            tag : tag de l'objet dans le canvas'''
        self.x, self.y, self.tag = x, y, tag
        
    def __str__(self):
        r = str(self.x) + ', ' + str(self.y) + ', tag=' + str(self.tag)
        return r
        
boite=Application(50, 100, 100, 5, 5)