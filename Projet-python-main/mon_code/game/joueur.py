from game.methods import *
from  game.bob import *
from  game.jeu import *
class Joueur:
    def __init__(self):
        self.liste_bobs = []

    def ajouter_bob(self, bob):
        self.liste_bobs.append(bob)
        # verifier si il faut ajouter dans le dictionnaire world 
        
    
    def supprimer_bob_joueur(self, bob,world):
        if bob in self.liste_bobs:
            self.liste_bobs.remove(bob)
            if bob in world:
                position = bob.get_position()
                bob.effacer_bob(world,position)
            
            


        
        