from game.methods import *
from  game.bob import *
from  game.jeu import *
nbjoueur=0
class Joueur:
   
    
    # def supprimer_bob_joueur(self, bob,world):
    #     if bob in self.liste_bobs:
    #         self.liste_bobs.remove(bob)
    #         if bob in world:
    #             position = bob.get_position()
    #             bob.effacer_bob(world,position)
    

        def __init__(self):  # Add other parameters if needed
            global nbjoueur
            self.idJoueur = nbjoueur
            nbjoueur+=1
            self.bobs = []
            self.nourritures = []

        def ajouter_bob(self, bob):
            bob.proprietaire = self.idJoueur
            self.bobs.append(bob)

        def ajouter_nourriture(self, nourriture):
            for partie in nourriture.elements:
                partie['proprietaire'] = self.idJoueur
            self.nourritures.append(nourriture)
                


        
        