# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:23:08 2021

@author: Groupe 3 : Aurélie, Tristan et Hugo BOUY
"""

import tkinter as tk
import random
import math

import crop_image


class Application():
    '''Contients des objets correspondant à une fenêtre de jeu'''

    frameHight = 200 # Hauteur de la zone de commande
    victory = True # Utilisée pour contrôler le jeu à la fin
    wrong_pos = list() # Utilisée pour mémoriser les pièces au mauvais emplacement

    def __init__(self, margin, pc_w, pc_h, n_pc_w, n_pc_h, image):
        '''Crée une fenêtre tkinter. Prend en paramètres :
            margin : marge autour du puzzle
            pc_w : largueur de la pièce
            pc_h : hauteur de la pièce
            n_pc_w : nombre de pièces en largeur
            n_pc_h : nombre de pièces en hauteur'''

        # Mémorisation des paramètres
        self.margin, self.pc_w, self.pc_h = margin, pc_w, pc_h
        self.n_pc_w, self.n_pc_h = n_pc_w, n_pc_h

        # Width et height : Largeur et hauteur du canvas
        self.width = self.pc_w*self.n_pc_w*2 + self.margin/2*(self.n_pc_w + 5)
        self.height = self.pc_h*self.n_pc_h + self.margin*4 + 100 # TEMPORAIRE

        # Création de la fenêtre
        self.wnd = tk.Tk()
        self.wnd.title("ZPuzzle")

        #Création de la zone de dessin
        self.cnv = tk.Canvas(self.wnd, width = self.width,
            height = self.height, bg='white', bd=0, highlightthickness=0,
            relief='ridge')
        self.cnv.pack(side = tk.TOP)

        #Création des éléments servant pour l'image
        
        #Récupération de la liste des tuiles de l'image
        tiles = image.crop(self.n_pc_w * self.n_pc_h)
        list_tiles =  image.createTilesTk(tiles, self.pc_w, self.pc_h)

        #Ajout d'un indice pour la vérification
        self.list_tiles_i = [[list_tiles[i],i] for i in range (len(list_tiles))]
        
        #Mélange de la liste
        random.shuffle(self.list_tiles_i)
        
        #Conversion en matrice self.n_pc_w*self.n_pc_h
        mat_tiles = [[[self.list_tiles_i[i][0],self.list_tiles_i[i][1]] \
            for i in range (j, self.n_pc_w+j)]\
            for j in range (0, self.n_pc_h*self.n_pc_w, self.n_pc_w)]
        
        
        #Création de la zone de commande du jeu
        self.frm = tk.Frame(self.wnd, height = self.frameHight,
            width = self.width, bg='green')
        self.frm.pack_propagate(0)
        self.frm.pack(side=tk.BOTTOM, expand = True)
        
        #TEMPORAIRE
        self.submit_button = tk.Button(self.frm, text='Soumettre', command=self.submit)
        self.submit_button.pack_forget()

        #Création des éléments de jeux
        #On mémorise les caractéristques de chaque objet déplacable du canvas
        self.object_list=list()
        #Variable mémorisant l'objet en cours de déplacement
        self.object = None
        #On mémorise les emplacements autorisés des objets
        self.authorized_pos=list()
        id_p=0
        for i in range (self.n_pc_h):
            for j in range (self.n_pc_w):
                #Création du plateau
                x, y = i*self.pc_w + self.margin, j*self.pc_h + self.margin*2
                self.cnv.create_rectangle(x, y, x + self.pc_w, y + self.pc_h)
                #Sauvegarde les emplacement possibles
                self.authorized_pos.append(PlaceCanvas(x,y,None))

        for i in range (self.n_pc_h):
            for j in range (self.n_pc_w):
                #Affichage des images découpés
                xi = self.pc_w*(self.n_pc_w) + self.margin*2 + \
                                      i*(self.pc_w + self.margin/2)
                yi = j*(self.pc_h + self.margin/2) + self.margin
                tag="Object"+str(id_p)
                self.cnv.create_image(xi + self.pc_w/2, yi + self.pc_h/2,
                    image = mat_tiles[i][j][0], tag=tag)
                # Sauvegarde les coordonées du coin supérieur gauche et
                #l'id de l'objet pour déplacement ultérieur
                self.object_list.append(ObjectCanvas(xi, yi, xi, yi,
                    len(self.authorized_pos), tag, mat_tiles[i][j][1]))
                #Sauvegarde l'emplacement
                self.authorized_pos.append(PlaceCanvas(xi,yi,mat_tiles[i][j][1]))
                id_p+=1
                
        #Création des éléments graphiques
        
        # Pas suivant x
        x_increment = 1
        
        # Largeur du sinus
        x_factor = x_increment / 150
        
        # Amplitude du sinus
        y_amplitude = 40
        
        '''Calcul tous les "x_increment" (pas) la valeur du sinus
        la place dans un tableau de valeur avec l'abscisse, puis crée un
        polygone avec ces coordonnées'''
        
        xy=list()
        
        i=0
        while x < self.width:
            x=i * x_increment
            xy.append(x)
            y=int(math.sin(i * x_factor ) * y_amplitude)
            xy.append(-y + self.height - y_amplitude)
            i+=1
        xy.append(self.width)
        xy.append(self.height)
        xy.append(0)
        xy.append(self.height)
        self.cnv.create_polygon(xy, fill='green')
        
        #Bind des touches de la souris
        self.status=0
        self.cnv.bind('<Button-1>',self.clic)
        self.cnv.bind('<B1-Motion>', self.drag_clic)
        self.cnv.bind('<ButtonRelease-1>', self.release_clic)
        self.wnd.mainloop()
        
    def submit(self):
        '''Verification du puzzle'''
        self.victory = True
        for k in range (self.n_pc_w * self.n_pc_h):
            #print(k, ",", self.authorized_pos[k].ob)
            if k != self.authorized_pos[k].ob:
                self.victory = False
                if self.authorized_pos[k].ob != None:
                    x, y = self.authorized_pos[k].x, self.authorized_pos[k].y
                    rectangle = self.cnv.create_rectangle(x, y, x + \
                        self.pc_w, y + self.pc_h, outline='red', fill="red", width=2, stipple="gray50")
                    self.wrong_pos.append([self.authorized_pos[k].ob, rectangle])
        if not self.victory:
            self.submit_button.config(text="Retirer", command=self.return_p)
        else:
            print("Won !")
        
    def return_p(self):
        '''Retourne les pièces étant à la mauvaise position à un emplacement
        disponible'''
        for i in range(len(self.wrong_pos)):
            for j in range (len(self.object_list)):
                if self.object_list[j].number == self.wrong_pos[i][0]:
                    self.object = self.object_list[j]
                    for k in range(self.n_pc_w * self.n_pc_h, len(self.authorized_pos)):
                        if self.authorized_pos[k].ob is None :
                            self.adjust_pos(self.authorized_pos[k], k)  
                            self.cnv.delete(self.wrong_pos[i][1])
                            break
                    break
        self.wrong_pos=[]                          
        self.submit_button.config(text="Soumettre", command=self.submit)
        self.submit_button.pack_forget()

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
                self.rectangle = self.cnv.create_rectangle(self.object.x, \
                    self.object.y, self.object.x + self.pc_w, \
                    self.object.y + self.pc_h, outline='green', fill="", width=5)
                return
            self.status = 0

        elif self.status == 2:
            self.status = 0
            self.final_pos(event.x, event.y)

        else:
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
        self.cnv.move(self.rectangle, difx, dify)

    def final_pos(self, x, y):
        '''Déplace et ajuste si possible l'objet vers sa position finale'''
        valid, place, i = self.valid_pos(x, y)
        if valid:
            self.adjust_pos(place, i)
            self.check_puzzle_complete()
            self.cnv.delete(self.rectangle)
        else:
            self.return_object()
            self.cnv.delete(self.rectangle)
            #Si la place est occupée, simulation d'un clic dessus
            if place is not None:
                #Si le clic est effectué sur le même objet, on le retourne dans le deck
                if place.ob == self.object.number:
                    self.wrong_pos.append([self.object.number, self.rectangle])
                    self.return_p()
                    return
                self.clic(place)
                self.release_clic(place)
                

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
                    if self.authorized_pos[i].ob is None:
                        return True, self.authorized_pos[i], i
                    return False, self.authorized_pos[i], None
        return False, None, None

    def adjust_pos(self, place, i):
        '''Ajuste l'objet à la case sur la souris'''
        self.move_object(place.x, place.y)
        self.authorized_pos[self.object.init_place].ob = None
        self.object.initx, self.object.inity = place.x, place.y
        self.object.init_place = i
        place.ob = self.object.number

    def return_object(self):
        '''Retourne l'objet à son emplacement inital (avant déplacement)'''
        self.move_object(self.object.initx, self.object.inity)
        
    def check_puzzle_complete(self):
        '''Vérifie si le puzzle est complet. Si oui affichage du bouton soumettre'''
        for k in range (self.n_pc_w * self.n_pc_h):
            if self.authorized_pos[k].ob is None:
                return
        self.submit_button.pack()


class ObjectCanvas():
    '''Contients les caractéristiques d'objets du canvas'''
    def __init__(self, x, y, initx, inity, init_place, tag, number):
        '''Mémorise les caractéristiques de l'objet :
            x, y : coordonnées du coin supérieur gauche
            initx, inity : coordonnées initiales de l'objet avant déplacement
            initPlace : indice de l'emplacement initial dans le tableau
            authorizedPos
            tag : tag de l'objet dans le canvas
            number : numéro de tuile pour la vérification'''
        self.x, self.y, self.tag, self.number = x, y, tag, number
        self.initx, self.inity, self.init_place = initx, inity, init_place

    def __str__(self):
        '''Affiche les principales coordonnées de l'objet (utile pour debug)'''
        r = str(self.x) + ', ' + str(self.y) + ', tag=' + str(self.tag)
        return r


class PlaceCanvas():
    '''Contients des emplacements possible de pièce de jeu sur le canvas'''
    def __init__(self, x, y, occupied_by):
        '''Mémorise les caractéristiques de l'emplacement :
            x, y : coordonnées du coin supérieur gauche
            occupied_by : numéro de l'objet occupant l'emplacement
            number : numéro de l'emplacement pour la vérification'''
        self.x, self.y, self.ob = x, y, occupied_by

image = crop_image.ImagePuzzle("images\img_forest.jpg")
boite=Application(50, 100, 100, 5, 5, image)
