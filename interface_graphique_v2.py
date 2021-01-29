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

    # Hauteur de la zone de commande
    frameHight = 200
    # Utilisée pour connaître l'issue du jeu
    victory = False
    # Utilisée pour connaître le type de clic
    clic_type = 0
    # Utilisée pour contrôler la machine à état
    status = 0
    # Utilisée pour le callback de la machie à état
    chrono_stop = True

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
        self.height = self.pc_h*self.n_pc_h + self.margin*4 + 100  # TEMPORAIRE

        # Création de la fenêtre
        self.wnd = tk.Tk()
        self.wnd.title("ZPuzzle")

        # Création de la zone de dessin
        self.cnv = tk.Canvas(self.wnd, width=self.width,
                             height=self.height, bg='white', bd=0,
                             highlightthickness=0, relief='ridge')
        self.cnv.pack(side=tk.TOP)

        # Création des éléments servant pour l'image

        # Récupération de la liste des tuiles de l'image
        tiles = image.crop(self.n_pc_w * self.n_pc_h)
        list_tiles = image.createTilesTk(tiles, self.pc_w, self.pc_h)

        # Ajout d'un indice pour la vérification
        self.list_tiles_i = [[list_tiles[i], i]
                             for i in range(len(list_tiles))]

        # Mélange de la liste
        random.shuffle(self.list_tiles_i)

        # Conversion en matrice self.n_pc_w*self.n_pc_h
        mat_tiles = [[[self.list_tiles_i[i][0], self.list_tiles_i[i][1]]
                     for i in range(j, self.n_pc_w+j)]
                     for j in range(0, self.n_pc_h*self.n_pc_w, self.n_pc_w)]

        # Création de la zone de commande du jeu
        self.frm = tk.Frame(self.wnd, height=self.frameHight,
                            width=self.width, bg='green')
        self.frm.pack_propagate(0)
        self.frm.pack(side=tk.BOTTOM, expand=True)

        # TEMPORAIRE
        self.submit_button = tk.Button(self.frm, text='Soumettre',
                                       command=self.submit)
        self.submit_button.pack_forget()

        # Création des éléments de jeux
        # On mémorise les caractéristques de chaque objet déplacable du canvas
        self.object_list = list()
        # Variable mémorisant l'objet en cours de déplacement
        self.object = None
        # On mémorise les emplacements autorisés des objets
        self.authorized_pos = list()
        id_p = 0
        for i in range(self.n_pc_h):
            for j in range(self.n_pc_w):
                # Création du plateau
                x, y = i*self.pc_w + self.margin, j*self.pc_h + self.margin*2
                self.cnv.create_rectangle(x, y, x + self.pc_w, y + self.pc_h)
                # Sauvegarde les emplacement possibles
                self.authorized_pos.append(PlaceCanvas(x, y, None))

        for i in range(self.n_pc_h):
            for j in range(self.n_pc_w):
                # Affichage des images découpés
                xi = self.pc_w*(self.n_pc_w) + self.margin*2 + \
                    i*(self.pc_w + self.margin/2)
                yi = j*(self.pc_h + self.margin/2) + self.margin
                tag = "Object"+str(id_p)
                self.cnv.create_image(xi + self.pc_w/2, yi + self.pc_h/2,
                    image=mat_tiles[i][j][0], tag=tag)
                # Sauvegarde les coordonées du coin supérieur gauche et
                # l'id de l'objet pour déplacement ultérieur
                self.object_list.append(ObjectCanvas(xi, yi, tag,
                    mat_tiles[i][j][1]))
                # Sauvegarde l'emplacement
                self.authorized_pos.append(PlaceCanvas(xi, yi,
                    self.object_list[-1]))
                id_p += 1

        # Création des éléments graphiques

        # Pas suivant x
        x_increment = 1

        # Largeur du sinus
        x_factor = x_increment / 150

        # Amplitude du sinus
        y_amplitude = 40

        '''Calcul tous les "x_increment" (pas) la valeur du sinus
        la place dans un tableau de valeur avec l'abscisse, puis crée un
        polygone avec ces coordonnées'''

        xy = list()

        i = 0
        while x < self.width:
            x = i * x_increment
            xy.append(x)
            y = int(math.sin(i * x_factor) * y_amplitude)
            xy.append(-y + self.height - y_amplitude)
            i += 1
        xy.append(self.width)
        xy.append(self.height)
        xy.append(0)
        xy.append(self.height)
        self.cnv.create_polygon(xy, fill='green')

        # Bind des touches de la souris
        self.cnv.bind('<Button-1>', self.clic)
        self.cnv.bind('<B1-Motion>', self.drag_clic)
        self.cnv.bind('<ButtonRelease-1>', self.release_clic)
        self.wnd.mainloop()

    def clic(self, event):
        '''Appelée si un clic a eu lieu'''
        self.clic_type = 1
        self.state_machine(event.x, event.y)

    def drag_clic(self, event):
        '''Appelée si un déplacement de la souris avec le clic maintenu
        a eu lieu'''
        self.clic_type = 2
        self.state_machine(event.x, event.y)

    def release_clic(self, event):
        '''Appelée quand le clic est relaché'''
        self.clic_type = 3
        self.state_machine(event.x, event.y)

    def submit(self):
        '''Verification du puzzle'''
        self.victory = True
        wrong_pos_object = list()
        for k in range(self.n_pc_w * self.n_pc_h):
            if k != self.authorized_pos[k].ob.number:
                self.victory = False
                if self.authorized_pos[k].ob is not None:
                    x, y = self.authorized_pos[k].x, self.authorized_pos[k].y
                    rectangle = self.cnv.create_rectangle(x, y, x +
                        self.pc_w, y + self.pc_h, outline='red', fill="red",
                        width=2, stipple="gray50")
                    current_object = ObjectSelect(self.authorized_pos[k].ob,
                        self.authorized_pos[k])
                    wrong_pos_object.append([current_object, rectangle])
        if not self.victory:
            self.submit_button.config(text="Retirer", command=lambda:
                self.return_wrong_pos_object(wrong_pos_object))
        else:
            print("Won !")

    def return_wrong_pos_object(self, wrong_pos_object):
        '''Retourne les pièces étant à la mauvaise position à un emplacement
        disponible'''
        for i in range(len(wrong_pos_object)):
            self.send_back_object_to_deck(wrong_pos_object[i][0])
            self.cnv.delete(wrong_pos_object[i][1])

        self.submit_button.config(text="Soumettre", command=self.submit)
        self.submit_button.pack_forget()

    '''
    Il existe deux modes de déplacement :
        Mode 1 : L'utilisateur clic une première fois sur un objet puis
        une deuxième fois sur une case vide : l'objet se déplace.
        Mode 2 : L'utlisateur clic sur un objet et le déplace avec sa
        souris jusqu'à l'emplacement voulu. Mode dit "drag and drop".'''

    def state_machine(self, event_x=None, event_y=None):
        '''Machine à état contrôlant les évènements du jeu'''
        # Status = 0, la machine attend le clic initial
        if self.status == 0:
            # Si le clic est sur un objet valide
            if self.clic_type == 1:
                result = self.is_valid_pos(event_x, event_y)
                if result is not None:
                    if result.ob is not None:
                        self.status = 1
                        self.active_selection_on_object(result.ob, result)

        # Status = 1, la machine attend l'évènement suivant le clic initial
        elif self.status == 1:
            # Si le clic est relaché
            if self.clic_type == 3:
                # On lance un chrono
                self.status = 2
                self.chrono_stop = False
                self.cnv.after(200, self.stop_chrono)
            # Si l'évènement est un "drag_clic"
            else:
                self.status = 3

        # Status = 2, la machine attend le prochain clic après le clic initial
        # (mode 1: clic and move)
        elif self.status == 2:
            result = self.is_valid_pos(event_x, event_y)

            # Si le deuxième clic n'est pas sur un emplacement valide
            if result is None:
                # On retire la sélection active
                self.desactivate_curent_selection()

            # Sinon on regarde par qui est occupé l'emplacement
            # Si l'emplacement est libre
            elif result.ob is None:
                # On déplace l'objet et désactive la sélection active
                self.send_object_to_final_pos(self.object, result)

            # Si le clic est effectué une deuxième fois sur le même objet
            elif result.ob == self.object.object:
                # Si le chrono ne s'est pas arrêté,
                # on retourne l'objet dans la pioche
                if not self.chrono_stop:
                    self.send_back_object_to_deck(self.object)
                    self.desactivate_curent_selection()
                # Sinon, on attend de nouveau un clic, retour à Status = 1
                else:
                    self.status = 1

            # Si le clic est effectué sur un autre objet
            # On active la sélection sur cet objet
            else:
                self.desactivate_curent_selection()
                self.active_selection_on_object(result.ob, result)
                self.status = 1

        # Status = 3, la machine attend le déplacement
        # ou relachement de la souris (mode 2: drag and drop)
        else:
            # Si la souris se déplace
            if self.clic_type == 2:
                # On fait suivre l'objet
                self.move_object(self.object, event_x - self.pc_w/2,
                    event_y - self.pc_h/2)
            # Si le clic est relaché
            else:
                # On vérifie l'emplacement
                result = self.is_valid_pos(event_x, event_y)
                # Si l'emplacement est invalide ou occupé
                if (result is None) or (result.ob is not None):
                    # On revoie l'objet à sa position initiale
                    self.move_object(self.object, self.object.init_pos.x,
                        self.object.init_pos.y)
                    # On retire la sélection active
                    self.desactivate_curent_selection()
                # Si l'emplacement est libre
                else:
                    self.send_object_to_final_pos(self.object, result)

    def send_object_to_final_pos(self, object_select, pos):
        '''Envoie l'object passé en argument vers sa position finale'''
        self.move_object(object_select, pos.x, pos.y)
        object_select.init_pos.ob = None
        pos.ob = object_select.object
        self.desactivate_curent_selection()
        self.check_puzzle_complete()

    def send_back_object_to_deck(self, object_select):
        '''Renvoie l'objet passé en argument dans la pioche'''
        for k in range(self.n_pc_w * self.n_pc_h, len(self.authorized_pos)):
            if self.authorized_pos[k].ob is None:
                self.move_object(object_select, self.authorized_pos[k].x,
                    self.authorized_pos[k].y)
                self.authorized_pos[k].ob = object_select.object
                object_select.init_pos.ob = None
                return

    def move_object(self, object_select, x, y):
        '''Déplace l'objet passé en argument
        dans le canvas aux coordonnées x, y'''
        difx = - (object_select.object.x-x)
        dify = - (object_select.object.y-y)
        object_select.object.x = x
        object_select.object.y = y
        self.cnv.move(object_select.object.tag, difx, dify)
        if object_select.border is not None:
            self.cnv.move(object_select.border, difx, dify)

    def stop_chrono(self):
        '''Arrête le chrono de la machine à état'''
        self.chrono_stop = True

    def active_selection_on_object(self, object_select, place):
        '''Active la sélection sur l'objet passé en argument.
        Dessine un contour vert autour de lui et le mémorise'''
        rectangle = self.cnv.create_rectangle(object_select.x, object_select.y,
            object_select.x + self.pc_w, object_select.y + self.pc_h,
            outline='green', fill="", width=5)
        self.object = ObjectSelect(object_select, place, rectangle)

    def desactivate_curent_selection(self):
        self.cnv.delete(self.object.border)
        self.object = None
        self.status = 0

    def is_valid_pos(self, x, y):
        '''Retourne l'emplacement des coordonnées passées en argument
        Retourne None si x, y ne correspond aux coordonnées d'aucun emplacement
        valide'''
        for i in range(len(self.authorized_pos)):
            if (x >= self.authorized_pos[i].x) and \
                (x <= self.authorized_pos[i].x + self.pc_w):
                if (y >= self.authorized_pos[i].y) and \
                    (y <= self.authorized_pos[i].y + self.pc_h):
                        return self.authorized_pos[i]
        return None

    def check_puzzle_complete(self):
        '''Vérifie si le puzzle est complet.
        Si oui affichage du bouton soumettre'''
        for k in range(self.n_pc_w * self.n_pc_h):
            if self.authorized_pos[k].ob is None:
                return
        self.submit_button.pack()


