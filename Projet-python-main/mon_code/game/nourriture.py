
########################################################
"""
La classe `Nourriture` représente un objet de nourriture dans le jeu.
"""
########################################################

import random


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
        self.nombre_parties = random.randint(0, 5)
        self.parties = [{'energie': self.energie_nourriture / self.nombre_parties, 'proprietaire': None, 'locked': False} for _ in range(self.nombre_parties)]                #on stocke uniquement les nouritures qui n'ont pas encore étaient consommées 
    @classmethod
    def set_parametres(cls,energy_food, **d):
        cls.dflt_energy_nourriture=float(energy_food)
    def set_proprietaire(self, proprietaire):
        self.proprietaire=proprietaire
    def get_energie(self):
        return self.energie_nourriture
    def set_energie(self, energie):
        self.energie_nourriture=energie
    def get_position(self):
        return (self.x, self.y)
    def effacer_nourriture(self, world, position): 
        #avant de supprimer la nourriture on traite le cas ou cette nourriture est deja memorise par l'un des bob   
        del world[position]["nourriture"]
     
    def __str__(self)    :
        global num_nourriture
        return "nourriture ("+str(self.x)+","+str(self.y)+") energie="+str(self.energie_nourriture)
    
    def __eq__(self, other):
        if isinstance(other, Nourriture):
            return self.energie_nourriture == other.energie_nourriture and self.x==other.x and self.y ==other.y
        return False
    #-------------Partie RZO----------------
    def transferer_propriete(self, nouveau_proprietaire):
        self.proprietaire = nouveau_proprietaire.id# Fichier nourriture.py
    def lock_partie(self, index_partie):
        if index_partie < len(self.elements) and not self.elements[index_partie]['locked']:
            self.elements[index_partie]['locked'] = True
            return True
        return False

    def unlock_partie(self, index_partie):
        if index_partie < len(self.elements):
            self.elements[index_partie]['locked'] = False
            return True
        return False


  
    

 
    
