import pygame as pg
import sys
import math

from game.world import *
from game.settings import *
from game.camera import Camera
from game.jeu import *
from game.methods import *
from game.menu_pause import *
from game.boutton import *
from game.menu import *
from game.ftRZO import bob_joueursAdverses
 

########################################################
"""
La classe Game gère le déroulement du jeu, intégrant le monde, la caméra, et les éléments de jeu.
"""
########################################################

class Game:
    def __init__(self, screen, clock,jeu, world):
        # Initialisation de l'objet Game
        self.screen = screen
        self.clock = clock
        self.largeur, self.hauteur = self.screen.get_size()

        # Pour le monde, la camera et le jeu
        self.world = world
        self.camera = Camera(self.largeur, self.hauteur)
        self.jeu=jeu

        # Pour la deuxième option pour faire pause
        self.draw_pause_v2=False
        # Pour la barre des bobs
        self.characteristic_bob = "Energie" # Caractéristique par défaut pour l'affichage de la barre des bob

        # Variable pour savoir si nous faisons le rendering
        self.rendering = False

        self.nb_bob = 0 ; self.nb_food = 0

        self.settings_display = False

        self.elapsed_time = 0

        # Gerer un affichage fluide avec le déplacement des bobs
        self.automatic_execution_interval = 500  # Intervalle de 0.5 seconde en millisecondes
        self.last_automatic_execution_time = pg.time.get_ticks() - self.automatic_execution_interval  # Initialiser le temps pour permettre la première exécution

        # Gerer le mode automatic / non automatic
        self.automatic_mode = True
        self.n_key_pressed_time = 0
        self.automatic_mode_toggle_interval = 200
      

    def set_parametres(self, N, M,ticks_day,nb_bobs,reproduction_parthenogenese_activation,reproduction_sexuelle_activation,foods_jour,Mutv, Mut_m, Mut_mem, Mut_p,  **d):
        self.jeu.set_parametres(N, M, ticks_day, nb_bobs,reproduction_parthenogenese_activation,reproduction_sexuelle_activation, foods_jour,Mutv, Mut_m, Mut_mem, Mut_p,)
        self.world.set_parametres(N, M)
    def set_jeu(self, jeu):
        self.jeu=jeu


    def gameOver_screen(self , screen):
        game_over_image = pg.image.load("./mon_code/assets/graphics/gameover.png")
        game_over_image = pg.transform.scale(game_over_image, (500,300))
        
        self.button_return = Bouton(50, self.hauteur-70-200,"./mon_code/assets/graphics/bouton.png", "./mon_code/assets/graphics/bouton2.png", "Menu principal",button_width=160, button_height=40 )
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        pg.quit()
                        sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # Check if the mouse click is inside the button
                    if self.button_return.check_button(event):
                        return "main menu"
              
            screen.blit(game_over_image,(self.screen.get_width()/3,self.screen.get_height()/3))
            self.button_return.afficher(self.screen)
            pg.display.flip()
            self.clock.tick(60)


    def events(self):
        current_time = pg.time.get_ticks()
        # Méthode pour gérer les événements du jeu
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                  self.playing=False
                  return "pause"
                if event.key==pg.K_q:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_x:
                    self.playing=False
                    self.draw_pause_v2 = not self.draw_pause_v2
                    return "pause_v2"
                if event.key == pg.K_r:
                    self.rendering = not self.rendering
                if event.key == pg.K_o:
                    self.settings_display = not self.settings_display
                if event.key == pg.K_b:
                    self.automatic_mode = not self.automatic_mode 
                if event.key == pg.K_n and not self.automatic_mode: # mode non auto : appuie sur "n" = un tick
                    current_time = pg.time.get_ticks()
                    if current_time - self.n_key_pressed_time > self.automatic_mode_toggle_interval:
                        self.n_key_pressed_time = current_time
                        if not self.automatic_mode:
                            self.jeu.jouer2()
                            self.jeu.jouer()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_n:
                    self.n_key_pressed_time = 0
    
            self.update_characteristic(event)

                  
    def update(self):
        # Méthode pour mettre à jour l'état du jeu
        self.camera.update()
    
    def run(self):
        # Méthode principale pour exécuter le jeu
        self.playing = True
        self.load_sun_moon_app()
        
        while self.playing:
            next=self.events() # pour quitter
            self.clock.tick(60) # nombre de FPS
            self.update() # pour initialiser

            current_time = pg.time.get_ticks()

            # Pour gerer le rendering
            if not self.rendering: 
                self.draw() # pour dessiner la map
            else: self.draw_rendering_img(); 
            
            if (current_time - self.last_automatic_execution_time >= self.automatic_execution_interval) and self.automatic_mode:
                self.last_automatic_execution_time = current_time
                self.jeu.jouer2()
                self.jeu.jouer()

            if self.nb_bob == 0:
                next = self.gameOver_screen(self.screen)
                self.playing=False
        
        return next


    def load_sun_moon_app(self):
        global sun_moon
        sun_moon = SunMoonDrawingApp(self.screen, self.jeu.get_tick_jour())


    def dessiner_grille(self):         
        self.screen.fill(self.calculate_background_color(self.jeu.get_tick(), self.jeu.get_tick_jour())) #(135,206,235)
        sun_moon.draw_sun_moon(self.jeu.get_tick())
        
        # Dessiner la grille
        for x in range(self.world.grille_x): #on parcours nos lignes
            for y in range(self.world.grille_y): #on parcours nos colonnes
                self.world.dessiner_tuile(x, y, self.screen, self.camera.mouvement.x, self.camera.mouvement.y, self.camera.zoom)
  

    def draw(self): 
        n_bob, n_food = 0,0
        self.dessiner_grille()

        # Desinner la barre noir pour les options :
        pg.draw.rect(self.screen, barre_couleur_opt, (barre_position_x_opt, barre_position_y_opt, self.screen.get_width(), self.screen.get_height() - self.screen.get_height()*0.96))
        
        for case, elmts in self.jeu.world.items():
            i,j=case                            
            for k in elmts.keys():
                if k=="bob":
                    for num, bob in enumerate(self.jeu.world[case]["bob"]): 
                        delta_x=num*(3/8)/(len(self.jeu.world[case]["bob"]))   
                        delta_y= num*(1/4)/(len(self.jeu.world[case]["bob"]))  

                        # Dessiner les bobs : 
                        if bob.eSpawn >0:                                                                 
                            self.world.dessiner_bob(i, j, self.screen, self.camera.mouvement.x, self.camera.mouvement.y, self.camera.zoom, bob.get_mass(), delta_x, delta_y)                                    
                        # Dessiner la barre au dessus de bob :
                        self.world.dessiner_barre_bob_info(self.screen, i, j, bob, self.camera.zoom, self.camera.mouvement.x, self.camera.mouvement.y, self)
                        n_bob+=1
                
                if k=="nourriture":                    
                    self.world.dessiner_nourriture(i,j, self.screen,self.camera.mouvement.x, self.camera.mouvement.y, self.camera.zoom)
                    n_food+=1

        self.nb_bob, self.nb_food = n_bob, n_food
        liste_info_bob= bob_joueursAdverses()
        for info in liste_info_bob:
            x,y,masse=info
            self.world.dessiner_bob_adversaire(x, y, self.screen, self.camera.mouvement.x, self.camera.mouvement.y, self.camera.zoom, masse, 0, 0)

            

 
        # Pour déssiner la barre d'info des jours et du cycle jour/nuit
        self.world.draw_day_night_bar(self.screen, self.jeu.get_tick(), self.jeu.get_tick_jour())
        self.world.draw_day_count(self.screen, self.jeu.get_jour())
            
        if self.draw_pause_v2: # Pour afficher le "PAUSE" dans le pause_v2
            pause_image_draw = pause_image
            pause_image_draw = pg.transform.scale(pause_image, (pause_image.get_width()*(0.3/2), pause_image.get_height()*(0.3/2)))
            self.screen.blit(pause_image_draw,((self.screen.get_width()//2 - pause_image_draw.get_width()//2, self.screen.get_height()//20)))
              
        if self.settings_display: # Affichage de la barre des paramètres
            draw_texte(self.screen, '\'ECHAP\' : menu      \'X\' : freeze   \'R\' : rendering   \'B\' : aumatic_mode      \'E\' : Energie   \'M\' : Masse   \'V\' : Vélocité   \'A\' : Age', 25, (255,255,255), (10, 10))
        else : # Affichage de 'O' = paramètre
            draw_texte(self.screen, '\'O\' : options', 25, (255, 255, 255), (10, 10))

        # Pour le nombre de bob
        draw_texte(self.screen, f'nb bob = {self.nb_bob}', 25, (255, 255, 255), (10, self.screen.get_height() - 50))
        # Pour le nombre de food
        draw_texte(self.screen, f'nb food = {self.nb_food}', 25, (255, 255, 255), (10, self.screen.get_height() - 30))
        # Pour le zoom speed
        draw_texte(self.screen, f'v.moov = {self.camera.speed}    v.zoom = {self.camera.zoom_speed}', 25, (255, 255, 255), (self.largeur - 240, 10))

        # A chaque fin de boucle on actualise notre map
        pg.display.flip()


    def draw_rendering_img(self):
        rendering_image_draw = rendering_image
        rendering_image_draw = pg.transform.scale(rendering_image, (rendering_image.get_width()*0.5, rendering_image.get_height()*0.5))
        self.screen.blit(rendering_image_draw,((self.screen.get_width()//2 - rendering_image_draw.get_width()//2, self.screen.get_height()//20)))
        
        pg.display.flip()
    
    
    def change_characteristic(self, new_characteristic):
        # Changer la caractéristique
        if new_characteristic in ["Energie", "Masse", "Vitesse", "Age", "Perception"]:
            self.characteristic_bob = new_characteristic


    def update_characteristic(self, event): 
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                self.change_characteristic("Energie")
            if event.key == pg.K_m:
                self.change_characteristic("Masse")
            if event.key == pg.K_v:
                self.change_characteristic("Vitesse")
            if event.key == pg.K_a:
                self.change_characteristic("Age")
            if event.key == pg.K_p:
                self.change_characteristic("Perception")


    def get_characteristic(self):
        return self.characteristic_bob


    def calculate_background_color(self, tick, tick_day):
        adjusted_tick_day = tick_day*2
        daylight_color = (135, 206, 250)  # Bleu clair pour la journée
        night_color = (0, 0, 139)         # Bleu foncé pour la nuit

        time_ratio = tick / adjusted_tick_day
        alpha = abs(math.sin(2 * math.pi * time_ratio))
        blended_color = (
            int(daylight_color[0] * alpha + night_color[0] * (1 - alpha)),
            int(daylight_color[1] * alpha + night_color[1] * (1 - alpha)),
            int(daylight_color[2] * alpha + night_color[2] * (1 - alpha)))
        
        return blended_color