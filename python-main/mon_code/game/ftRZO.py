from game.joueur import *
global joueur1
global idjoueur 

# A coder return l'id du joueur qui possede une case de coord (x,y), sinon return 0 si personne ne la possede  
def id_joueur_case(x,y):
    return 1


#A coder : le joueur dont l'id est en parametre abandonne la propriete de la case de coord (x,y)
# cad appeler dans le programme de l'autre joueur la ft abandonner_propriete (que j'ai code dans la classe Case) a partir de l'objet case de coord (x,y)

def autre_joueur_abandonne_propriete(idjoueur,x,y):
    pass 

#retourne le joueur a partir de son id
def get_mon_joueur():
    return joueur1

#retourne l'id de joueur qui execute le code
def get_mon_id():
    return idjoueur

#retourne un id pour un nouveau joueur
def create_id():
    return 1

def bob_joueursAdverses(): #retourne une liste de liste [[x,y,masse], [x,y,masse], ...] des bobs des joueurs adverses x,y (coordonnees du bob) et sa masse 
    #utiliser la fonction mesBobs de la classe Jeu ou le joueur retourne les 3infos de ses bob dans une liste de liste  [[x,y,masse], [x,y,masse], ...] 
    return [[1,1,1]] # je retourne [[1,1,1]] pour tester

idjoueur = create_id()# je recupere l'id du joueur

joueur1=Joueur(idjoueur) # pour tester je cree un joueur avec idjoueur qui est 1 
