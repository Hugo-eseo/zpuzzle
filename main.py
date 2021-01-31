# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:00:40 2021

@author: hugob
"""

#Ceci est le main
import tkinter as tk
import math
import os
from PIL import Image, ImageTk

import interface_graphique_v2

import crop_image

class Welcome():
    def __init__(self, folder):
        self.folder = folder
        self.win = tk.Tk()
        self.win.title("Welcome")
        self.win.geometry("1000x400")
        self.win.resizable(width=False, height=False)
        self.frm_left = tk.Frame(self.win, height=800,width=250, bg='white')
        self.frm_left.pack(side=tk.LEFT)
        
        self.cnv_middle = tk.Canvas(self.win,height=800, width=500, bg='white',
                                    bd=0, highlightthickness=0, relief='ridge')
        self.cnv_middle.pack(side=tk.LEFT)
        
        self.frm_right = tk.Canvas(self.win,height=800,width=250, bg='white',
                                   bd=0, highlightthickness=0, relief='ridge')
        self.frm_right.pack(side=tk.RIGHT)
        self.list_images = os.listdir(self.folder)
        
        self.num_image = 0
        self.image = Image.open("images\\" + self.list_images[0])
        self.ratio_wh = self.image.size[0]/self.image.size[1]
        self.image = self.image.resize((int(300*self.ratio_wh),300))
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.tag='image' + str(self.num_image)
        
        self.cnv_middle.create_image(1000/4, 400/2,
                                     image = self.image_tk, tag=self.tag)
        
        self.next = tk.Button(self.frm_right, text='Image suivante',
                              command=self.next_image) 
        self.next.place(x=75, y=190)
        self.previous = tk.Button(self.frm_left, text='Image précédente',
                              command=self.previous_image) 
        self.previous.place(x=75, y=190)
        self.beginning = tk.Button(self.frm_left,
                                   text='Retourner à la première image',
                                   command=self.first_image)
        self.beginning.place(x=75,y=230)
        self.begin_game = tk.Button(self.cnv_middle, text='Jouer avec cette image',
                              command=self.begin_game)
        self.begin_game.place(x=150,y=360)
        self.win.mainloop()
        
    def next_image(self):
        '''Oui'''
        if (self.num_image == len(self.list_images)-1):
            return
        self.cnv_middle.delete(self.tag)
        self.num_image += 1
        self.image = Image.open("images\\" + self.list_images[self.num_image])
        self.ratio_wh = self.image.size[0]/self.image.size[1]
        self.image = self.image.resize((int(300*self.ratio_wh),300))
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.tag='image' + str(self.num_image)
        self.cnv_middle.create_image(1000/4, 400/2,
                                     image = self.image_tk, tag=self.tag)
        print(self.num_image)
        
    def previous_image(self):
        '''Oui'''
        if (self.num_image == 0):
            return
        self.cnv_middle.delete(self.tag)
        self.num_image -= 1
        self.image = Image.open("images\\" + self.list_images[self.num_image])
        self.ratio_wh = self.image.size[0]/self.image.size[1]
        self.image = self.image.resize((int(300*self.ratio_wh),300))
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.tag='image' + str(self.num_image)
        self.cnv_middle.create_image(1000/4, 400/2,
                                     image = self.image_tk, tag=self.tag)
        print(self.num_image)
        
    def first_image(self):
        self.cnv_middle.delete(self.tag)
        self.num_image = 0
        self.image = Image.open("images\\" + self.list_images[self.num_image])
        self.ratio_wh = self.image.size[0]/self.image.size[1]
        self.image = self.image.resize((int(300*self.ratio_wh),300))
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.tag='image' + str(self.num_image)
        self.cnv_middle.create_image(1000/4, 400/2,
                                     image = self.image_tk, tag=self.tag)
        print(self.num_image)
        
    def begin_game(self):
        global ratio_wh
        self.win.destroy()
        image_chosen = self.list_images[self.num_image]
        image = crop_image.ImagePuzzle("images\\" + str(image_chosen))
        print("images\\" + str(image_chosen))
        ratio_wh = image.width/image.height
        #print(ratio_wh)
        interface_graphique_v2.Application(40, 70*ratio_wh, 70, 5, 5, image)
        
        