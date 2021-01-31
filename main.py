# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:00:40 2021

@author: hugob
"""

import tkinter as tk
import os
from PIL import Image, ImageTk

import crop_image
import interface_graphique_v2


class SelectImage():
    '''Fenêtre d'accueil permettant de choisir l'image à reconstituer'''

    def __init__(self, folder):
        # Mémorisation du fichier
        self.folder = folder

        # Création de la fenêtre Tkinter et de ses éléments (canva, frames)
        self.win = tk.Tk()
        self.win.title("Selection de l'image")
        self.win.geometry("1000x400")
        self.win.resizable(width=False, height=False)  # Pas de fullscreen

        self.frm_left = tk.Frame(self.win, height=800, width=250, bg="white")
        self.frm_left.pack(side=tk.LEFT)

        self.cnv_middle = tk.Canvas(self.win, height=800, width=500,
                                    bg="white", bd=0,
                                    highlightthickness=0, relief='ridge')
        self.cnv_middle.pack(side=tk.LEFT)

        self.frm_right = tk.Canvas(self.win, height=800, width=250, bg="white",
                                   bd=0, highlightthickness=0, relief="ridge")
        self.frm_right.pack(side=tk.RIGHT)

        # Création de la liste des images du fichier
        self.list_images = os.listdir(self.folder)

        # Affichage de la première image du dossier selectionné
        self.num_image = 0
        self.image = Image.open("images\\" + self.list_images[0])
        self.ratio_wh = self.image.size[0]/self.image.size[1]
        self.image = self.image.resize((int(300*self.ratio_wh), 300))
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.tag = 'image' + str(self.num_image)

        self.cnv_middle.create_image(1000/4, 400/2,
                                     image=self.image_tk, tag=self.tag)

        # Création des boutons
        self.next = tk.Button(self.frm_right, text='Image suivante',
                              command=self.next_image)
        self.next.place(x=75, y=190)
        tk.Button(self.frm_left, text='Image précédente',
                  command=self.previous_image).place(x=75, y=190)
        tk.Button(self.frm_left, text='Retourner à la première image',
                  command=self.first_image).place(x=75, y=230)
        tk.Button(self.cnv_middle, text='Jouer avec cette image',
                  command=self.begin_game).place(x=180, y=360)

    def display(self):
        '''Fonction qui sert pour les trois à venir, ouvre l'image, la met à
        la taille souhaitée, la convertie pour être utilisable par Tkinter,
        et l'affiche dans le canvas central en mémorisant son tag'''
        self.image = Image.open("images\\" + self.list_images[self.num_image])
        self.ratio_wh = self.image.size[0]/self.image.size[1]
        self.image = self.image.resize((int(300*self.ratio_wh), 300))
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.tag = 'image' + str(self.num_image)
        self.cnv_middle.create_image(1000/4, 400/2,
                                     image=self.image_tk, tag=self.tag)

    def next_image(self):
        '''Affiche l'image suivante dans le dossier
        Si c'est la dernière image qui est affichée, la fonction ne fait rien
        '''
        if self.num_image == len(self.list_images)-1:
            return
        self.cnv_middle.delete(self.tag)
        self.num_image += 1
        self.display()

    def previous_image(self):
        '''Affiche l'image précédente dans le dossier
        Si c'est la premoère image qui est affichée, la fonction ne fait rien
        '''
        if self.num_image == 0:
            return
        self.cnv_middle.delete(self.tag)
        self.num_image -= 1
        self.display()

    def first_image(self):
        '''Retourne au début de la liste d'images'''
        self.cnv_middle.delete(self.tag)
        self.num_image = 0
        self.display()

    def begin_game(self):
        '''Lance le jeu avec l'image affichée à l'écran'''
        self.win.destroy()
        image_chosen = self.list_images[self.num_image]
        image = crop_image.ImagePuzzle("images\\" + str(image_chosen))
        ratio_wh = image.width/image.height
        interface_graphique_v2.Application(5, 5, image, ratio_wh)


SelectImage("images")
