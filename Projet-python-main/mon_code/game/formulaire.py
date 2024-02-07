import pygame
import sys
from game.methods import *
from game.boutton import *
from game.boutton_on_off import *
 
caractere_valides_int=['1','2','3','4','5','6','7','8','9','0']
caractere_valides_float=['1','2','3','4','5','6','7','8','9','0','.']

class Formulaire:
    def __init__(self, screen, parametres,labels, previous):
        pygame.init()
        #labels
        self.labels=labels
        
        # Couleurs
        self.BLANC = (255, 255, 255) ; self.NOIR = (0, 0, 0)
        self.GRIS = (169, 169, 169) ; self.JAUNE=(255, 255,0)

        # Initialisation de Pygame
        self.largeur, self.hauteur = screen.get_width(), screen.get_height()
        self.ecran = screen
        pygame.display.set_caption("OPTIONS")
        self.police = pygame.font.Font(None, 30)
        
        # Boutons
        self.next_rect = pygame.Rect(self.largeur - 150, self.hauteur - 120, 100, 40)
        self.button_sauvegarde = Bouton((1.4*self.largeur) // 2, 3.9*self.hauteur//5,"./mon_code/assets/graphics/bouton.png", "./mon_code/assets/graphics/bouton2.png", "Save", taille_texte = 34 )
        self.button_next = Bouton((1.4*self.largeur) // 2, 4.2*self.hauteur//5, "./mon_code/assets/graphics/bouton.png", "./mon_code/assets/graphics/bouton2.png", "Next", taille_texte = 34)
        self.button_return = Bouton(0.9*self.largeur // 4, 4.2*self.hauteur//5 ,"./mon_code/assets/graphics/bouton.png", "./mon_code/assets/graphics/bouton2.png", "Return", taille_texte = 34 )
        self.fermer_rect = pygame.Rect(50, self.hauteur - 70, 100, 40)

        self.current=0
        self.previous=previous

        self.active_option = None
        self.input_value = ""

        # Charger les valeurs au demarrage
        self.options=parametres
        self.bouton_reproduction_parthenogenese=Bouton_on_off(1.2*self.largeur//2, 100 + len(self.labels[4]) * 50, "./mon_code/assets/graphics/bouton_on.png", "./mon_code/assets/graphics/bouton_off.png", self.options["reproduction_parthenogenese_activation"])
        self.bouton_reproduction_sexuelle=Bouton_on_off(1.2*self.largeur//2, 100 + (len(self.labels[4])+1) * 50, "./mon_code/assets/graphics/bouton_on.png", "./mon_code/assets/graphics/bouton_off.png", self.options["reproduction_sexuelle_activation"])
        self.bouton_age=Bouton_on_off(1.2*self.largeur//2, 100 + (len(self.labels[4])+2) * 50, "./mon_code/assets/graphics/bouton_on.png", "./mon_code/assets/graphics/bouton_off.png", self.options["age"])
        self.input_field_image = pygame.image.load("./mon_code/assets/graphics/champ.png") 
        self.input_field_image = pygame.transform.scale(self.input_field_image, (150, 30))
        
        self.custom_font = pygame.font.Font("./mon_code/assets/graphics/arcade.ttf", 36)

        self.background_image = pygame.image.load("./mon_code/assets/graphics/background_option.jpg")  
        self.background_image = pygame.transform.scale(self.background_image, (self.largeur , self.hauteur ))

        # Gerer le curseur "|" qui clignotte
        self.cursor_visible = True
        self.cursor_blink_interval = 500  # Intervalle de clignotement du curseur en millisecondes
        self.last_blink_time = pygame.time.get_ticks()


    def warning_screen(self , screen):
        font = pygame.font.Font(None , 36)
        text = font.render("Les options sont des nombres!!!", True, (255, 0, 0))
        screen.blit(text,(self.largeur//5,5*self.hauteur//8))
        pygame.display.flip()
        pygame.time.wait(1000)
    

    def valid_caractere(self , c, list):
        return c in list
        

    def run(self):
        self.active=True
        while self.active:  
            self.draw()  
            pygame.display.flip()
            self.current=self.events()
        return self.previous  
        
        
    def set_parametres(self, parametres):
        self.options= parametres    
      

    def events(self):
        # Gestion des evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Verification si la souris est sur un champ de texte
                for  i, label in enumerate(self.labels[self.current]):
                    input_field_rect = pygame.Rect(1.2*self.largeur//2, self.hauteur//8 + i * 50, 150, 30)
                    if input_field_rect.collidepoint(x, y):
                        self.active_option = label[0]
                        self.input_value = str(self.options[label[0]])

                if self.button_return.check_button(event):
                    if self.current==0:
                        self.active=False
                        return 0
                    else:
                        return self.current-1
                    
                elif self.button_next.check_button(event):
                    if self.current==len(self.labels)-1:
                        return len(self.labels)-1
                    else:
                        return self.current+1
                    
                elif self.button_sauvegarde.check_button(event):
                    self.active=False
                    return 0
                if self.current==4 :
                    if self.bouton_reproduction_parthenogenese.check_button(event):
                        self.options["reproduction_parthenogenese_activation"]=self.bouton_reproduction_parthenogenese.value
                    if self.bouton_reproduction_sexuelle.check_button(event):
                        self.options["reproduction_sexuelle_activation"]=self.bouton_reproduction_sexuelle.value
                    if self.bouton_age.check_button(event):
                        self.options["age"]=self.bouton_age.value
                
            elif event.type == pygame.KEYDOWN:
                if self.active_option is not None:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_value = self.input_value[:-1]
                    else:
                        if event.key==pygame.K_LSHIFT or event.key==pygame.K_RSHIFT :
                            pass
                        else:
                            if(self.active_option in ["eSpawn","eMax", "eMother","eBirth","Mutv","Mut_m","velocity","mass", "e_SR", "eBirth_SR"]):
                                if self.valid_caractere(event.unicode,caractere_valides_float):
                                    self.input_value +=event.unicode
                                else :
                                    self.warning_screen(self.ecran)
                            else : 
                                if self.valid_caractere(event.unicode,caractere_valides_int):
                                    self.input_value +=event.unicode
                                else :
                                    self.warning_screen(self.ecran)
                    if self.input_value :
                        self.options[self.active_option] = self.input_value
                        
        return self.current
        

    def text_input(self):
        for i, label in enumerate(self.labels[self.current]):
            # Affichage de l'option
            texte_option = self.custom_font.render(label[1], True, self.JAUNE)
            self.ecran.blit(texte_option, (self.largeur//5, self.hauteur//8 + i * 50))

            # Affichage du champ de texte
            input_field_rect = pygame.Rect(1.2*self.largeur//2,self.hauteur//8 + i * 50 , 150, 30) 
            self.ecran.blit(self.input_field_image, input_field_rect)
            
            if self.active_option == label[0]:
                texte_valeur = self.police.render(str(self.input_value), True, self.NOIR)
                text_rect = texte_valeur.get_rect()

                # Clignotement du curseur
                current_time = pygame.time.get_ticks()
                if current_time - self.last_blink_time > self.cursor_blink_interval:
                    self.last_blink_time = current_time
                    self.cursor_visible = not self.cursor_visible

                # Affichage du curseur clignotant
                if self.cursor_visible:
                    cursor_rect = pygame.Rect(1.21*self.largeur//2 + text_rect.width ,1.06*self.hauteur//8 + i * 50 , 5, text_rect.height)
                    pygame.draw.rect(self.ecran, self.NOIR, cursor_rect)
            else:
                texte_valeur = self.police.render(str(self.options[label[0]]), True, self.NOIR)
            
            # Ajustez la position du texte pour un meilleur alignement
            self.ecran.blit(texte_valeur, (1.21*self.largeur//2 ,1.06*self.hauteur//8 + i * 50))  


    def draw(self):
        self.ecran.blit(self.background_image, (0, 0))
       
        self.button_sauvegarde.afficher(self.ecran)
        self.button_next.afficher(self.ecran)
        self.button_return.afficher(self.ecran)

        self.text_input()
        
        if self.current==4:
            
            self.bouton_reproduction_parthenogenese.afficher(self.ecran)
            self.bouton_reproduction_sexuelle.afficher(self.ecran)
            self.bouton_age.afficher(self.ecran)

            texte_option = self.custom_font.render("Reproduction parthenogenesis", True, self.JAUNE)
            self.ecran.blit(texte_option, (self.largeur//5, 100 + len(self.labels[self.current]) * 50))

            texte_option = self.custom_font.render("Sexual reproduction", True, self.JAUNE)
            self.ecran.blit(texte_option, (self.largeur//5, 100 + (len(self.labels[self.current])+1) * 50))

            texte_option = self.custom_font.render("Age", True, self.JAUNE)
            self.ecran.blit(texte_option, (self.largeur//5, 100 + (len(self.labels[self.current])+2) * 50))

   
