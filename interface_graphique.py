# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:23:08 2021

@author: hugo
"""

import tkinter as tk
import crop_image
import math

class Application():
    '''Contients des objets correspondant à une fenêtre de jeu'''
    frameHight=200 #Hauteur de la zone de commande
    def __init__(self, margin, pcW, pcH, nPcW, nPcH, image):
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
        #Création des éléments servant pour l'image
        numberTiles = self.nPcW * self.nPcH
        tiles = image.crop(numberTiles)
        listTilesTk =  image.createTilesTk(tiles,self.pcW,self.pcH)
        matTilesTk = [[listTilesTk[i] 
                       for i in range(j,
                                      len(listTilesTk),
                                      int(math.sqrt(len(listTilesTk))))]
                       for j in range(0,int(math.sqrt(len(listTilesTk))))]
        #Création de la zone de commande du jeu
        self.frm = tk.Frame(self.wnd, height = self.frameHight, width = self.width)
        self.frm.pack_propagate(0)
        self.frm.pack(side=tk.BOTTOM, expand = True)
        self.nMove = tk.Label(self.frm, text = "N/A")
        self.nMove.pack()
        #Création des éléments de jeux
        self.objectList=list() #On mémorise les caractéristques de chaque objet du canvas dans cette liste
        self.authorizedPos=list() #On mémorise les emplacements autorisés des objets
        idP=0
        for i in range (self.nPcH):
            for j in range (self.nPcW):
                #Création du plateau
                x, y = i*self.pcW + self.margin, j*self.pcH + self.margin*2
                self.cnv.create_rectangle(x, y, x + self.pcW, y + self.pcH)
                #Sauvegarde les emplacement possibles
                self.authorizedPos.append(PlaceCanvas(x,y,True))
        for i in range (self.nPcH):
            for j in range (self.nPcW):
                #Affichage des images découpés
                xi = self.pcW*(self.nPcW) + self.margin*2 + i*(self.pcW + self.margin/2)
                yi = j*(self.pcH + self.margin/2) + self.margin
                tag="Object"+str(idP)
                self.cnv.create_image(xi + self.pcW/2, yi + self.pcH/2, image = matTilesTk[i][j], tag=tag)
                #Sauvegarde les coordonées du coin supérieur gauche et l'id de l'objet pour déplacement ultérieur
                self.objectList.append(ObjectCanvas(xi, yi, tag, xi, yi, len(self.authorizedPos)))
                #Sauvegarde l'emplacement
                self.authorizedPos.append(PlaceCanvas(xi,yi,False))
                idP+=1
        self.status=0
        self.cnv.bind('<Button-1>',self.clic)
        self.cnv.bind('<B1-Motion>', self.dragClic)
        self.cnv.bind('<ButtonRelease-1>', self.releaseClic)
        self.wnd.mainloop()
        
    '''
    Il existe deux modes de déplacement :
        Mode 1 : L'utilisateur clic une première fois sur un objet puis
        une deuxième fois sur une case vide : l'objet se déplace.
        Mode 2 : L'utlisateur clic sur un objet et le déplace avec sa
        souris jusqu'à l'emplacement voulu. Mode dit "drag and drop".
        
    Les fonctions suivantes se basent sur le principe d'une machine à état
    contrôlée par la variable self.status. Cette dernière, en fonction des
    évènements, peut prendre plusieurs valeurs :
        0 : Le programme est dans l'attente d'un nouveau clic
        1 : Un clic a été détecté sur un objet valide, le programme attend
        la suite des évènements.
        2 : Le clic a été aussitôt relaché, mode de déplacement 1.
        Le programme attend le prochain clic.
        12 : La souris se déplace avec le clic maintenu, le programme
        déplace l'objet sélectionné en temps réel et attend le relachement du
        clic. Mode de déplacement 2.
        
    '''
        
    def clic(self,event):
        '''Si un clic est détecté'''
        if self.status == 0:
            find, self.object = self.isObject(event.x,event.y)
            if find:
                self.status = 1
                return
                
        elif self.status == 2:
            self.finalPos(event.x, event.y)
        
        self.status = 0
    
    def dragClic(self,event):
        '''Si le clic est maintenu et la souris dépalcée'''
        if self.status == 1:    
            self.status = 12
        if self.status == 12:
            self.moveObject(event.x - self.pcW/2, event.y - self.pcH/2)
    
    def releaseClic(self,event):
        '''Si le clic est relaché'''
        if self.status == 1:
            self.status = 2
            
        elif self.status == 12:
            self.status = 0
            self.finalPos(event.x, event.y)
            
    def moveObject(self, x, y):
        '''Déplace l'objet séléctionné dans le canvas'''
        difx = - (self.object.x-x)
        dify = - (self.object.y-y)
        self.object.x = x
        self.object.y = y
        self.cnv.move(self.object.tag, difx, dify)
        
    def finalPos(self, x, y):
        '''Déplace et ajuste si possible l'objet vers sa position finale'''
        valid, place, i = self.validPos(x, y)
        if valid:
            self.adjustPos(place, i)
        else:
            self.returnObject()
    
    def isObject(self, x, y):
        '''Retourne l'objet si le clic a été effectué sur un objet valide. Retourne False sinon'''
        for i in range (len(self.objectList)):
            if (x >= self.objectList[i].x) and (x <= self.objectList[i].x + self.pcW):
                if (y >= self.objectList[i].y) and (y <= self.objectList[i].y + self.pcH):
                    return(True, self.objectList[i])
        return False, None
    
    def validPos(self, x, y):
        '''Retourne true, l'emplcament et son index dans authorizedPos si ce dernier est valide, false sinon'''
        for i in range (len(self.authorizedPos)):
            if (x >= self.authorizedPos[i].x) and (x <= self.authorizedPos[i].x + self.pcW):
                if (y >= self.authorizedPos[i].y) and (y <= self.authorizedPos[i].y + self.pcH):
                    if self.authorizedPos[i].av:
                        return True, self.authorizedPos[i], i
        return False, None, None
        
    def adjustPos(self, place, i):
        '''Ajuste l'objet à la case sur la souris'''
        self.moveObject(place.x, place.y)
        self.authorizedPos[self.object.initPlace].av = True
        self.object.initx, self.object.inity = place.x, place.y
        self.object.initPlace = i
        place.av = False
        
    def returnObject(self):
        '''Retourne l'objet à son emplacement inital (avant déplacement)'''
        self.moveObject(self.object.initx, self.object.inity)
        
class ObjectCanvas():
    '''Contients les caractéristiques d'objets du canvas'''
    def __init__(self, x, y, tag=False, initx=0, inity=0, initPlace=0):
        '''Mémorise les caractéristiques de l'objet :
            x, y : coordonnées du coin supérieur gauche
            initx, inity : coordonnées initiales de l'objet avant déplacement
            initPlace : indice de l'emplacement initial dans le tableau authorizedPos
            tag : tag de l'objet dans le canvas'''
        self.x, self.y, self.tag = x, y, tag
        self.initx, self.inity, self.initPlace = initx, inity, initPlace
        
    def __str__(self):
        '''Affiche les principales coordonnées de l'objet (utile pour debug)'''
        r = str(self.x) + ', ' + str(self.y) + ', tag=' + str(self.tag)
        return r
    
class PlaceCanvas():
    '''Contients des emplacements possible de pièce de jeu sur le canvas'''
    def __init__(self, x, y, availability):
        '''Mémorise les caractéristiques de l'emplacement :
            x, y : coordonnées du coin supérieur gauche
            availability : si l'emplacement est disponible ou occupé par un objet'''
        self.x, self.y, self.av = x, y, availability
    
image = crop_image.ImagePuzzle("images\img_forest.jpg")
boite=Application(50, 100, 100, 5, 5, image)
