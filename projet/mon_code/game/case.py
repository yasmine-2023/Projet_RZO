from game.ftRZO import *
from game.nourriture import *

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
        print("la valeur du proprietaire test3",self.proprietaire)
        if (not self.je_possede_propriete()):
                val=interface.autre_joueur_abandonne_propriete(self.x,self.y)
                print("valeur de l'energie test2 yas",val)
                self.prendre_propriete(interface.jeu) #prendre propriété de la case
    
                if val>0:
                    print("test4 J'ai trouvé un nourriture dans la case(",self.x,",",self.y,")",)
                    interface.adverssaire_abandonne_nourriture(self.x,self.y)
                    nourriture = Nourriture()
                    nourriture.set_position(self.x,self.y)
                    nourriture.set_energie(val)
                    print("On vient de créé uune nouvelle nourriture de position:(",self.x,",",self.y,") et d'energie",val)
                    nourriture.prendre_propriete(interface.jeu)  #prendre propriété du contenue de la case
                    print("je prend la propriete de la nourriture de position:(",self.x,",",self.y,")" )
                    
    

    
    

    
    

    