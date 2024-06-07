from game.boutton_Menu import *
from game.settings import *
from game.game import *
from game.methods import *

import pygame as pg
import sys
import pickle
import os

########################################################
"""
La classe Menu gère l'affichage et les événements du menu principal du jeu.
"""
########################################################

class Menu():
    def __init__(self, screen, lanceur):
        # Initialisation de l'objet Menu
        self.lanceur = lanceur
        self.screen = screen

        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont('Constantia', 50)
        self.font2 = pg.font.SysFont('Constantia', 50)
        self.current = "Main"

        # Chargement de l'image de fond du menu
        self.background = pg.transform.scale(background_of_menu, screen.get_size())
        
        # Chargement / récupération / mise à l'échelle de l'image du menu
        self.background_name = pg.image.load("./mon_code/assets/graphics/background_name.png")
        self.longueur_image_menu_name = self.background_name.get_width()
        self.largeur_image_menu_name = self.background_name.get_height()
        self.new_longueur_image_menu_name = self.longueur_image_menu_name//6
        self.new_largeur_image_menu_name = self.largeur_image_menu_name//6
        self.background_name = pg.transform.scale(self.background_name, (self.new_longueur_image_menu_name, self.new_largeur_image_menu_name))
        
        self.mid_width = (self.screen.get_width() // 2) - (WIDTH_BUTTON // 2)
        self.mid_height = (self.screen.get_height() // 2) - (1.5 * HEIGHT_BUTTON)
        
        # Variable d'état pour le menu
        self.displayed = True
        self.start = False
        self.load = False
        #self.save = False
        self.pause = False
        

    def display_main(self):
        # Méthode pour afficher le menu principal
        if self.displayed:
            # Affichage des bouttons 
            self.Start_new_game  = Button_Menu(self.screen, self.mid_width, self.mid_height, 'Nouvelle partie')
            #self.Load_Saved_Game = Button_Menu(self.screen, self.mid_width, self.mid_height, 'Charger partie sauvegarder')
            self.Options         = Button_Menu(self.screen, self.mid_width, self.mid_height + GAP, 'Options')
            self.Createur        = Button_Menu(self.screen, self.mid_width, self.mid_height + (2 * GAP), 'Createur')
            self.Exit            = Button_Menu(self.screen, self.mid_width, self.mid_height + (3 * GAP), 'Exit')
            
    def events(self):
        # Méthode pour gérer les événements liés au menu principal
        for event in pygame.event.get():
            # Lancement d'une nouvelle partie
            if self.Start_new_game.check_button(event):
                self.active=False
                return "nouvelle partie"

            # Chargmeent d'une partie sauvegardé
            #if self.Load_Saved_Game.check_button(event):
            #    self.active=False
            #    return "reprendre"

            # Quiter le jeu
            if self.Exit.check_button(event):
                run = False
                sys.exit()

            # Les paramètres du jeu
            if self.Options.check_button(event):
                self.active=False
                return "formulaire"
               
            # Pour voir les créateurs
            if self.Createur.check_button(event):
                self.current = "Creators"
                self.display_creators()
                run = False
            
            if event.type == pg.QUIT:
                run = False
                sys.exit()


    def run(self):
        self.display_main()
        self.active=True
        while self.active:
            next=self.events()
            self.draw()
        return next
    
    
    def draw(self):
        # Méthode pour afficher le menu principal
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.background_name, (self.screen.get_width()//2 - self.background_name.get_width()//2, self.screen.get_height()//4 - self.background_name.get_height()//1.3))

        # Pour afficher les bouttons
        self.Start_new_game.draw()
        #self.Load_Saved_Game.draw()
        self.Createur.draw()
        self.Options.draw()
        self.Exit.draw()

        pg.display.flip()


    def display_creators(self):
        # Méthode pour afficher le nom des créateur
        if self.displayed:

            Return = Button_Menu(self.screen, self.mid_width, self.mid_height + (4 * GAP), 'Return')

            run = True
            while run:
                self.screen.blit(self.background, (0, 0))

                names = ["Bob Land a Game centred around a visual ","and interactive simulation of natural selection","created by :", "Morad", "Aymen", "Yassmine", "Oumaima", "Maxime", "Yassine"]
                for i, name in enumerate(names):
                    text_surface = self.font.render(name, True, (0, 0, 0))  # (0, 0, 0) représente la couleur noire
                    text_rect = text_surface.get_rect()
                    text_rect.center = (self.screen.get_width()//2, self.screen.get_height()//6 + i * 50)
                    self.screen.blit(text_surface, text_rect)

                Return.draw()
                
                for event in pg.event.get():
                    if Return.check_button(event):
                        run = False
                        self.current = "Main"
                        self.display_main()

                    if event.type == pg.QUIT:
                        run = False
                        sys.exit()

                pg.display.update()