from game.ftRZO import *
from game.nourriture import *
import  time 
class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.proprietaire = 0
        

    def abandonner_propriete(self,jeu):
        self.proprietaire = 0
        jeu.get_mon_joueur().effacer_case(self)
        if (self.x, self.y) in jeu.world:
            if("nourriture" in jeu.world[self.x,self.y]):
                nourriture = jeu.world[(self.x, self.y)]["nourriture"]
                if nourriture is not None:
                    nourriture.abandonner_propriete_nourriture(jeu)

    def prendre_propriete(self,jeu):
        self.proprietaire = 1
        jeu.get_mon_joueur().ajouter_case(self)
        
    
    def je_possede_propriete(self):
        return self.proprietaire 
    
    def gerer_propriete(self,interface):
        # print("la valeur du proprietaire de la case de coordoné:",self.x,",",self.y,"; est ",self.proprietaire)
        if (not self.je_possede_propriete()):
                val=interface.autre_joueur_abandonne_propriete(self.x,self.y)
                time.sleep(0.1)
                # print("valeur de l'energie de la case  de coordonnée:",self.x,",",self.y," ; que possede un autre joueur est ",val)
                self.prendre_propriete(interface.jeu)
                time.sleep(0.1) #prendre propriété de la case
                if val>0:
                    # print("je demande aux autres de laisser la propriete de la nourriture de coordonnée :",self.x,",",self.y)
                    interface.adverssaire_abandonne_nourriture(self.x,self.y)
                    time.sleep(0.1)
                    nourriture = Nourriture()
                    nourriture.set_position(self.x,self.y)
                    nourriture.set_energie(val)
                    nourriture.prendre_propriete(interface.jeu)
                    time.sleep(0.1)#prendre propriété du contenue de la case
                    # print("je devrai avoir bien pris la propriete et nourriture la case de coordoné:",self.x,",",self.y)

    
    

    
    

    