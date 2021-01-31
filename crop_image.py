# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:03:28 2021

@author: Groupe 3 : Aurélie, Tristan et Hugo BOUY
"""

import math
import random
import os
from PIL import Image, ImageTk


class ImagePuzzle():
    '''Prend une image en paramètre et effectue des opérations dessus'''

    def __init__(self, image):
        self.image = Image.open(image)
        self.size = self.image.size
        self.width = self.size[0]
        self.height = self.size[1]

    def print_size(self):
        '''Affiche les dimensions de l'image sous forme (width,height)'''
        print(self.size)

    def crop(self, tiles_number):
        '''
        Découpage de l'image en fonction du nombre de tuiles souhaité
        Retourne une liste des pièces
        '''
        self.tiles_number = tiles_number
        tiles = list()
        '''calcul du nombre de découpages en longueur et en hauteur
        exemple : si on veut 25 tuiles, on découpe 5 fois en longueur
        et 5 fois en hauteur
        comme ça : 5*5 =25 et on a bien le nombre de tuiles souhaité'''
        dim = int(math.sqrt(self.tiles_number))  # int est une sécurité
        for i in range(dim):
            for j in range(dim):
                ''''calcul des coordonnées du rectangle que l'on veut découper
                de l'image'''
                left = i * (self.width // dim)
                top = j * (self.height // dim)
                right = left + self.width // dim
                bottom = top + self.height // dim
                tile = self.image.crop((left, top, right, bottom))
                tiles.append(tile)
        return tiles

    def create_tiles_tk(self, tiles, piece_width, piece_height):
        '''
        Création de la liste d'images de Tkinter en fonction de longueur et
        de la hauteur d'une pièce souhaitée
        self.tiles : liste d'images non converties pour Tkinter
        pieceWidth, pieceHeight : longueur et hauteur souhaitées de chaque
        pièce
        Retourne une liste d'images utilisables dans Tkinter'
        '''
        self.tiles = tiles
        self.piece_width = piece_width
        self.piece_height = piece_height

        tile_tk = list()
        for i in self.tiles:
            ''''resize ne modifie pas l'image si pieceWidth et pieceHeigt
            sont déjà la vraie longueur et la vraie hauteur d'une pièce'''
            tile_tk.append(ImageTk.PhotoImage(i.resize((int(piece_width),
                                                        int(piece_height)))))
        # random.shuffle(tile_tk)  # mélange de l'ordre des pièces
        return tile_tk

    def dominant_color(self):
        '''Trouve la couleur la plus présente dans l'image sélectionnée'''

        '''Création d'une liste pixels qui contient des tuples avec la couleur
        d'un pixel et le nombre de fois que ce pixel apparaît'''
        pixels = self.image.getcolors(self.width * self.height)

        # Trouver la couleur qui revient le plus et la retourner
        self.dominant_color = pixels[0]
        for number, color in pixels:
            if number > self.dominant_color[0]:
                self.dominant_color = color
        return self.dominant_color
    

def image_choice(folder):
    list_images = os.listdir(folder)
    return random.choice(list_images)
