
########################################################
"""
La classe `Nourriture` représente un objet de nourriture dans le jeu.
"""
########################################################

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
        self.elements = () #la clef c'est une chaine de caractere (ex MC1) et la valeur c'est l'objet joueur  
                          #on stocke uniquement les nouritures qui n'ont pas encore étaient consommées 
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
     
    def __str__(self)    :
        global num_nourriture
        return "nourriture ("+str(self.x)+","+str(self.y)+") energie="+str(self.energie_nourriture)
    
    def __eq__(self, other):
        if isinstance(other, Nourriture):
            return self.energie_nourriture == other.energie_nourriture and self.x==other.x and self.y ==other.y
        return False
    

 
    
