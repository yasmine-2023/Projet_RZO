from game.joueur import *
global joueur1
global idjoueur 
# return True si un autre joueur possede la case sinon false
def case_appartient_autre_joueur(case):
    return False

#retourne le joueur a partir de son id
def get_joueur_by_id(idjoueur):
    return joueur1

#retourne l'id de joueur qui execute le code
def get_id():
    return idjoueur

#retourne un id pour un nouveau joueur
def create_id():
    return 1

idjoueur = create_id()# je recupere l'id du joueur

joueur1=Joueur(idjoueur) # pour tester je cree un joueur avec idjoueur qui est 1 
