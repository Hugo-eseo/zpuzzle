# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:03:28 2021

@author: Groupe 3 : Aurélie, Tristan et Hugo BOUY
"""

from PIL import Image, ImageTk
import math
#import random
    
    
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
        #random.shuffle(tileTk) #mélange de l'ordre des pièces
        return tileTk
    
    