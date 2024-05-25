from glob import glob
import random
from game.bob import *

from game.joueur import Joueur
from game.nourriture import *
from game.methods import *
from game.bob import *
from game.ftRZO import *
from game.joueur import *
from game.case import *
from game.ftRZO import Interface
#from game.traitement import *
eat_bob=0

x_start=30 
y_start=30
#global idjoueur 

class Jeu():
    def __init__(self, N, M, ticks_day,nb_bobs,foods_jour,reproduction_parthenogenese_activation,reproduction_sexuelle_activation,age, **d):        
        self.world_x=int(N)
        self.world_y=int(M)

        self.totale_nourriture=int(foods_jour)
        self.nb_bobs=int(nb_bobs)
     
        self.ticks_jour=int(ticks_day)
        self.cpt_ticks=1
        self.jour=1
        
        self.reproduction_parthenogenese_activation=reproduction_parthenogenese_activation
        self.reproduction_sexuelle_activation=reproduction_sexuelle_activation
        self.age_active=age
       
        self.world = {}
        self.listeCases=[]

         #le joueur qui execute ce programme
        self.initialiser_case()
        self.interface = Interface(self)
        self.interface.start_game()
        self.joueur=Joueur(self.interface.create_id())
        self.idjoueur =self.interface.get_mon_id()
        self.genere_objet("bob")
        self.genere_nourriture()

    def get_mon_interface(self):
        return self.interface
       
    def get_mon_joueur(self):
        return self.joueur
    
    def est_valide(self, coord, i, j):
        x, y = coord
        return x in range(i) and y in range(j)

    def nettoyer_dictionnaire(self, dictionnaire, i, j):
        # Créer une copie des clés pour éviter de modifier le dictionnaire pendant l'itération
        cles_a_supprimer = [cle for cle in dictionnaire if not self.est_valide(cle, i, j)]
        
        # Supprimer les clés invalides
        for cle in cles_a_supprimer:
            del dictionnaire[cle]

    def set_parametres(self,N, M,ticks_day,nb_bobs,reproduction_parthenogenese_activation,reproduction_sexuelle_activation,foods_jour,Mutv, Mut_m, Mut_mem, Mut_p,  **d):
        self.world_x=int(N)
        self.world_y=int(M)
        self.nettoyer_dictionnaire(self.world, self.world_x, self.world_y)
        self.ticks_jour=int(ticks_day)
        self.totale_nourriture=int(foods_jour)
        self.nb_bobs=int(nb_bobs)

        self.reproduction_parthenogenese_activation=reproduction_parthenogenese_activation
        self.reproduction_sexuelle_activation=reproduction_sexuelle_activation

        for case, elmt in self.world.items():
            if "bob" in elmt:
                for bob in self.world[case]["bob"]:
                    bob.set_parametres_bob(Mutv, Mut_m, Mut_mem, Mut_p)

    def tick_jour_renitialisation(self):
        # Méthode à appeler pour remettre à 0 le "temps" lorsque l'on commence une nouvelle partie
        global tick, jour
        tick = 1 ; jour = 1
     
    def jouer2(self)  :
        if(self.cpt_ticks>=self.ticks_jour):
            if(self.cpt_ticks>self.ticks_jour):
                self.cpt_ticks=1
            self.jour+=1
            self.effacer_nourriture()
            self.genere_nourriture()
        self.cpt_ticks=1+self.cpt_ticks%(self.ticks_jour) 
               
    def jouer(self):
        copy_dict=dict(self.world)
        for case, elmts in list(copy_dict.items()): 
            if "bob" in elmts:
                for bob in list(elmts["bob"]):
                    if not bob.deja_deplace:
                        if not bob.est_mort:
                            bob.deplacementParTick(self.world, case, self.world_x,self.world_y, self.reproduction_parthenogenese_activation, self.reproduction_sexuelle_activation, self.age_active,self.listeCases,self.interface)
                            if self.age_active:    
                                bob.increment_age()
                            if bob.eSpawn<=0:
                                bob.est_mort=True
        copy_dict=dict(self.world) 
        for case, elmts in list(copy_dict.items()): 
            if "bob" in elmts:
                for bob in list(elmts["bob"]):
                    bob.deja_deplace=False
                    if bob.est_mort:
                        bob.effacer_bob(self.world,case)
        self.interface.give_info()
 
    def genere_objet(self,option):
        joueur = self.get_mon_joueur() # joueur = joueur1
        if option=="bob":
            nb_objet=self.nb_bobs 
        # elif option=="nourriture":
        #     nb_objet=self.totale_nourriture
            
        for _ in range(nb_objet):
            pos_i = random.randint(0, self.world_x - 1)
            pos_j = random.randint(0, self.world_y - 1)
            case = get_Case(self.listeCases,pos_i,pos_j)
            if (case is not None and( case.je_possede_propriete()==True or self.interface.autre_Joueur_Possede_Case(pos_i,pos_j) == False)):
                if option=="bob":
                    new_objet = Bob() 
                # if option=="nourriture":
            #     new_objet= Nourriture()
                ajouter(self.world,option,new_objet,pos_i,pos_j)
                joueur.ajouter_bob_au_joueur(new_objet)
                case.prendre_propriete(self)


                
                

            else:
                #print("case impossible !!!!!!!!!!!!!!!")
                self.genere_objet(option)  
    
    

    
    
    
    def effacer_nourriture(self):
        dict_copy = dict(self.world)
        for pos in dict_copy.keys():
            if "nourriture" in dict_copy[pos]:
                del self.world[pos]["nourriture"]
                if len(self.world[pos])==0:            
                    del self.world[pos]

    def genere_nourriture(self):
        joueur = self.get_mon_joueur()
        for _ in range(self.totale_nourriture):
            pos_i = random.randint(0, self.world_x - 1)
            pos_j = random.randint(0, self.world_y - 1)
            case = get_Case(self.listeCases,pos_i,pos_j)
            if( case is not None and (case.je_possede_propriete()==True or self.interface.autre_Joueur_Possede_Case(pos_i,pos_j) == False)):
                new_objet= Nourriture()
                new_objet.x=pos_i
                new_objet.y=pos_j
                if (pos_i, pos_j) in self.world:
                    if "nourriture" in self.world[pos_i, pos_j]:
                        self.world[pos_i, pos_j]["nourriture"].set_energie((self.world[pos_i, pos_j]["nourriture"].get_energie() + new_objet.get_energie())) 
                        
                    else:
                        self.world[pos_i, pos_j]["nourriture"]=new_objet
                        joueur.ajouter_nourriture_joueur(new_objet)
                else:
                    self.world[pos_i, pos_j]={"nourriture":new_objet}
                    joueur.ajouter_nourriture_joueur(new_objet)
                case.prendre_propriete(self)
            else:
                
                self.genere_nourriture()
                
            
            
        
    def get_tick(self):
        return self.cpt_ticks
    def get_jour(self):
        return self.jour   
    def get_tick_jour(self):
        return self.ticks_jour

    def initialiser_case(self):
        for i in range(self.world_x):
            for j in range(self.world_y):
                case = Case(i, j)
                self.listeCases.append(case)

    def mesBobs(self): # retourne une liste de liste [[x,y,masse], [x,y,masse], ...]
        liste_bobs = []
        for case, elmts in self.world.items():
            if "bob" in elmts:
                for bob in elmts["bob"]:
                    liste_bobs.append([bob.x, bob.y, bob.mass])
        return liste_bobs
    
    #retourne l'energie de la nouriture si elle existe sinon 0    
    def check_nourriture_existe(self, x, y):
        if (x, y) in self.world:
            if "nourriture" in self.world[x, y]:
                return self.world[x, y]["nourriture"].get_energie()
        return 0 
    

#retourne la liste des positions des nourritures
    def get_postions_mesNourritures(self):
        liste_nourriture = []
        for case, elmts in self.world.items():
            if "nourriture" in elmts:
                liste_nourriture.append([case[0], case[1]])
        return liste_nourriture
       
    
        
                
               


       
