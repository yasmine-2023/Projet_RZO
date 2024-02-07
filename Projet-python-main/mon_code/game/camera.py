import pygame as pg 

########################################################
"""
La classe Camera définit un système de caméra pour le mouvement et le zoom dans une fenêtre.
"""
########################################################

class Camera:
    def __init__(self, longueur, hauteur):
        self.longueur = longueur
        self.hauteur = hauteur

        self.mouvement = pg.Vector2(0, 0) # vecteur pour la position de la souris
        self.dx = 0 ; self.dy = 0
        self.speed = 20
        
        self.zoom = 1.0  # Facteur de zoom initial
        self.zoom_speed = 0.1  # Vitesse de zoom
        
    def update(self):
        self.deplacement()
        self.fzoom()
        self.modification_var()

        # Update du mouvement (x, y) en fonction du zoom
        self.mouvement.x += self.dx
        self.mouvement.y += self.dy

    def deplacement(self):
        mouse_pos = pg.mouse.get_pos()

        # Pour le x :
        if mouse_pos[0] > self.longueur*0.97: # si la souris se trouve a 97% de la largeur de la fenetre
            self.dx = -self.speed # deplacement a GAUCHE
        elif mouse_pos[0] < self.longueur*0.03: # si la souris se trouve a 3% de la largeur de la fenetre
            self.dx = +self.speed # deplacement a DROITE
        else:
            self.dx = 0

        # Pour le y :
        if mouse_pos[1] > self.hauteur*0.97: # si la souris se trouve a 97% de la hauteur de la fenetre
            self.dy = -self.speed # deplacement en HAUT
        elif mouse_pos[1] < self.hauteur*0.03: # si la souris se trouve a 3% de la hauteur de la fenetre
            self.dy = +self.speed # deplacement en BAS
        else:
            self.dy = 0

    def fzoom(self):
        keys = pg.key.get_pressed()
        # Gestion du zoom avec les touches fleches
        if keys[pg.K_UP]:  # Zoom avant 
            self.zoom *= (1.0 + self.zoom_speed)
        if keys[pg.K_DOWN]:  # Zoom arriere
            self.zoom /= (1.0 + self.zoom_speed)
        self.zoom = max(0.1, min(3.0, self.zoom))

    def modification_var(self):
        keys = pg.key.get_pressed()
        # Gestion de la vitesse avec les touches t et g
        if keys[pg.K_t]:  
            self.speed += 1
            self.speed = min(50, self.speed) # Limiter la vitesse de deplacement
        if keys[pg.K_g]:  
            self.speed -= 1
            self.speed = max(5, self.speed) # Limiter la vitesse de deplacement

        # Gestion de la vitesse avec les touches y et h
        if keys[pg.K_y]:  
            self.zoom_speed += 0.01
            self.zoom_speed = min(1.5, self.zoom_speed) # Limiter la vitesse de zoom
        if keys[pg.K_h]: 
            self.zoom_speed -= 0.01
            self.zoom_speed = max(0.05, self.zoom_speed) # Limiter la vitesse de zoom
