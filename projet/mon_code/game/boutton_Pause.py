import pygame
from pygame.locals import *
from game.settings import *

########################################################
"""
Classe Button_Pause utilisée pour créer des boutons interactifs dans le menu de pause d'un jeu.
"""
########################################################

class Button_Pause():
    def __init__(self, screen, x, y, text):
        # Initialisation de l'objet Button_Pause
        self.screen = screen
        self.x = x ; self.y = y
        self.width = 220 ; self.height = 45
        
        # Tous nos bouttons pour changer les couleurs
        self.button_rect = Rect(self.x, self.y, self.width, self.height) # Pour changer la couleur de nos bouttons
        self.button_orange = bouton_orange ; self.button_orange = pygame.transform.scale(self.button_orange, (self.width*3, self.height*3))
        self.button_orange_souris = bouton_orange_souris ; self.button_orange_souris = pygame.transform.scale(self.button_orange_souris, (self.width*3, self.height*3))
        self.button_click = bouton_rouge ; self.button_click = pygame.transform.scale(self.button_orange_souris, (self.width*3, self.height*3))

        self.text = text
        self.font = pygame.font.SysFont('path/to/PressStart2P.ttf', 30) 
        
        # Variables liées à l'état du bouton
        self.clicked = False
        self.current_button = self.button_orange
        self.space = 30
        self.text_original = BLACK
        self.text_base = self.text_original
        self.clic = False


    def draw(self):
        # Méthode pour dessiner le bouton sur l'écran
        text_img = self.font.render(self.text, True, self.text_base)
        text_len = text_img.get_width()

        # Affichage du bouton & du texte
        self.screen.blit(self.current_button, (self.x - self.button_orange.get_width()//3, self.y - self.button_orange.get_width()//11))
        self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y))
    
    
    def check_button(self, event):
        # Méthode pour vérifier l'état du bouton (hover, clic, relâchement) et retourner une action si nécessaire
        action = False
        pos = pygame.mouse.get_pos()

        # Changement de couleur du texte du bouton lorsqu'il est survolé
        if self.button_rect.collidepoint(pos):
            self.current_button = self.button_orange_souris
        else:
            self.current_button = self.button_orange

        # Vérification du clic de la souris
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button_rect.collidepoint(pos): self.clic = True
        if self.clic:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.button_rect.collidepoint(pos):
                self.current_button = self.button_click
                action = True

        # Réinitialisation de l'état du bouton après le clic
        if action == True:
            self.clic = False
            
        return action
