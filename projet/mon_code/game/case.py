from game.ftRZO import *


class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.proprietaire = 0
        

    def abandonner_propriete(self,jeu):
        self.proprietaire = 0
        jeu.get_mon_joueur().effacer_case(self)
        nourriture = jeu.world[(self.x, self.y)]["nourriture"]
        if nourriture is not None:
            nourriture.abandonner_propriete_nourriture(jeu)

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
                if val>0:
                    nourriture = None
                    for n in interface.jeu.nourritures_adverssaires:
                        if n.x==self.x and n.y==self.y:
                            nourriture = n
                    nourriture.set_energie(val)
                    nourriture.prendre_propriete(interface.jeu)   
                    print("valeur de l'energie test3 yas",val)

    
    

    
    

    