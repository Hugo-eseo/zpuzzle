# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:23:08 2021

@author: Groupe 3 : Aurélie, Tristan et Hugo BOUY
"""

import tkinter as tk

import random
import math
from tkinter.messagebox import askyesno

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
            n_pc_h : nombre de pièces en hauteur
            image : image type ImagePuzzle (géré par le fichier crop_image)'''

        # Mémorisation des paramètres
        self.margin, self.pc_w, self.pc_h = margin, pc_w, pc_h
        self.n_pc_w, self.n_pc_h = n_pc_w, n_pc_h

        # Width et height : Largeur et hauteur du canvas
        self.width = self.pc_w*self.n_pc_w*2 + self.margin/2*(self.n_pc_w + 5)
        self.height = self.pc_h*self.n_pc_h + self.margin*4 + 150  # TEMPORAIRE

        # Création de la fenêtre
        self.wnd = tk.Tk()
        self.wnd.title("ZPuzzle")

        # Création de la zone de dessin
        self.cnv = tk.Canvas(self.wnd, width=self.width,
                             height=self.height, bg='white', bd=0,
                             highlightthickness=0, relief='ridge')
        self.cnv.pack(side=tk.TOP)

        # Création des éléments servant pour la découpe de l'image

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
                     for i in range(j, self.n_pc_w + j)]
                     for j in range(0, self.n_pc_h*self.n_pc_w, self.n_pc_w)]

        # Création de la zone de commande du jeu
        self.frm = tk.Frame(self.wnd, height=self.frameHight,
                            width=self.width, bg='green')
        self.frm.pack_propagate(0)
        self.frm.pack(side=tk.BOTTOM, expand=True)

        '''# Création de la fenêtre de réussite et de ses éléments
        self.frmr = tk.Frame(self.wnd, height=(self.frameHight)/2,
            width=(self.width)/2, bg='white')
        self.total_attempt = tk.Label(self.frmr, text='Déplacements totaux: ',
            width=10)'''

        # TEST

        self.top_frame = tk.Frame(self.cnv, height=self.margin,
                                  width=self.width, bg='green')
        self.top_frame.pack_propagate(0)
        self.top_frame.place(x=0, y=0, anchor=tk.NW)

        # Création des boutons

        self.start = tk.Button(self.frm, text='Start', command=self.start_game)
        self.start.pack(side=tk.TOP, pady=5, padx=5)
        tk.Button(self.frm, text='Quitter', command=self.stop_game).pack()
        self.sc = tk.Label(self.top_frame, text='VOTRE SCORE: ', width=14,
                           bg='green', fg='white',
                           font=('Franklin Gothic Demi Cond', 12))
        self.sc.pack(side=tk.LEFT, pady=5, padx=5)
        self.attempt = tk.Label(self.top_frame, text='Déplacements : 0',
                                width=17, bg='green', fg='white',
                                font=('Franklin Gothic Demi Cond', 12))
        self.attempt.pack(side=tk.LEFT, pady=5, padx=5)
        self.chrono = tk.Label(self.top_frame, text='Temps écoulé : 0s',
                               width=30, bg='green', fg='white',
                               font=('Franklin Gothic Demi Cond', 12))
        self.chrono.pack(side=tk.LEFT, pady=5, padx=5)

        # Remise à zéro du chrono
        self.sec = 55
        self.min = 0
        self.hour = 0
        self.chrono_on = [False, None]
        self.move = 0

        # Winframe(self.wnd, self.sec, self.nb_coup) #TEMPORAIRE

        # TEMPORAIRE
        self.submit_button = tk.Button(self.frm, text='Soumettre',
                                       command=self.submit)
        self.submit_button.pack_forget()

        '''Pour fonctionner, le jeu utilise 3 classes suplémentaires:

            ObjectCanvas : Mémorise toutes les informations des tuiles sur le
            canvas (coordonnées, tag...). Chaque tuile a son ObjectCanvas
            correspondant. L'ensemble des ObjectCanvas est ensuite mémorisé
            dans la liste self.object_list

            PlaceCanvas : Mémorise les informations de chaque emplacement
            disponible sur le canvas. Un emplacement est soit l'emplacement
            initiale de la tuile, soit une case du plateau de jeu.
            L'ensemble des PlaceCanvas est mémorisé dans la liste
            self.authorized_pos'

            ObjectSelect : Mémorise lorsqu'un objet est sélectionné :
                - Son ObjectCanvas coorespondant
                - Son emplacement PlaceCanvas initial/de départ
                - Et la bordure verte indiquant que l'objet est sélectionné
        '''

        # Création des éléments de jeux (tuiles + emplacements)
        self.object_list = list()
        self.authorized_pos = list()
        # Variable mémorisant l'objet sélectionné du type ObjectSelect
        self.object = None
        # Utilisé pour le tag canvas de l'objet
        id_p = 0

        # Etape 1: Création du plateau de jeu
        for i in range(self.n_pc_h):
            for j in range(self.n_pc_w):
                x, y = i*self.pc_w + self.margin, j*self.pc_h + self.margin*3
                self.cnv.create_rectangle(x, y, x + self.pc_w, y + self.pc_h)
                # Sauvegarde chaque emplacement dessiné
                self.authorized_pos.append(PlaceCanvas(x, y, None))

        # Etape 2 : Affichage des tuiles dans la pioche
        for i in range(self.n_pc_h):
            for j in range(self.n_pc_w):
                # Affichage des images découpés
                xi = self.pc_w*(self.n_pc_w) + self.margin*2 + \
                    i*(self.pc_w + self.margin/2)
                yi = j*(self.pc_h + self.margin/2) + self.margin*2
                tag = "Object" + str(id_p)
                self.cnv.create_image(xi + self.pc_w/2, yi + self.pc_h/2,
                                      image=mat_tiles[i][j][0], tag=tag)
                # Sauvegarde chaque objet crée
                self.object_list.append(ObjectCanvas(xi, yi, tag,
                                                     mat_tiles[i][j][1]))
                # Sauvegarde l'emplacement correspondant
                self.authorized_pos.append(PlaceCanvas(xi, yi,
                                                       self.object_list[-1]))
                id_p += 1

        # Création des éléments de dessin graphiques :
        # Création de la sinusoide

        # Configuration
        # Pas suivant x
        x_increment = 1
        # Largeur du sinus
        x_factor = x_increment / 150
        # Amplitude du sinus
        y_amplitude = 40

        '''Calcule tous les "x_increment" (pas) la valeur du sinus
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

        Rules(self.wnd, 200, 500)
        Winframe(self.wnd, self.sec, self.move)
        self.wnd.protocol("WM_DELETE_WINDOW", self.stop_game)
        self.wnd.mainloop()

    '''Pour chaque 'clic' de souris différent (clic, relachement du clic
    ou déplacement de la souris avec le clic maintenu), une fonction
    correspondante appelle la machine a état'''

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
        '''Verification du puzzle lorsque l'utilisateur appuis sur le bouton
        soumettre'''
        self.victory = True
        wrong_pos_object = list()
        # On vérifie emplacement par emplacement si ce dernier est
        # occupé par la bonne pièce
        for k in range(self.n_pc_w * self.n_pc_h):
            if k != self.authorized_pos[k].ob.number:
                self.victory = False
                # En cas de pièce au mauvaise endroit, on affiche
                # un rectangle rouge par dessus
                x, y = self.authorized_pos[k].x, self.authorized_pos[k].y
                rectangle = self.cnv.create_rectangle(x, y, x + self.pc_w, y +
                                                      self.pc_h, outline='red',
                                                      fill="red",
                                                      width=2,
                                                      stipple="gray50")
                current_object = ObjectSelect(self.authorized_pos[k].ob,
                                              self.authorized_pos[k])
                # On mémorise la pièce et son rectangle dans une liste
                wrong_pos_object.append([current_object, rectangle])
        if not self.victory:
            # En cas de mauvaise combinaison, le bouton Retirer s'affiche
            self.submit_button.config(text="Retirer", command=lambda:
                        self.return_wrong_pos_object(wrong_pos_object))
            # On désactive les clics
            self.cnv.unbind('<Button-1>')
            self.cnv.unbind('<B1-Motion>')
            self.cnv.unbind('<ButtonRelease-1>')
        else:
            # Sinon c'est la victoire !
            print("Won !")

    def return_wrong_pos_object(self, wrong_pos_object):
        '''Retourne les pièces étant à la mauvaise position à un emplacement
        disponible'''
        for i in range(len(wrong_pos_object)):
            self.send_back_object_to_deck(wrong_pos_object[i][0])
            self.cnv.delete(wrong_pos_object[i][1])
        # On enlève le bouton retirer
        self.submit_button.config(text="Soumettre", command=self.submit)
        self.submit_button.pack_forget()
        # On réactive les clics :
        self.cnv.bind('<Button-1>', self.clic)
        self.cnv.bind('<B1-Motion>', self.drag_clic)
        self.cnv.bind('<ButtonRelease-1>', self.release_clic)

    def start_game(self):
        '''Lance la partie !'''
        # Bind des touches de la souris
        self.cnv.bind('<Button-1>', self.clic)
        self.cnv.bind('<B1-Motion>', self.drag_clic)
        self.cnv.bind('<ButtonRelease-1>', self.release_clic)
        # Lance le timer
        self.chrono_on[0] = True
        self.timer()
        self.start.destroy()

    def stop_game(self):
        '''Stop la partie'''
        self.chrono_on[0] = False
        if self.chrono_on[1] is not None:
            self.wnd.after_cancel(self.chrono_on[1])
        self.wnd.destroy()

    def timer(self):
        ''' Méthode permettant le suivi du temps écoulé après le lancement
        du jeu '''
        if self.chrono_on[0]:
            if self.sec >= 0 and self.min == 0  and self.hour == 0:
                string = "Temps écoulé: " + str(self.sec) + " s"
            if self.min == 60 and self.sec == 60:
                self.hour += 1
                self.min = 0
                self.sec = 0
                string = "Temps écoulé: " + str(self.hour) + " h :" +\
                    str(self.min) + " m :" + str(self.sec) + " s"
            if self.sec == 60:
                self.sec = 0
                self.min += 1
                string = "Temps écoulé: " + str(self.min) + ' m :' +\
                    str(self.sec) + ' s'
            self.sec += 1
            self.chrono_on[1] = self.wnd.after(1000, self.timer)
            self.chrono.config(text=string)

    def update_score(self):
        '''Méthode affichant le score du joueur'''
        self.move += 1
        string = 'Déplacements: ' + str(self.move)
        self.attempt.config(text=string)

    '''
    Pour la machine à état, il existe deux modes de déplacement :
        Mode 1 : L'utilisateur clic une première fois sur un objet puis
        une deuxième fois sur une case vide : l'objet se déplace.
        Mode dit 'clic and move'
        Mode 2 : L'utlisateur clic sur un objet et le déplace avec sa
        souris jusqu'à l'emplacement voulu. Mode dit 'drag and drop'.'''

    def state_machine(self, event_x=None, event_y=None):
        '''Machine à état contrôlant les évènements du jeu'''
        # Status = 0, la machine attend le clic initial
        if self.status == 0:
            # Si c'est un clic qui appelle la machine
            if self.clic_type == 1:
                # Si le clic est sur un emplacement valide
                result = self.is_valid_pos(event_x, event_y)
                if result is not None:
                    # Si l'emplacement n'est pas vide
                    if result.ob is not None:
                        # On active la sélection sur l'objet présent
                        # sur l'emplacement
                        self.status = 1
                        self.active_selection_on_object(result.ob, result)

        # Status = 1, la machine attend l'évènement suivant le clic initial
        elif self.status == 1:
            # Si le clic est relaché
            if self.clic_type == 3:
                # On lance un chrono, ce chrono servira à différencier
                # un double clic rapide sur le même objet, de deux clic
                # espacés dans le temps sur le même objet.
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
                    # Si l'utilisateur re-dépose l'objet sur sa case initiale
                    if result is not None and result.ob == self.object.object:
                        # On ne désactive pas la sélection
                        self.status = 2
                    # Si l'utilisateur dépose l'objet sur une case contentant
                    # déjà un autre objet
                    elif result is not None and result.ob is not None:
                        # On échange intervertit les deux objets
                        self.swap_two_object(self.object,
                                             ObjectSelect(result.ob, result))
                    else:
                        # Sinon, on retire la sélection active
                        self.desactivate_curent_selection()
                # Si l'emplacement est libre
                else:
                    # On y déplace l'objet
                    self.send_object_to_final_pos(self.object, result)

    def swap_two_object(self, object1, object2):
        '''Enchange la position de deux objets'''
        # 1 : On déplace les deux objets
        self.move_object(object1, object2.init_pos.x, object2.init_pos.y)
        self.move_object(object2, object1.init_pos.x, object1.init_pos.y)
        # 2 : On met à jour leur emplacement initial
        object1.init_pos.ob = object2.object
        object2.init_pos.ob = object1.object
        # 3 : On désactive la sélection
        self.desactivate_curent_selection()
        # 4 : On vérifie si le puzzle est complet
        self.check_puzzle_complete()
        # 5 : On met à jour le score
        self.update_score()

    def send_object_to_final_pos(self, object_select, pos):
        '''Envoie l'object de type ObjectSelect
        passé en argument vers sa position finale pos'''
        # 1 : On déplace l'objet
        self.move_object(object_select, pos.x, pos.y)
        # 2 : On met à jour l'emplacement initial
        object_select.init_pos.ob = None
        # 3 : On met à jour l'emplacement final
        pos.ob = object_select.object
        # 4 : On désactive la sélection
        if object_select.border is not None:
            self.desactivate_curent_selection()
        # 5 : On vérifie si le puzzle est complet
        self.check_puzzle_complete()
        # 6 : On met à jour le score
        self.update_score()

    def send_back_object_to_deck(self, object_select):
        '''Renvoie l'objet passé en argument dans la pioche'''
        for k in range(self.n_pc_w * self.n_pc_h, len(self.authorized_pos)):
            if self.authorized_pos[k].ob is None:
                # On déplace l'objet dans le premier emplacement libre de la
                # pioche trouvé
                self.send_object_to_final_pos(object_select,
                                              self.authorized_pos[k])
                return

    def move_object(self, object_select, x, y):
        '''Déplace l'objet de type ObjectSelect passé en argument
        dans le canvas aux coordonnées x, y'''
        difx = - (object_select.object.x - x)
        dify = - (object_select.object.y - y)
        # On met à jour les coordonnées de l'objet
        object_select.object.x = x
        object_select.object.y = y
        self.cnv.move(object_select.object.tag, difx, dify)
        # Si l'objet contient une bordure
        if object_select.border is not None:
            self.cnv.move(object_select.border, difx, dify)

    def stop_chrono(self):
        '''Arrête le chrono de la machine à état'''
        self.chrono_stop = True

    def active_selection_on_object(self, object_select, place):
        '''Active la sélection sur l'objet passé en argument.
        Dessine un contour vert autour de lui et le mémorise'''
        # Passe au premier plan l'objet sélectionné
        self.cnv.tag_raise(object_select.tag)
        rectangle = self.cnv.create_rectangle(object_select.x, object_select.y,
                                              object_select.x + self.pc_w,
                                              object_select.y + self.pc_h,
                                              outline='green', fill="",
                                              width=5)
        self.object = ObjectSelect(object_select, place, rectangle)

    def desactivate_curent_selection(self):
        '''Désactive la sélection sur l'objet self.object en cours'''
        self.cnv.delete(self.object.border)
        self.object = None
        self.status = 0

    def is_valid_pos(self, x, y):
        '''Retourne l'emplacement de type PlaceCanvas aux coordonnées passées
        en argument. Retourne None si x, y ne correspond aux coordonnées
        d'aucun emplacement valide'''
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
                self.submit_button.pack_forget()
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
        '''Affiche les caractéristiques de l'objet (pour debug)'''
        r = str(self.x) + ', ' + str(self.y) + ", tag=" + str(self.tag)\
            + " number=" + str(self.number)
        return r


class ObjectSelect():
    '''Contients les caractéristiques de l'objet sélectionné
        object : contient l'objet du type ObjectCanvas
        border : contient le rectangle indiquant que l'objet est
        initPos : contient l'emplacement du type PlaceCanvas de départ
        de l'objet sélectionné'''

    def __init__(self, object_select, init_pos, border=None):
        self.object, self.border = object_select, border
        self.init_pos = init_pos


class PlaceCanvas():
    '''Contients des emplacements possible des pièce de jeu sur le canvas'''

    def __init__(self, x, y, occupied_by):
        '''Mémorise les caractéristiques de l'emplacement :
            x, y : coordonnées du coin supérieur gauche
            occupied_by : objet occupant l'emplacement '''
        self.x, self.y, self.ob = x, y, occupied_by


class Winframe(tk.Toplevel):
    '''Contient les éléments qui résumment le score du joueur'''

    def __init__(self, parent, sec, nbcoup):
        super().__init__(parent)
        # Configuration de la fenêtre
        self.geometry("-690+350")
        self.wm_attributes('-topmost', 1)
        self.title("Score final")
        self.config(bg='white')
        # Définition du score total
        self.time_total = 'Temps total: ' + str(sec)
        self.nbmove_total = 'Nombre de déplacements totaux :' + str(nbcoup)
        tk.Label(self, text=self.time_total, bg='white').pack(pady=10)
        tk.Label(self, text=self.nbmove_total, bg='white').pack(pady=10)
        # Création des boutons pour rejouer ou quitter
        tk.Button(self, text="Recommencer", command=self.destroy).pack()
        tk.Button(self, text='Quitter', command=lambda: self.leave(parent))\
            .pack()

    def leave(self, wnd):
        '''Permet de quitter le jeu à partir de la fenêtre des scores à l'aide
        d'une fenêtre popup'''
        # Affiche la fenêtre popup au premier plan
        wnd.wm_attributes('-topmost', 1)
        if askyesno('Vous êtes sur le point de quitter',
                    'Êtes-vous sûr de vouloir quitter ?'):
            wnd.destroy()


class Rules(tk.Toplevel):
    '''Fenêtre affichant les règles à suivre pour jouer au jeu'''

    def __init__(self, parent, frame_height, frame_width):
        super().__init__(parent)
        # Configuration de la fenêtre
        self.title("Règles du jeu")
        self.config(bg='white')
        # Positionnement au centre de l'écran et en premier plan
        self.geometry("-500+275")
        self.wm_attributes("-topmost", 1)
        # Création des bandeaux de décoration
        frm = tk.Frame(self, height=25, width=frame_width, bg='green')
        frm_bot = tk.Frame(self, height=25, width=frame_width, bg='green')
        frm.pack_propagate(0)
        frm_bot.pack_propagate(0)
        frm.pack(side=tk.TOP)
        frm_bot.pack(side=tk.BOTTOM)
        tk.Label(frm, text="Bonjour et bienvenue dans ZPUZZLE !",
                 bg='green', fg='white', font=('Franklin Gothic Demi Cond',
                                               11)).pack()
        tk.Button(frm_bot, text='OK', relief='flat', bg='white',
                  command=self.destroy).pack(side=tk.BOTTOM)
        # Définition des règles
        txt = " \n Votre objectif est de compléter ce puzzle avec le moins" +\
            " de \n déplacements possible et dans un minimum de temps"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "Pour déplacer une tuile deux choix s'offrent à vous:"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "-Cliquez sur la tuile et cliquer ensuite sur \n" +\
            " l'emplacement que vous voulez"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "-Maintenez le clic sur la tuile et déplacez la en \n la" +\
            " glissant sur le plateau"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "Pour retirer une tuile, double-cliquez sur celle-ci"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "Vous pouvez interchanger deux tuiles en glissant la \n" +\
            " première sur la deuxième"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "Appuyer sur le bouton soumettre lorsque vous aurez complété" +\
            " le puzzle. Vos erreurs seront \n indiquées en rouge et vous" +\
            " pourrez alors retirer les mauvaises tuiles \n en appuyant" +\
            " sur le bouton Retirer"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "Si votre puzzle est réussi, une fenêtre popup s'affichera" +\
            " indiquant votre score final.\n Vous aurez alors le choix" +\
            " entre rejouer ou bien quitter l'application \n \n" +\
            "Bon courage ! \n "
        tk.Label(self, text=txt, bg='white').pack()


image = crop_image.ImagePuzzle("images\img_forest.jpg")
boite = Application(50, 75, 75, 5, 5, image)
