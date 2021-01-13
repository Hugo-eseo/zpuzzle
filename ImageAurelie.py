# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:23:40 2021

@author: odial
"""

from PIL import Image
import math

image= Image.open("img_forest.jpg")
ImageSize = image.size #ImageSize = (width, height) de image
#Découpe image : Xgauche = 0, Yhaut = 0, Xdroite = 60, Ybas = 40
ImageCrop = image.crop((0,0,60,40))  


print(image.format, image.size, image.mode)
print (ImageCrop.format,ImageCrop.size,ImageCrop.mode)
image.show()
#ImageCrop.show()

print(ImageSize[0]/ImageSize[1])

class Photolmage:
    def __init__(self,image):
        self.image = Image.open(image)
        self.size = self.image.size
        self.width = self.size[0]
        self.height = self.size[1]
    
    def printSize(self):
        print(self.size , self.width, self.height)
        
    def crop(self):
    def crop(self,TilesNumber):
        self.TilesNumber = TilesNumber
        tiles = list()
#        coord = list()
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

image1 = Photolmage("img_forest.jpg") 
#image1 = Photolmage("ImageMario.png")
image1.printSize()
image1.crop(100)
