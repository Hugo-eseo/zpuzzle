# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:03:28 2021

@author: odial
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:29:46 2021
@author: hugob
"""

import tkinter as tk
from PIL import Image, ImageTk
import math
import random


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
                #A MERGE :
                self.authorizedPos.append(ObjectCanvas(x,y,True))
        for i in range (self.nPcH):
            for j in range (self.nPcW):
                #Affichage des images découpés
                xi = self.pcW*self.nPcW + self.margin*2 + i*(self.pcW + self.margin/2)
                yi = j*(self.pcH + self.margin/2) + self.margin
                tag="Object"+str(idP)
                self.cnv.create_image(xi,yi, image = matTilesTk[i][j], tag=tag, anchor ='nw') 
                #ATTENTION SUITE A MERGE SUR LE MAIN
                #Sauvegarde les coordonées et l'id de l'objet pour déplacement ultérieur
                self.objectList.append(ObjectCanvas(xi, yi, tag))
                self.authorizedPos.append(ObjectCanvas(xi,yi,False))
                idP+=1
                #TEST
                self.isClic=False
        self.cnv.bind('<Button-1>',self.getCords)
        self.cnv.bind('<B1-Motion>', self.dragObject)
        self.cnv.bind('<ButtonRelease-1>', self.posObject)
        self.wnd.mainloop()
        
    def posObject(self,event):
        '''Une fois le clic utilisateur relaché, positionne l'objet sur un emplacement autorisé'''
        if (self.object == False):
            return
        if self.isClic:
            return
        for i in range (len(self.authorizedPos)):
            if (event.x >= self.authorizedPos[i].x) and (event.x <= self.authorizedPos[i].x + self.pcW):
                if (event.y >= self.authorizedPos[i].y) and (event.y <= self.authorizedPos[i].y + self.pcH):
                    if not self.authorizedPos[i].tag:
                        break
                    #Si un la souris est sûr un emplacement autorisé, on ajuste la position de l'objet
                    self.moveObject(self.authorizedPos[i].x, self.authorizedPos[i].y)
                    self.authorizedPos[i].tag=False
                    return
        #Sinon l'objet retrouve sa position initiale.
        self.moveObject(self.initPos.x, self.initPos.y)
        self.initPos.tag = False
        
    def dragObject(self,event):
        if (self.object == False):
            return
        self.isClic=False
        self.moveObject(event.x, event.y)
        self.initPos.tag = True
        
        
    def getCords(self,event):
        '''Mémorise l'objet sélectionné'''
        if self.isClic:
            for i in range (len(self.authorizedPos)):
                if (event.x >= self.authorizedPos[i].x) and (event.x <= self.authorizedPos[i].x + self.pcW):
                    if (event.y >= self.authorizedPos[i].y) and (event.y <= self.authorizedPos[i].y + self.pcH):
                        if not self.authorizedPos[i].tag:
                            break
                        #Si un la souris est sûr un emplacement autorisé, on ajuste la position de l'objet
                        self.moveObject(self.authorizedPos[i].x, self.authorizedPos[i].y)
                        self.authorizedPos[i].tag=False
                        self.initPos.tag = True
                        return
        self.object,self.initPos = self.findObject(event.x,event.y)
        '''for i in range (len(self.objectList)):
            print(self.objectList[i])'''
               
    def moveObject(self, x, y):
        '''Déplace l'objet séléctionné dans le canvas'''
        difx = - (self.object.x-x)
        dify = - (self.object.y-y)
        self.object.x = x
        self.object.y = y
        self.cnv.move(self.object.tag, difx, dify)
        
    def findObject(self, x, y):
        '''Retourne l'objet et sa position si le clic a été effectué sur un objet déplacable. Retourne False sinon'''
        for i in range (len(self.objectList)):
            if (x >= self.objectList[i].x) and (x <= self.objectList[i].x + self.pcW):
                if (y >= self.objectList[i].y) and (y <= self.objectList[i].y + self.pcH):
                    for j in range (len(self.authorizedPos)):
                        if (x >= self.authorizedPos[j].x) and (x <= self.authorizedPos[j].x + self.pcW):
                            if (y >= self.authorizedPos[j].y) and (y <= self.authorizedPos[j].y + self.pcH):
                                self.isClic=True
                                return(self.objectList[i], self.authorizedPos[j])
        return False, False
        
class ObjectCanvas():
    '''Contients les caractéristiques d'objets du canvas'''
    def __init__(self, x, y, tag=False):
        '''Mémorise les caractéristiques de l'objet :
            x, y : coordonnées du coin supérieur gauche
            tag : tag de l'objet dans le canvas'''
        self.x, self.y, self.tag = x, y, tag
        
    def __str__(self):
        r = str(self.x) + ', ' + str(self.y) + ', tag=' + str(self.tag)
        return r
    
    
class ImagePuzzle:
    def __init__(self,image):
        '''
        Initiatilisation :
        self.image : image voulue
        self.size : tuple : (width,height)
        self.wdith : longueur de l'image
        self.height : hauteur de l'image
        '''
        self.image = Image.open(image)
        self.size = self.image.size
        self.width = self.size[0]
        self.height = self.size[1]
    
    def printSize(self):
        '''Affiche les dimensions de l'image sous forme (width,height)'''
        print(self.size)
    def crop(self,tilesNumber):
        '''
        Découpage de l'image en fonction du nombre de tuiles souhaité
        Retourne une liste des pièces
        '''
        self.tilesNumber = tilesNumber
        tiles = list()
        #calcul du nombre de découpages en longueur et en hauteur
        #exemple : si on veut 25 tuiles, on découpe 5 fois en longueur
        #et 5 fois en hauteur
        #comme ça : 5*5 =25 et on a bien le nombre de tuiles souhaité
        dim = int(math.sqrt(self.tilesNumber)) #int est une sécurité
        for i in range(dim):
            for j in range(dim):
                #calcul des coordonnées du rectangle que l'on veut découper
                #de l'image
                left = i * (self.width // dim)
                top = j * (self.height // dim)
                right = left + self.width // dim 
                bottom = top + self.height // dim
                tile = self.image.crop((left, top, right, bottom))
                tiles.append(tile)
        return tiles
    
    def createTilesTk(self, tiles, pieceWidth, pieceHeight):
        '''
        Création de la liste d'images de Tkinter en fonction de longueur et
        de la hauteur d'une pièce souhaitée
        self.tiles : liste d'image non converties pour Tkinter
        pieceWidth, pieceHeight : longueur et hauteur souhaitées de chaque 
        pièce
        Retourne une liste d'images utilisables dans Tkinter'
        '''
        self.tiles = tiles
        self.pieceWidth = pieceWidth
        self.pieceHeight = pieceHeight
        
        tileTk=list()
        for i in self.tiles : 
            #resize ne modifie pas l'image si pieceWidth et pieceHeigt
            #sont déjà la vraie longueur et la vraie hauteur d'une pièce
            tileTk.append(ImageTk.PhotoImage(i.resize((pieceWidth,pieceHeight))))
        random.shuffle(tileTk) #mélange de l'ordre des pièces
        return tileTk
    
    
image = ImagePuzzle("img_forest.jpg")
boite=Application(50, 100, 100, 5, 5, image)