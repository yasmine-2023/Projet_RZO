from os import path
import pygame as pg
import os 

########################################################
"""
Le module `methods` contient des variables du jeu (comme des tailles de boutton ou encore et couleur...)
"""
########################################################

################################################################################

TAILLE_TUILE = 66
WORLD_X = 100
WORLD_Y = 100

################################################################################

# Paramètres barre bob
font_size = 16 ; font_color = (0, 0, 0)
bar_width_bob = 50 ; bar_height_bob = 8
border_color = (0, 0, 0)

# Paramètre pour barre jour/nuit 
bar_width_jn = 400 ; bar_height_jn = 30
background_color = (255, 255, 255)
day_color = (0, 128, 255)  # Bleu clair
night_color = (0, 0, 128)  # Bleu foncé

################################################################################

# Buttons
HEIGHT_BUTTON = 50
WIDTH_BUTTON = 300
GAP = 75     
#FONT_SIZE = 15

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (238, 130, 238)
MARRON = (165, 42, 42)
GOLD = (255, 215, 200)
YELLOW_LIGHT = (249, 231, 159)
BEIGE = (255, 253, 208)
GREEN_DARK = (9, 48, 22)
BLUE_SKY = (122, 215, 255)
PINK = (255, 88, 150)
PURPLE = (128, 0, 128)

# background_of_menu  = pg.image.load("assets/graphics/background.jpg")
chemin=os.path.join( "mon_code", "assets", "graphics", "background.jpeg")
background_of_menu = pg.image.load(chemin)

bouton_orange = pg.image.load("./mon_code/assets/graphics/bouton_orange.png")
bouton_orange_souris = pg.image.load("./mon_code/assets/graphics/bouton_orange_souris.png")
bouton_rouge = pg.image.load("./mon_code/assets/graphics/bouton_rouge.png")
pause_image = pg.image.load("./mon_code/assets/graphics/pause_image.png")
rendering_image = pg.image.load("./mon_code/assets/graphics/rendering_image.png")
                
paths = path.dirname("./song")
music_menu = path.join(path.join(paths, "./song"), "song.wav")

################################################################################

# Définir les propriétés de la barre
barre_couleur_opt = (0, 0, 0)  # Noir
barre_position_x_opt = 0
barre_position_y_opt = 0