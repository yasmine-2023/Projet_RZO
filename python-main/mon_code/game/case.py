from game.ftRZO import *
#from game.traitement import *

class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.proprietaire = 1
        

    def abandonner_propriete(self):
        self.proprietaire = 0
        get_mon_joueur().effacer_case(self)

    def prendre_propriete(self):
        self.proprietaire = 1
        get_mon_joueur().ajouter_case(self)
    
    def je_possede_propriete(self):
        return self.proprietaire == 1
    
    def gerer_propriete(self):
        if (not self.je_possede_propriete()):
            if (id_joueur_case(self.x,self.y)!=0):
                joueur = id_joueur_case(self.x,self.y)
                autre_joueur_abandonne_propriete(joueur,self.x,self.y)
                self.prendre_propriete()
            else:
                self.prendre_propriete()

    
    

    
    

    