import pygame as pg
from game.game import *
from game.menu import *
from game.formulaire import *
from game.methods import *
from game.bob import *


########################################################
"""
La Lanceur permet de lancer le jeu
"""
########################################################



class Lanceur():
    def __init__(self):
       
        pg.init()
        pg.mixer.init()

        # Variable pour savoir si on joue / pause
        self.playing = False
        running = True
        
        # Les variables 
        self.screen = pg.display.set_mode((1250,600))
        self.clock = pg.time.Clock()

        self.current="main menu"

        self.active_option = None
        self.input_value = ""
        
        self.default_options={'N': '5', 'M': '5', 'ticks_day': '100', 'energy_food': '100', 'foods_jour': '5', 'nb_bobs': '1', 'eSpawn': '100', 'eMax': '200', 'eMother': '150', 'eBirth': '50',"e_SR":'150',"eBirth_SR":"100", 'Mutv': '0.1', 'Mut_m': '0.1', 'Mut_p': '1', 'Mut_mem': '1', 'velocity': '0', 'mass': '1', 'perception_score': '6', 'initial_memory_points': '0', 'reproduction_parthenogenese_activation': True, "age":False, "reproduction_sexuelle_activation":False}
        self.labels_formulaire=[[("N","Height"), ("M", "Width"), ("ticks_day", "Ticks per day")], [("energy_food", "Energy per food"),("foods_jour", "Number of Food per day"), ("nb_bobs", "Initial Bob number")], [("eSpawn", "Initial energy of Bob"), ("eMax", "Maximum energy of bob"), ("eMother", "Energy lost by the mother"),("e_SR", "Energie for SR"), ("eBirth", "Initial energy of Birth"),("eBirth_SR", "Initial energy of Birth SR")], [("Mutv", "Mutation rate for velocity"), ("Mut_m", "mutation rate for mass"), ("Mut_p", "mutation rate for perception"), ("Mut_mem", "mutation rate for memory")], [("velocity", "Initial velocity"), ("mass", "Initial mass"), ("perception_score", "Initial perception score"), ("initial_memory_points", "initial memory points")]]
        self.labels_formulaire_pause=[[("N","Height"), ("M", "Width"), ("ticks_day", "Ticks per day")], [("energy_food", "Energy per food"),("foods_jour", "Number of Food per day")], [("eSpawn", "Initial energy of Bob"), ("eMax", "Maximum energy of bob"), ("eMother", "Energy lost by the mother"),("e_SR", "Energie for SR"), ("eBirth", "Initial energy of Birth"),("eBirth_SR", "Initial energy of Birth SR")], [("Mutv", "Mutation rate for velocity"), ("Mut_m", "mutation rate for mass"), ("Mut_p", "mutation rate for perception"), ("Mut_mem", "mutation rate for memory")], [("velocity", "Initial velocity"), ("mass", "Initial mass"), ("perception_score", "Initial perception score"), ("initial_memory_points", "initial memory points")]]
        self.options=self.default_options
        
        self.menu=Menu(self.screen, self)
        self.formulaire=Formulaire(self.screen, self.options,self.labels_formulaire, "main menu")
         
        self.jeu=None
        self.world=None
        self.game=None
        
        self.pause=Pause_menu(self.screen, self)
        self.formulaire_pause=Formulaire(self.screen, self.options,self.labels_formulaire_pause, "game")

        self.saved_games=charger_jeu('saved_games.pickle')

        while running:
            # Boucle du jeu
            self.events()
       
        pg.exit()

   
    def events(self):
        if self.current=="main menu":
            self.current=self.menu.run()
        elif self.current=="nouvelle partie":
            self.nouvelle_partie()
            self.current=self.game.run()
        elif self.current=="formulaire":
            self.formulaire.set_parametres(self.options) 
            self.current=self.formulaire.run()
        #********************************************************************************
        elif self.current=="game":  
            self.game.draw_pause_v2 = not self.game.draw_pause_v2 if self.game.draw_pause_v2 else self.game.draw_pause_v2              
            self.current=self.game.run()
        elif self.current=="pause": 
            self.current=self.pause.run()
        elif self.current=="pause_v2":
            self.current=self.pause.run_pause_v2(self.game)
        elif self.current=="sauvegarder":
            choix, text=self.fonction(self.screen)
            if choix:
                sauvegarder_jeu(text, {"jeu":self.jeu, "parametres":self.options})
                self.current="main menu" 
            else:
                self.current="pause"
        elif self.current=="reprendre":
            self.current=self.choisir_partie_sauvegardee()
            
        elif self.current=="formulaire pause":  
            print("formulaire pause")   
            print(self.options)
            self.formulaire_pause.set_parametres(self.options)     
            self.current=self.formulaire_pause.run()

            Nourriture.set_parametres(**self.options)
            Bob.set_parametres(**self.options)
            self.game.set_parametres(**self.options)

        
    def choisir_partie_sauvegardee(self):
        self.button_supprimer = Bouton((2.5*self.screen.get_width()) // 4, 3.6*self.screen.get_height()//5,"./mon_code/assets/graphics/bouton.png", "./mon_code/assets/graphics/bouton2.png", "Supprimer", taille_texte = 24)
        self.button_charger = Bouton((2.5*self.screen.get_width()) // 4, 4*self.screen.get_height()//5, "./mon_code/assets/graphics/bouton.png", "./mon_code/assets/graphics/bouton2.png", "Charger" , taille_texte = 30)
        self.button_return = Bouton((1.1*self.screen.get_width()) // 4,4*self.screen.get_height()//5 ,"./mon_code/assets/graphics/bouton.png", "./mon_code/assets/graphics/bouton2.png", "Return" , taille_texte = 34)
        font_option = pygame.font.Font(None, 30)
        font_titre = pygame.font.Font("./mon_code/assets/graphics/arcade.ttf", 48)
    
        menu_en_cours = True
                
        fond_image = pygame.image.load("./mon_code/assets/graphics/background_sauvegarde.jpg")
        fond_image = pygame.transform.scale(fond_image, (self.screen.get_width(), self.screen.get_height())) 

        self.saved_games=charger_jeu('saved_games.pickle')

        option_selectionnee = 0  

        while menu_en_cours:
            options = list(self.saved_games.keys())
            start_index = max(0, option_selectionnee-4)
            end_index = min(len(options), start_index + 5)

            self.screen.blit(fond_image, (0, 0))
            self.button_supprimer.afficher(self.screen)
            self.button_charger.afficher(self.screen)
            self.button_return.afficher(self.screen)
            titre = font_titre.render("Les parties sauvegardees", True, (255, 255, 255))
            titre_rect = titre.get_rect(center=(self.screen.get_width() / 2, 150))
            self.screen.blit(titre, titre_rect)

            if not self.saved_games:
                texte = font_option.render("Aucune partie n est sauvegardee", True, (255, 0, 0))
                texte_rect = texte.get_rect(center=(self.screen.get_width() / 2, 200 + 50))
                self.screen.blit(texte, texte_rect)

            for i in range(start_index, end_index):
                couleur = (255, 255, 255) if i == option_selectionnee else (128, 128, 128)
                texte = font_option.render(options[i], True, couleur)
                texte_rect = texte.get_rect(center=(self.screen.get_width() / 2, 200 + (i - start_index) * 50))
                self.screen.blit(texte, texte_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif self.button_supprimer.check_button(event) and self.saved_games:
                    effacer_jeu(options[option_selectionnee])
                    del self.saved_games[options[option_selectionnee]]
                    option_selectionnee = max(0, option_selectionnee - 1)
                
                elif self.button_charger.check_button(event) and self.saved_games:
                    self.jeu=self.saved_games[options[option_selectionnee]]["jeu"]
                    self.options=self.saved_games[options[option_selectionnee]]["parametres"]
                    Bob.set_parametres(**self.options)
                    self.world=World(self.jeu.world_x,self.jeu.world_y, self.screen.get_width(), self.screen.get_height())
                    self.game=Game(self.screen, self.clock, self.jeu, self.world)
                    menu_en_cours=False
                    return "game"
                elif self.button_return.check_button(event):
                    # il faut sauvegarder saved_games
                    menu_en_cours=False
                    return "main menu"
                elif event.type == pygame.KEYDOWN and self.saved_games:
                    if event.key == pygame.K_UP:
                        option_selectionnee = (option_selectionnee - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        option_selectionnee = (option_selectionnee + 1) % len(options)

            pygame.display.flip()


    def fonction(self, screen):

        # Dimensions de la fenÃªtre
        width, height = 400, 200

        # Couleurs
        white = (255, 255, 255) ; black = (0, 0, 0)

        # Charger l'image d'arriÃ¨re-plan
        background_image = pygame.image.load("./mon_code/assets/graphics/bg.png")  # Remplacez "votre_image.jpg" par le chemin de votre image
        background_image = pygame.transform.scale(background_image, (width, height))

        self.save_button = Bouton((0.94*self.screen.get_width() ) // 2, 1.15*self.screen.get_height()//2,"./mon_code/assets/graphics/bouton.png", "./mon_code/assets/graphics/bouton2.png", "Save", taille_texte = 34, button_width=100, button_height=40)
        self.close_button = Bouton(self.screen.get_width()/2 -width/2+width - 40, self.screen.get_height()/2 -height/2+10, "./mon_code/assets/graphics/bouton_close.png", "./mon_code/assets/graphics/bouton_close2.png", "" , taille_texte = 40, button_width= 30, button_height=30)

        # CrÃ©er un rectangle reprÃ©sentant le champ de texte
        text_field_image = pygame.image.load("./mon_code/assets/graphics/champ.png")  
        text_field_image = pygame.transform.scale(text_field_image, (300, 60))

        # Police de texte
        font = pygame.font.Font(None, 30)
        text1 = font.render("Nom de la sauvegarde", True, white)
        # Texte initial dans le champ de texte
        text = ""

        # Variable pour indiquer si le champ de texte est actif
        text_active = False

        # Boucle principale
        running = True
        cursor_visible = True ; last_blink_time = pygame.time.get_ticks() 
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.save_button.check_button(event):
                        return True, text
                        # Ajoutez ici la logique pour le bouton Save
                    elif self.close_button.check_button(event):
                        return False, ""
        
                        # Ajoutez ici la logique pour le bouton Close
                    elif text_field_rect.collidepoint(event.pos):
                        text_active = not text_active  # Activer/dÃ©sactiver le champ de texte

                elif event.type == pygame.KEYDOWN:
                    if text_active:
                        if event.key == pygame.K_RETURN:
                            print("Text entered:", text)
                            text_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            # Dessiner l'image d'arrière-plan
            screen.blit(background_image, (self.screen.get_width()/2 -width/2, self.screen.get_height()/2 -height/2))
            screen.blit(text1,(1.05*self.screen.get_width()/2 -width/2, 1.1*self.screen.get_height()/2 -height/2.2))
            # Dessiner le rectangle représentant le champ de texte
            text_field_rect = screen.blit(text_field_image, (self.screen.get_width()/2 -width/2+50, 1.1*self.screen.get_height()/2 -height/2+50))

            # Dessiner le texte dans le rectangle
            text_surface = font.render(text, True, white)
            screen.blit(text_surface, (text_field_rect.x + 10, text_field_rect.y + 10))

            # Dessiner le curseur clignotant
            current_time = pygame.time.get_ticks()
            if current_time - last_blink_time > 500:  
                last_blink_time = current_time
                cursor_visible = not cursor_visible

            if text_active and cursor_visible:
                cursor_rect = pygame.Rect(text_field_rect.x + 10 + text_surface.get_width(), text_field_rect.y + 10, 2, text_surface.get_height())
                pygame.draw.rect(screen, white, cursor_rect)

            # Dessiner les images des boutons
            self.save_button.afficher(self.screen)
            self.close_button.afficher(self.screen)

            # Mettre Ã  jour l'affichage
            pygame.display.flip()


    def nouvelle_partie(self):
        Bob.set_parametres(**self.options)
        self.jeu=Jeu( **self.options)
        self.world=World(int(self.options["N"]), int(self.options["M"]), self.screen.get_width(), self.screen.get_height())
        self.game=Game(self.screen, self.clock, self.jeu, self.world)
        self.jeu.tick_jour_renitialisation()
        

    def update_paused(self):
        self.pause = not self.pause
    def getscreen(self):
        return self.screen
    def getclock(self):
        return self.clock
    def create_new_game(self):
        self.jeu = Jeu()
    def ispause(self): return self.pause
    def getpause(self): return self.pause
    def isplaying(self): return self.playing



Lanceur()

