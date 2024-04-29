class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.proprietaire = 1
        

    def abandonner_propriete(self):
        self.proprietaire = 0

    def prendre_propriete(self):
        self.proprietaire = 1
    
    
    def je_possede_propriete(self):
        return self.proprietaire == 1
    
    

    
    

    