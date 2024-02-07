import pygame

########################################################
"""
Classe Bouton_on_off pour créer des boutons bascules avec des images on/off. 
Permet de changer l'état du bouton lorsqu'il est cliqué.
"""
########################################################

class Bouton_on_off:
    def __init__(self, x, y, image_on, image_off, value=True):
        # Initialise un bouton bascule avec des images on/off.
        
        # Chemins vers les images représentant l'état activé et désactivé du bouton.
        self.image_on = pygame.image.load(image_on)
        self.image_off = pygame.image.load(image_off)

        self.image_on = pygame.transform.scale(self.image_on, (80, 30)) 
        self.image_off = pygame.transform.scale(self.image_off, (80, 30))

        # État initial du bouton (True pour activé, False pour désactivé).
        self.value = value
        
        # Position du bouton sur l'écran.
        self.x=x ; self.y=y
        self.width=self.image_on.get_width() ; self.height=self.image_on.get_height()
        

    def afficher(self, surface):
        # Affiche le bouton sur une surface en utilisant l'image correspondante à son état.
        if self.value:
            surface.blit(self.image_on, (self.x, self.y))
        else:
            surface.blit(self.image_off, (self.x, self.y))


    def set_selected(self, selected):
        # Définit l'état sélectionné du bouton (non utilisé dans le code fourni).
        self.is_selected = selected


    def check_button(self, event):
        # Vérifie si le bouton est cliqué lorsqu'un événement de souris se produit, puis change son état.
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.x < x < self.x+self.width and self.y < y < self.y+self.height:
                self.value=not self.value
                return True
        return False
                
        