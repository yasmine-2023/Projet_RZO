import pygame as pg 
import os 
import math

from game.settings import *

########################################################
"""
La classe World gère la partie graphique du jeu
"""
########################################################


# interface graphique
class World:
    def __init__(self, grille_x, grille_y, largeur, hauteur):
        self.grille_x = grille_x #taille de la grille en x
        self.grille_y = grille_y #taille de la grille en y
        self.largeur = largeur ; self.hauteur = hauteur 
        
        # Chargement des images
        self.img_nourriture= self.chrg_image("tile_0047.png")
        self.img_bob= self.chrg_image("character_0005.png")
        self.img_tuile=self.chrg_image("grass.png")
        self.img_bob_adversaire=self.chrg_image("bob_vert.png")
        self.img_nourriture_adv= self.chrg_image("nourriture_adv.png")
      

    def set_parametres(self,N, M, **d):
        self.grille_x=int(N)
        self.grille_y=int(M)
   

    def dessiner_nourriture(self, i ,j, fenetre, camera_x, camera_y, zoom):  
        img_nourriture_z=pg.transform.scale(self.img_nourriture, ((self.img_nourriture.get_width()*zoom), (self.img_nourriture.get_height()*zoom)))   
        img_tuile_z=pg.transform.scale(self.img_tuile, ((self.img_tuile.get_width()*zoom), (self.img_tuile.get_height()*zoom)))
        x,y=self.calculer_x_y(i,j)
        fenetre.blit(img_nourriture_z, 
                        (x*zoom + fenetre.get_width()/2+img_tuile_z.get_width()/2-img_nourriture_z.get_width()/2 + camera_x,  
                        y*zoom + img_tuile_z.get_height()/4- img_nourriture_z.get_height()/2 + camera_y))
        

    def dessiner_bob(self, i ,j, fenetre, camera_x, camera_y, zoom, masse, delta_x, delta_y): 
        masse=(masse)**(1/3)
        img_bob_z=pg.transform.scale(self.img_bob, ((self.img_bob.get_width()*zoom*masse), (self.img_bob.get_height()*zoom*masse)))          
        img_tuile_z=pg.transform.scale(self.img_tuile, ((self.img_tuile.get_width()*zoom), (self.img_tuile.get_height()*zoom)))
        x,y=self.calculer_x_y(i,j)
        fenetre.blit(img_bob_z, 
                        (x*zoom + fenetre.get_width()/2 +img_tuile_z.get_width()/2+img_tuile_z.get_width()*delta_x-img_bob_z.get_width()/2+ camera_x,  
                        y*zoom +img_tuile_z.get_height()/8+img_tuile_z.get_height()*delta_y-img_bob_z.get_height()/2+ camera_y))    



    def dessiner_bob_adversaire(self, i ,j, fenetre, camera_x, camera_y, zoom, masse, delta_x, delta_y):
        masse=(masse)**(1/3)
        img_bob_z=pg.transform.scale(self.img_bob_adversaire, ((self.img_bob_adversaire.get_width()*zoom*masse), (self.img_bob_adversaire.get_height()*zoom*masse)))          
        img_tuile_z=pg.transform.scale(self.img_tuile, ((self.img_tuile.get_width()*zoom), (self.img_tuile.get_height()*zoom)))
        x,y=self.calculer_x_y(i,j)
        fenetre.blit(img_bob_z, 
                        (x*zoom + fenetre.get_width()/2 +img_tuile_z.get_width()/2+img_tuile_z.get_width()*delta_x-img_bob_z.get_width()/2+ camera_x,  
                        y*zoom +img_tuile_z.get_height()/8+img_tuile_z.get_height()*delta_y-img_bob_z.get_height()/2+ camera_y))    