class ObjectCanvas():
    '''Contients les caractéristiques d'objets du canvas'''

    def __init__(self, x, y, tag, number):
        '''Mémorise les caractéristiques de l'objet :
            x, y : coordonnées du coin supérieur gauche
            tag : tag de l'objet dans le canvas
            number : numéro de tuile pour la vérification'''
        self.x, self.y, self.tag, self.number = x, y, tag, number

    def __str__(self):
        '''Affiche les principales coordonnées de l'objet (utile pour debug)'''
        r = str(self.x) + ', ' + str(self.y) + ", tag=" + str(self.tag)\
            + " number=" + str(self.number)
        return r


class ObjectSelect():
    '''Contients les caractéristiques de l'objet sélectionné
        object : contient l'objet du type ObjectCanvas
        border : contient le rectangle indiquant que l'objet est
        sélectionné'''

    def __init__(self, object_select, init_pos, border=None):
        self.object, self.border = object_select, border
        self.init_pos = init_pos


class PlaceCanvas():
    '''Contients des emplacements possible de pièce de jeu sur le canvas'''

    def __init__(self, x, y, occupied_by):
        '''Mémorise les caractéristiques de l'emplacement :
            x, y : coordonnées du coin supérieur gauche
            occupied_by : objet occupant l'emplacement
            number : numéro de l'emplacement pour la vérification'''
        self.x, self.y, self.ob = x, y, occupied_by


image = crop_image.ImagePuzzle("images\img_forest.jpg")
boite = Application(50, 100, 100, 5, 5, image)
