from game.ftRZO import *


class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.proprietaire = 0
        

    def abandonner_propriete(self,jeu):
        self.proprietaire = 0
        jeu.get_mon_joueur().effacer_case(self)

    def prendre_propriete(self,jeu):
        self.proprietaire = 1
        jeu.get_mon_joueur().ajouter_case(self)
    
    def je_possede_propriete(self):
        return self.proprietaire 
    
    def gerer_propriete(self,interface):
        print("la valeur du proprietaire test3",self.proprietaire)
        if (not self.je_possede_propriete()):
                val=interface.autre_joueur_abandonne_propriete(self.x,self.y)
                print("valeur de l'energie test2 yas",val)
                self.prendre_propriete(interface.jeu)

    
    

    
    

    