import pygame

########################################################
"""
La classe Bouton permet de créer des boutons interactifs avec des images et du texte.
"""
########################################################

class Bouton:
    def __init__(self, x, y, image_path, image_path_selected,texte, action=None, taille_texte = 30,  button_width=100, button_height=40):
        self.rect = pygame.Rect(x, y, 100, 40)
        self.image = pygame.image.load(image_path)
        self.image_selected = pygame.image.load(image_path_selected)
        self.image = pygame.transform.scale(self.image, (button_width, button_height))
        self.image_selected = pygame.transform.scale(self.image_selected, (button_width, button_height))
        
        self.is_selected = False
        self.x=x ; self.y=y
        self.width=button_width ; self.height=button_height
        
        self.police = pygame.font.Font(None, taille_texte)
        self.action = action
        
        # Texte des boutons
        self.texte_sauvegarder = self.police.render(texte, True, (0,0,0))
        

    def afficher(self, surface):
        if self.survol():
            surface.blit(self.image_selected, (self.x, self.y))
        else:
            surface.blit(self.image, (self.x, self.y))
        texte_rect = self.texte_sauvegarder.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(self.texte_sauvegarder, texte_rect)


    def survol(self):
        x, y = pygame.mouse.get_pos()
        if self.x < x < self.x+self.width and self.y < y < self.y+self.height:
            return True
        return False


    def set_selected(self, selected):
        self.is_selected = selected


    def check_button(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.x < x < self.x+self.width and self.y < y < self.y+self.height:
                self.set_selected(True)
                return True
        self.set_selected(False)
        return False
