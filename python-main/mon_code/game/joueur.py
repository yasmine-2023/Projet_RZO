from game.methods import *
from  game.bob import *
from  game.jeu import *


class Joueur:

        def __init__(self, idjoueur):
            self.idJoueur = idjoueur
            self.bobs = []
            self.nourritures = []
            self.cases = []
            

        def ajouter_bob_au_joueur(self, bob):
            self.bobs.append(bob)

        def ajouter_nourriture_joueur(self, nourriture):
            self.nourritures.append(nourriture)

        def effacer_nourriture_joueur(self, nourriture):
            self.nourritures.remove(nourriture)

        def possede_case(self, x, y):
            for case in self.cases:
                if case.x == x and case.y == y:
                    return True
            return False

        
     

        
        