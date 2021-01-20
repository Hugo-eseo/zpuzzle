# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:23:40 2021

@author: odial
"""

from PIL import Image, ImageTk
import tkinter as Tk
import math
import random

class ImagePuzzle:
    def __init__(self,image):
        '''Initiatilisation :
        self.image : image voulue
        self.size : tuple : (width,height)
        '''
        self.image = Image.open(image)
        self.size = self.image.size
        self.width = self.size[0]
        self.height = self.size[1]
    
    def printSize(self):
        print(self.size, self.width, self.height)
        
    def crop(self,TilesNumber):
        self.TilesNumber = TilesNumber
        tiles = list()
        for i in range(int(math.sqrt(TilesNumber))):
            for j in range(int(math.sqrt(TilesNumber))):
                left = i * (self.width // math.sqrt(TilesNumber))
                top = j * self.height // math.sqrt(TilesNumber)
                right = left + self.width // math.sqrt(TilesNumber) 
                bottom = top + self.height // math.sqrt(TilesNumber)
                tile = self.image.crop((left, top, right, bottom))
                tiles.append(tile)
#                coord.append((left, top, right, bottom))
#        tiles[0].show()
#        tiles[99].show()
#        print(coord)
        return tiles
    
    def display(self, tiles, window, windowWidth, windowHeight, pieceWidth, pieceHeight):
        self.tiles, self.window = tiles, window
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.pieceWidth = pieceWidth
        self.pieceHeight = pieceHeight
        numberTiles = len(tiles)
        #pieceWidth, pieceHeight = self.width//math.sqrt(numberTiles), self.height//math.sqrt(numberTiles)
        widthNeeded = numberTiles * pieceWidth + pieceWidth*1.5+(numberTiles-1)*(pieceWidth/2)
        
        numberLines = widthNeeded / 1500
        if (type(numberLines) != int): 
            numberLines = int(numberLines)+1
        
        cnvHeight = pieceHeight + (numberLines-1)*pieceHeight*0.5 + numberLines*pieceHeight
        cnv = Tk.Canvas(self.window, height=cnvHeight, bg='light grey')
        cnv.pack(side=Tk.TOP, fill = Tk.X)
        
        tileTk=list()
        for i in self.tiles : 
            tileTk.append(ImageTk.PhotoImage(i.resize((pieceWidth,pieceHeight))))
        random.shuffle(tileTk)
            
        x, y = pieceWidth*1.5, pieceHeight
        nbt = 1
        for i in range(len(tileTk)):
            if x+pieceWidth > self.windowWidth :
                y+= pieceHeight*1.5
                x=pieceWidth*1.5
            tagt = 'tile' + str(nbt)
            cnv.create_image(x, y, image=tileTk[i], tag = tagt)  
            x += pieceWidth*1.5
            nbt += 1
        win.mainloop() 


#####
win = Tk.Tk()
win.geometry("1500x700")
image1 = ImagePuzzle("img2.jpg")
numberTiles = 25 #la racine carrée doit être un nombre entier
#pieceWidth, pieceHeight = 45,30
pieceWidth = image1.width//math.sqrt(numberTiles)
pieceHeight = image1.height//math.sqrt(numberTiles)

image1.printSize()

tiles = image1.crop(numberTiles)
print(len(tiles))
print(pieceWidth,pieceHeight)

image1.display(tiles,win,1500,700,pieceWidth,pieceHeight)
####

 



    