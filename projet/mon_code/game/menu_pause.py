import pygame as pg
import sys

from game.boutton_Pause import *
from game.methods import *

########################################################
"""
La classe Pause_menu gère le menu de pause dans le jeu
"""
########################################################

class Pause_menu:
    def __init__(self, screen, lanceur):
        # Initialisation de l'objet Pause_menu
        self.lanceur = lanceur
        self.screen = screen
        self.center_x = screen.get_width()/2 ; self.center_y = screen.get_height()/2 
        
        self.font = pg.font.SysFont('path/to/PressStart2P.ttf', 75)
        self.font2 = pg.font.SysFont('path/to/PressStart2P.ttf', 50)
        self.space = 60
        self.text = "Pause"
        self.pause_image = pause_image
        self.pause_image = pg.transform.scale(self.pause_image, (self.pause_image.get_width()//10, self.pause_image.get_height()//10))
        
        # Variable d'état pour le menu
        self.displayed = False
        self.menu_principale = False
        self.new_game = False
        self.save = False
        self.quitter = False
        
        # Chargement / récupération / mise à l'échelle de l'image du menu pause
        self.fond_menu = pg.image.load("mon_code/assets/graphics/background_pause.png")
        self.longueur_centre_image_menu = self.fond_menu.get_width()*0.4
        self.largeur_centre_image_menu = self.fond_menu.get_height()*0.4
        self.fond_menu = pg.transform.scale(self.fond_menu, (self.longueur_centre_image_menu, self.largeur_centre_image_menu))
    
        # Création bouttons du menu pause
        self.menu_principale = Button_Pause(self.screen, self.center_x - self.space*1.4, self.center_y - (2*self.space), 'Menu principale')
        self.new_game        = Button_Pause(self.screen, self.center_x - self.space*1.4, self.center_y - (1*self.space), 'Nouvelle partie')
        self.save            = Button_Pause(self.screen, self.center_x - self.space*1.4, self.center_y, 'Sauvegarder')
        self.settings        = Button_Pause(self.screen, self.center_x - self.space*1.4, self.center_y  - (-1*self.space), 'Réglages')
        self.quitter         = Button_Pause(self.screen, self.center_x - self.space*1.4, self.center_y  - (-2*self.space), 'Quitter le jeu')

        # Longueur du "Pause" affiché au dessus du menu
        self.title_menu = self.font.render(self.text, True, (255, 0, 0))
        self.width_title = self.title_menu.get_width()


    def events(self):
        # Méthode pour gérer les événements liés au menu de pause
        for event in pg.event.get():
            # Revenir au menu principale 
            if self.menu_principale.check_button(event):
                self.active=False
                return "main menu"
               
            # Paramètre
            if self.settings.check_button(event):
                self.active=False
                return "formulaire pause"
                
            # Nouvelle partie
            if self.new_game.check_button(event):
                self.active=False
                return "nouvelle partie"
            
            # Sauvegarde
            if self.save.check_button(event):
                self.active=False
                return "sauvegarder"

            # Quitter le jeu
            if self.quitter.check_button(event):
                self.active = False
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: # Pour echap (pause v1)
                    self.active=False
                    return "game"
                if event.key == pg.K_x: # Pour X (pause v2)
                    self.active=False
                    return "game"
        
        return True


    def draw(self):
        # Méthode pour afficher le menu de pause
        # --> Affichage du fond du menu
        self.screen.blit(self.fond_menu,(self.center_x - (self.longueur_centre_image_menu//2.1), self.center_y//5))
        # --> Affichage du titre "Pause"
        self.screen.blit(self.pause_image,(self.center_x - (self.pause_image.get_width()//2.2), self.center_y - self.longueur_centre_image_menu//4.2))

        # Affichage des boutons de notre menu pause
        self.new_game.draw()
        self.save.draw()
        self.menu_principale.draw()
        self.settings.draw()
        self.quitter.draw()
        
        pg.display.flip()
    

    def run(self): # Pause avec 'ECHAP'
        self.active=True
        while self.active:
            self.draw()
            next=self.events()
        return next


    def run_pause_v2(self, game): # Pause avec 'X'
        self.active=True
        while self.active:
            game.update() # pour initialiser
            game.draw() # pour dessiner la map
            next=self.events()
        return next


    def update_display(self):
        # Méthode pour mettre à jour la variable d'affichage du menu
        self.displayed = not self.displayed
        