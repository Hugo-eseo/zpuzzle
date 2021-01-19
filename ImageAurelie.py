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
    
    def display(self, tiles, window, windowWidth, windowHeight):
        self.tiles, self.window = tiles, window
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        numberTiles = len(tiles)
        imgWidth, imgHeight = 45,30
        widthNeeded = numberTiles * imgWidth + imgWidth*1.5+(numberTiles-1)*(imgWidth/2)
        
        numberLines = widthNeeded / 1500
        print(numberLines, type(numberLines))
        if (type(numberLines) != int): 
            numberLines = int(numberLines)+1
        print(numberLines, type(numberLines))
        
        cnvHeight = imgHeight + (numberLines-1)*imgHeight*0.5 + numberLines*imgHeight
        print(cnvHeight)
        cnv = Tk.Canvas(self.window, height=cnvHeight, bg='light grey')
        cnv.pack(side=Tk.TOP, fill = Tk.X)
        
        
        tileTk=list()
        for i in self.tiles : 
            tileTk.append(ImageTk.PhotoImage(i.resize((imgWidth,imgHeight))))
        random.shuffle(tileTk)
            
        x, y = imgWidth*1.5, imgHeight
        for i in range(len(tileTk)):
            if x+imgWidth > self.windowWidth :
                y+= imgHeight*1.5
                x=imgWidth*1.5
            cnv.create_image(x, y, image=tileTk[i])  
            x += imgWidth*1.5
        win.mainloop() 


#####
win = Tk.Tk()
win.geometry("1500x700")
image1 = ImagePuzzle("img_forest.jpg")
image1.printSize()

numberTiles = 49 #la racine carrée doit être un nombre entier
tiles = image1.crop(numberTiles)
print(len(tiles))


image1.display(tiles,win,1500,700)
####

 



    