#################
    def dessiner_nourriture_adversaire(self, i ,j, fenetre, camera_x, camera_y, zoom):  
        img_nourriture_z=pg.transform.scale(self.img_nourriture_adv, ((self.img_nourriture.get_width()*zoom), (self.img_nourriture.get_height()*zoom)))   
        img_tuile_z=pg.transform.scale(self.img_tuile, ((self.img_tuile.get_width()*zoom), (self.img_tuile.get_height()*zoom)))
        x,y=self.calculer_x_y(i,j)
        fenetre.blit(img_nourriture_z, 
                        (x*zoom + fenetre.get_width()/2+img_tuile_z.get_width()/2-img_nourriture_z.get_width()/2 + camera_x,  
                        y*zoom + img_tuile_z.get_height()/4- img_nourriture_z.get_height()/2 + camera_y))
        


    def dessiner_tuile(self, i, j,fenetre, camera_x, camera_y, zoom):
        img = pg.transform.scale(self.img_tuile, ((self.img_tuile.get_width()*zoom), (self.img_tuile.get_height()*zoom)))
        x, y=self.calculer_x_y(i, j)
        fenetre.blit(img, (x*zoom + fenetre.get_width()/2 +camera_x, y*zoom +camera_y)) #on affiche, sur nos surfaces par un block en les centrant correctement selon x et y    
      

    def calculer_x_y(self, ligne, colonne):
        rect = [(ligne*(self.img_tuile.get_width()/2), colonne*(self.img_tuile.get_width()/2)),                                 # coin supÃ©rieur gauche
                (ligne*(self.img_tuile.get_width()/2) + (self.img_tuile.get_width()/2), colonne*(self.img_tuile.get_width()/2)),                  # coin supÃ©rieur droit 
                (ligne*(self.img_tuile.get_width()/2) + (self.img_tuile.get_width()/2), colonne*(self.img_tuile.get_width()/2) + (self.img_tuile.get_width()/2)),   # coin infÃ©rieur droit 
                (ligne*(self.img_tuile.get_width()/2), colonne*(self.img_tuile.get_width()/2) + (self.img_tuile.get_width()/2))]                  # coin infÃ©rieur gauche
        
        # On transforme notre rectangle en rectangle ISOMETRIQUE
        iso_poly = [self.cartesien_to_iso(x, y) for (x, y) in rect]

        minx = min(x for x,_ in iso_poly)
        miny = max(y for _,y in iso_poly)
        return (minx, miny)
    

    def cartesien_to_iso(self, x, y):
        # Effectue une transformation des coordonnes cartesiennes en coordonnees isometriques
        iso_x = x-y
        iso_y = (x+y)/2
        return (iso_x, iso_y)
  

    def chrg_image(self, img):
        # Pour charger les images
        chemin=os.path.join( "mon_code","assets", "graphics", img)
        image = pg.image.load(chemin).convert_alpha()
                
        return image


    # Methode pour afficher la barre des bobs
    def dessiner_barre_bob_info(self, screen, bob_x, bob_y, bob, zoom, camera_x, camera_y, game):
        # Calculer les coordonnees
        x, y = self.calculer_x_y(bob_x, bob_y)
        x_screen = x * zoom + screen.get_width() / 2 + camera_x + 40 * zoom  # Ajuster pour le zoom
        y_screen = y * zoom + camera_y - 5 * zoom  # Ajuster pour le zoom

        border_rect = pg.Rect(x_screen, y_screen, bar_width_bob * zoom + 2, bar_height_bob * zoom + 2)
        pg.draw.rect(screen, border_color, border_rect)

        # Determiner quelle caracteristique afficher
        if game.get_characteristic() == "Energie":
            value = bob.get_eSpawn()
        elif game.get_characteristic() == "Masse":
            value = bob.get_mass()
        elif game.get_characteristic() == "Vitesse":
            value = bob.get_velocity()
        elif game.get_characteristic() == "Age":
            value = bob.get_age()
        elif game.get_characteristic() == "Perception":
            value = bob.get_perception()
        else:
            raise ValueError("CaractÃ©ristique invalide")

        # Calcul de la max_value 
        if game.get_characteristic() in ["Masse"]: 
            max_value = bob.get_mass()
        elif game.get_characteristic() in ["Vitesse"]: 
            max_value = bob.get_velocity()
        elif game.get_characteristic() in ["Age"]: 
            max_value = bob.get_age()
        elif game.get_characteristic() in ["Perception"]: 
            max_value = bob.get_perception()
        else: 
            max_value = bob.get_emax()

        # Dessiner la barre de caracteristique
        if game.get_characteristic() == "Energie":
            if value == max_value:
                bar_width = int(bar_width_bob * zoom)  # La barre est pleine si l'energie est egal a l'energie max
            else:
                # Ajuster la longueur de la barre en fonction de la diffÃ©rence entre l'energie max et l'energie actuelle
                bar_width = int(bar_width_bob * ((value) / max_value) * zoom)
        elif game.get_characteristic() == "Age" or game.get_characteristic() == "Perception":
            bar_width = int(bar_width_bob * zoom)  # autre calcul pour la caractéristique "Age"
        else:
            bar_width = int(bar_width_bob * (value / max_value) * zoom)  # Pour les autres caracteristiques

        # Ajuster la longueur de la barre pour qu'elle soit egal a la largeur du rectangle noir
        bar_width = min(bar_width, bar_width_bob * zoom)
        bar_rect = pg.Rect(x_screen, y_screen, bar_width, bar_height_bob * zoom)  # Normaliser en fonction du max_value
        pg.draw.rect(screen, (0, 255, 0), bar_rect)

        # Calcule la taille de police en fonction du zoom
        base_font_size = int(font_size * zoom)
        font = pg.font.Font(None, base_font_size)

        # Arrondir la valeur a 2 chiffres apres la virgule
        rounded_value = round(value, 2)

        text = font.render(f"{game.get_characteristic().capitalize()} : {rounded_value}", True, font_color)
        # Ajuste la position du texte en fonction du zoom
        text_rect = text.get_rect(center=(x_screen + 22 * zoom, y_screen - 6 * zoom))
        screen.blit(text, text_rect)


    # Methode pour afficher la barre de progression jour/nuit
    def draw_day_night_bar(self, screen, tick, tick_jour):
        progress = tick / tick_jour
        font = pg.font.Font(None, 36)
        
        # Ajuster les coordonnÃ©es y pour dÃ©placer vers le bas de l'Ã©cran
        x_center = screen.get_width() ; y_center = screen.get_height() - screen.get_height()//35
        
        bar_rect = pg.Rect((x_center - bar_width_jn) // 2, y_center - bar_height_jn // 2, int(bar_width_jn * progress), bar_height_jn)
        
        if progress <= 0.5:
            pg.draw.rect(screen, day_color, bar_rect)
        else:
            pg.draw.rect(screen, night_color, bar_rect)

        # Dessiner le rectangle noir vide avec un contour blanc
        outline_rect = pg.Rect((screen.get_width() - bar_width_jn) // 2, y_center - bar_height_jn // 2, bar_width_jn, bar_height_jn)
        pg.draw.rect(screen, (0, 0, 0), outline_rect, 2)  # Contour blanc, Ã©paisseur de 2 pixels


    # Methode pour afficher le texte du compteur de journÃ©e
    def draw_day_count(self, screen, jour):
        x_center = screen.get_width() ; y_center = screen.get_height() - screen.get_height()//15
        font = pg.font.Font(None, 36)
        text = font.render(f"Jour {jour}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(x_center // 2, y_center))
        screen.blit(text, text_rect)



########################################################
"""
La classe SunMoonDrawingApp est un ajout graphique pour avoir un cycle jour/nuit avec un soleil et une lune
"""
########################################################

class SunMoonDrawingApp:
    def __init__(self, screen, ticks_per_day):
        self.screen = screen
        self.sun_angle = 0 ; self.moon_angle = math.pi  # lune commence à l'opposé du soleil
        self.sun_x = 0 ; self.sun_y = 0
        self.moon_x = 0 ; self.moon_y = 0
        self.zoom_scale = 2
        self.adjusted_tick_day = ticks_per_day*2

        # Chargemement des images
        self.sun_img = pg.image.load('./mon_code/assets/graphics/sun.png')
        self.moon_img = pg.image.load('./mon_code/assets/graphics/moon.png')
        
    def draw_sun_moon(self, tick):
        sun_x, sun_y = self.calculate_sun_position(tick)
        sun_image = pg.transform.scale(self.sun_img, (100, 100))
        sun_rect = sun_image.get_rect()
        self.screen.blit(sun_image, (sun_x - sun_rect.width // 2, sun_y - sun_rect.height // 2))
            
        moon_x, moon_y = self.calculate_moon_position(tick)
        moon_image = pg.transform.scale(self.moon_img, (80, 80))
        moon_rect = moon_image.get_rect()
        self.screen.blit(moon_image, (moon_x - moon_rect.width // 2, moon_y - moon_rect.height // 2))

    def calculate_sun_position(self, tick):
        time_ratio = tick / self.adjusted_tick_day
        self.sun_angle = 4 * math.pi * time_ratio
        initial_sun_angle = math.pi / 2

        self.sun_x = 400 + (self.screen.get_width()//2) * math.cos(self.sun_angle + initial_sun_angle) + self.screen.get_width() // 4
        self.sun_y = 200 + (self.screen.get_height()//2) * math.sin(self.sun_angle + initial_sun_angle) + self.screen.get_height() // 4

        return self.sun_x, self.sun_y

    def calculate_moon_position(self, tick):
        time_ratio = tick / self.adjusted_tick_day
        self.moon_angle = math.pi + 4 * math.pi * time_ratio  # ajout de pi pour être à l'opposé du soleil
        initial_moon_angle = math.pi / 2

        self.moon_x = 400 + (self.screen.get_width()//2) * math.cos(self.moon_angle + initial_moon_angle) + self.screen.get_width() // 4
        self.moon_y = 200 + (self.screen.get_height()//2) * math.sin(self.moon_angle + initial_moon_angle) + self.screen.get_height() // 4

        return self.moon_x, self.moon_y


   
