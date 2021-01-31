# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:23:08 2021
@author: Groupe 3 : Aurélie, Tristan et Hugo BOUY
"""

import tkinter as tk
import math
import os
from PIL import Image, ImageTk

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
        Application(40, 70*ratio_wh, 70, 5, 5, image)
    

        
class Application():
    '''Contients des objets correspondant à une fenêtre de jeu'''

    frameHight=200 #Hauteur de la zone de commande

    def __init__(self, margin, pc_w, pc_h, n_pc_w, n_pc_h, image):
        '''Crée une fenêtre tkinter. Prend en paramètres :
            margin : marge autour du puzzle
            pc_w : largueur de la pièce
            pc_h : hauteur de la pièce
            n_pc_w : nombre de pièces en largeur
            n_pc_h : nombre de pièces en hauteur'''

        #Mémorisation des paramètres
        self.margin, self.pc_w, self.pc_h = margin, pc_w, pc_h
        self.n_pc_w, self.n_pc_h = n_pc_w, n_pc_h
        self.image = image
        #Width et height : Largeur et hauteur du canvas
        self.width = self.pc_w*self.n_pc_w*2 + self.margin/2*(self.n_pc_w + 5)
        self.height = self.pc_h*self.n_pc_h + self.margin*4

        #Création de la fenêtre
        self.wnd = tk.Tk()
        self.wnd.title("ZPuzzle")

        #Création de la zone de dessin
        self.cnv = tk.Canvas(self.wnd, width = self.width,
                            height = self.height, bg='white')
        self.cnv.pack(side = tk.TOP)

        #Création des éléments servant pour l'image
        number_tiles = self.n_pc_w * self.n_pc_h
        tiles = self.image.crop(number_tiles)
        list_tiles_tk =  self.image.create_tiles_tk(tiles,self.pc_w,self.pc_h)
        mat_tiles_tk = [[list_tiles_tk[i]
            for i in range(j, len(list_tiles_tk),
                int(math.sqrt(len(list_tiles_tk))))]
            for j in range(0,int(math.sqrt(len(list_tiles_tk))))]

        #Création de la zone de commande du jeu
        self.frm = tk.Frame(self.wnd, height = self.frameHight,
            width = self.width, bg='white')
        self.frm.pack_propagate(0)
        self.frm.pack(side=tk.BOTTOM, expand = True)
        
        #Création de la fenêtre de réussite et de ses éléments
        self.frmr = tk.Frame(self.wnd, height = (self.frameHight)/2, 
                            width = (self.width)/2, bg='white')
        self.total_attempt = tk.Label(self.frmr, text = 'Déplacements totaux: '
                                      ,width = 10)

        #Création des boutons
        self.quit = tk.Button(self.frm, text='Quitter', #Bouton pour quitter
                              command=self.wnd.destroy) 
        self.quit.pack(side=tk.RIGHT, pady=5, padx=5)
        self.start = tk.Button(self.frm, text='Start', command = self.timer)
        self.start.pack(side=tk.TOP, pady=5, padx=5) #Bouton pour commencer à jouer
        self.first_level = tk.Button(self.frm, text = 'Niveau 1',
                                     command = self.first_level)
        self.first_level.pack(side = tk.LEFT, anchor = 'nw', padx=3)
        self.second_level = tk.Button(self.frm, text='Niveau 2',
                                      command = self.second_level)
        self.second_level.pack(side = tk.LEFT, anchor = 'nw', padx= 3)
        self.third_level = tk.Button(self.frm, text = 'Niveau 3',
                                     command = self.third_level)
        self.third_level.pack(side = tk.LEFT, anchor = 'nw', padx = 3)
        self.change_image = tk.Button(self.frm, text="Changer d'image",
                                      command = self.change_image)
        self.change_image.pack(side=tk.LEFT, anchor='nw')
        self.sc = tk.Label(self.frm, text = 'Votre score: ', width = 10)
        self.sc.pack(side=tk.LEFT, pady=5, padx=5)
        self.attempt = tk.Label(self.frm, text = 'Coups: ' , width = 20)
        self.attempt.pack(side=tk.LEFT, pady=5, padx=5)
        self.chrono = tk.Label(self.frm, text= 'Temps écoulé :', width = 10)
        self.chrono.pack(side = tk.LEFT, anchor='center', pady=5, padx=5)
        
        #remise à zéro du chrono
        self.sec = 0
        self.nb_coup = 3
        self.score()
        self.win()

        #Création des éléments de jeux
        #On mémorise les caractéristques de chaque objet déplacable du canvas
        self.object_list=list()
        #On mémorise les emplacements autorisés des objets
        self.authorized_pos=list()
        id_p=0
        for i in range (self.n_pc_h):
            for j in range (self.n_pc_w):
                #Création du plateau
                x, y = i*self.pc_w + self.margin, j*self.pc_h + self.margin*2
                self.cnv.create_rectangle(x, y, x + self.pc_w, y + self.pc_h)
                #Sauvegarde les emplacement possibles
                self.authorized_pos.append(PlaceCanvas(x,y,True))
        for i in range (self.n_pc_h):
            for j in range (self.n_pc_w):
                #Affichage des images découpés
                xi = self.pc_w*(self.n_pc_w) + self.margin*2 + \
                                      i*(self.pc_w + self.margin/2)
                yi = j*(self.pc_h + self.margin/2) + self.margin
                tag="Object"+str(id_p)
                self.cnv.create_image(xi + self.pc_w/2, yi + self.pc_h/2,
                    image = mat_tiles_tk[i][j], tag=tag)
                #Sauvegarde les coordonées du coin supérieur gauche et
                #l'id de l'objet pour déplacement ultérieur
                self.object_list.append(ObjectCanvas(xi, yi, xi, yi,
                    len(self.authorized_pos), tag))
                #Sauvegarde l'emplacement
                self.authorized_pos.append(PlaceCanvas(xi,yi,False))
                id_p+=1

        self.status=0
        self.cnv.bind('<Button-1>',self.clic)
        self.cnv.bind('<B1-Motion>', self.drag_clic)
        self.cnv.bind('<ButtonRelease-1>', self.release_clic)
        self.wnd.mainloop()

    def timer(self):
        """ Méthode permettant le suivi du temps écoulé après le lancement
        du jeu """
        self.sec += 1
        self.chaine = 'Temps écoulé: ' + str(self.sec) +'s'
        self.chrono.after(1000, self.timer)
        self.chrono.config(text = self.chaine)
        self.start.destroy()
    
    def score(self):
        '''Méthode affichant le score du joueur'''
        self.coup = 'Déplacements: ' + str(self.nb_coup)
        self.attempt.config(text = self.coup)
    
    def win(self):
        self.frmr.pack(side=tk.TOP)
        self.total_attempt.config(text = 'Déplacements totaux:' + 
                                  str(self.nb_coup))
        self.total_attempt.pack(side=tk.TOP)
    
    def first_level(self):
        '''Oui'''
        self.wnd.destroy()
        Application(40, 70*ratio_wh, 70, 5, 5, self.image)
    def second_level(self):
        '''Oui'''
        self.wnd.destroy()
        Application(50, 60*ratio_wh, 60, 6, 6, self.image)

    def third_level(self):
        '''Oui'''
        self.wnd.destroy()
        Application(35, 60*ratio_wh, 60, 7, 7, self.image)
    def change_image(self):
        '''Oui'''
        self.wnd.destroy()
        chosen_image = crop_image.image_choice("images")
        image = crop_image.ImagePuzzle("images\\" + str(chosen_image))
        ratio_wh = image.width/image.height
        boite=Application(40, 70*ratio_wh, 70, 5, 5, image)


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
            find, self.object = self.is_object(event.x,event.y)
            if find:
                self.status = 1
                return

        elif self.status == 2:
            self.final_pos(event.x, event.y)

        self.status = 0

    def drag_clic(self, event):
        '''Si le clic est maintenu et la souris dépalcée'''
        if self.status == 1:
            self.status = 12
        if self.status == 12:
            self.move_object(event.x - self.pc_w/2, event.y - self.pc_h/2)

    def release_clic(self, event):
        '''Si le clic est relaché'''
        if self.status == 1:
            self.status = 2

        elif self.status == 12:
            self.status = 0
            self.final_pos(event.x, event.y)

    def move_object(self, x, y):
        '''Déplace l'objet séléctionné dans le canvas'''
        difx = - (self.object.x-x)
        dify = - (self.object.y-y)
        self.object.x = x
        self.object.y = y
        self.cnv.move(self.object.tag, difx, dify)

    def final_pos(self, x, y):
        '''Déplace et ajuste si possible l'objet vers sa position finale'''
        valid, place, i = self.valid_pos(x, y)
        if valid:
            self.adjust_pos(place, i)
        else:
            self.return_object()

    def is_object(self, x, y):
        '''Retourne l'objet si le clic a été effectué sur un objet valide.
        Retourne False sinon'''
        for i in range (len(self.object_list)):
            if (x >= self.object_list[i].x) and \
                (x <= self.object_list[i].x + self.pc_w):
                if (y >= self.object_list[i].y) and \
                    (y <= self.object_list[i].y + self.pc_h):
                    return(True, self.object_list[i])
        return False, None

    def valid_pos(self, x, y):
        '''Retourne true, l'emplcament et son index dans authorizedPos
        si ce dernier est valide, false sinon'''
        for i in range (len(self.authorized_pos)):
            if (x >= self.authorized_pos[i].x) and \
                (x <= self.authorized_pos[i].x + self.pc_w):
                if (y >= self.authorized_pos[i].y) and \
                    (y <= self.authorized_pos[i].y + self.pc_h):
                    if self.authorized_pos[i].av:
                        return True, self.authorized_pos[i], i
        return False, None, None

    def adjust_pos(self, place, i):
        '''Ajuste l'objet à la case sur la souris'''
        self.move_object(place.x, place.y)
        self.authorized_pos[self.object.initPlace].av = True
        self.object.initx, self.object.inity = place.x, place.y
        self.object.initPlace = i
        place.av = False

    def return_object(self):
        '''Retourne l'objet à son emplacement inital (avant déplacement)'''
        self.move_object(self.object.initx, self.object.inity)


class ObjectCanvas():
    '''Contients les caractéristiques d'objets du canvas'''
    def __init__(self, x, y, initx, inity, initPlace, tag):
        '''Mémorise les caractéristiques de l'objet :
            x, y : coordonnées du coin supérieur gauche
            initx, inity : coordonnées initiales de l'objet avant déplacement
            initPlace : indice de l'emplacement initial dans le tableau
            authorizedPos
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
            availability : si l'emplacement est disponible ou occupé'''
        self.x, self.y, self.av = x, y, availability

welcome = Welcome("images")

'''
chosen_image = crop_image.image_choice("images")
image = crop_image.ImagePuzzle("images\\" + str(chosen_image))
ratio_wh = image.width/image.height
Application(40, 70*ratio_wh, 70, 5, 5, image)
'''









