# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:23:40 2021

@author: odial
"""

from PIL import Image

image= Image.open("img_forest.jpg")
ImageSize = image.size #ImageSize = (width, height) de image
#Découpe image : Xgauche = 0, Yhaut = 0, Xdroite = 60, Ybas = 40
ImageCrop = image.crop((0,0,60,40))  


print(image.format, image.size, image.mode)
print (ImageCrop.format,ImageCrop.size,ImageCrop.mode)
#image.show()
#ImageCrop.show()

print(ImageSize[0]/ImageSize[1])

class Photolmage:
    def __init__(self,image):
        self.image = Image.open(image)
    
    def size(self):
        self.size = self.image.size
        self.width = self.size[0]
        self.height = self.size[1]
    
    def printSize(self):
        print(self.size , self.width, self.height)
        
    def crop(self):
        for i in range(10):
            for j in range(10):
                

image1 = Photolmage("img_forest.jpg")
image1.size()
image1.printSize()
