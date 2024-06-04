
########################################################
"""
La classe `Nourriture` représente un objet de nourriture dans le jeu.
"""
########################################################
from game.ftRZO import *
from game.methods import * 
num_nourriture=0
    
class Nourriture():
    dflt_energy_nourriture=100
    def __init__(self):
        self.energie_nourriture=self.dflt_energy_nourriture
        global num_nourriture
        self.id=num_nourriture
        num_nourriture+=1
        self.x=0
        self.y=0
        self.proprietaire=0 #remis a 1 quand  je genere ma propre nourriture dans jeu
    @classmethod
    def set_parametres(cls,energy_food, **d):
        cls.dflt_energy_nourriture=float(energy_food)
    def get_energie(self):
        return self.energie_nourriture
    def set_energie(self, energie):
        self.energie_nourriture=energie
    def get_position(self):
        return (self.x, self.y)
    def effacer_nourriture(self, world, position): 
        #avant de supprimer la nourriture on traite le cas ou cette nourriture est deja memorise par l'un des bob   
        del world[position]["nourriture"]
    
    def set_position(self, x, y):
        self.x=x
        self.y=y
     
    def __str__(self)    :
        global num_nourriture
        return "nourriture ("+str(self.x)+","+str(self.y)+") energie="+str(self.energie_nourriture)
    
    def __eq__(self, other):
        if isinstance(other, Nourriture):
            return self.energie_nourriture == other.energie_nourriture and self.x==other.x and self.y ==other.y
        return False
    
    def abandonner_propriete_nourriture(self,jeu):
        self.proprietaire=0
        jeu.get_mon_joueur().effacer_nourriture_joueur(self)
        self.effacer_nourriture(jeu.world, (self.x, self.y))

    def prendre_propriete(self,jeu):
        self.proprietaire=1
        jeu.get_mon_joueur().ajouter_nourriture_joueur(self)
        if (self.x, self.y) not in jeu.world:
            jeu.world[(self.x, self.y)] = {}
       
        # Ajoute ou met à jour la clé "nourriture" dans le dictionnaire à la position (self.x, self.y)
        if "nourriture" not in jeu.world[(self.x, self.y)]:
            jeu.world[(self.x, self.y)]["nourriture"] = None
       
        jeu.world[(self.x, self.y)]["nourriture"] = self
        print("Je mets à jour mon dictionnaire, je rajoute la nourriture :", jeu.world[(self.x, self.y)]["nourriture"])






 
    
