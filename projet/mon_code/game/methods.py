import pickle
import pygame as pg

########################################################
"""
Le module `methods` contient des fonctions utilitaires pour le jeu.
"""
########################################################

def draw_texte(screen, texte, size, couleur, pos):
    font = pg.font.SysFont(None, size) # création de la police PyGame par défaut (None) ainsi que de la taille (size)
    texte_surface = font.render(texte, True, couleur) # permet de faire le rendu du texte
    texte_rectangle = texte_surface.get_rect(topleft=pos) # création d'un rectangle à "pos", c'est dans ce rectangle où sera notre texte

    screen.blit(texte_surface, texte_rectangle) # affiche à l'écran


def ajouter( world,option,obj, pos_i, pos_j):
    obj.x=pos_i                     
    obj.y=pos_j                 
    postion=(pos_i, pos_j)            
    if postion in world:   
        if option in world[postion]:
            world[postion][option].append(obj)
        else:
            world[postion][option] = [obj]
    else:
        world[postion] = {option: [obj]}


def calcule_distance(obj1, obj2):
    xi1, yi1 = obj1.get_position()
    xi2, yi2 = obj2.get_position()
    dx = abs(xi1 - xi2)
    dy = abs(yi1 - yi2)        
    return dx + dy 


def sauvegarder_valeurs(d, path):
        with open(path, "wb") as file:
            pickle.dump(d, file)


def charger_valeurs(d, path, all=False):
    with open(path, "rb") as file:
        d = pickle.load(file)
    return d

# def sauvegarder_valeurs(d, path):
#         with open(path, "a") as file:
#             for option, valeur in d.items():
#                 file.write(f"{option}:{valeur}\n")

# def charger_valeurs(d, path, all=False):
#     try:
#         with open(path, "r") as file:
#             file_content = file.readlines()  # Lire toutes les lignes
#             if not file_content:
#                 d={}
#             else:
#                 for line in file_content:
#                     parts = line.strip().split(":")
#                     if len(parts) == 2  :
#                         option, valeur = parts
                        
#                         if not all:                                                    
#                             if option in d:
#                                 d[option] = valeur
#                         else:
#                             d[option] = valeur
            
#     except FileNotFoundError:
#         pass  # Si le fichier n'existe pas, ignorez simplement


def sauvegarder_jeu(fic_name, jeu):
  
    # Charger le dictionnaire depuis le fichier binaire avec pickle
    with open('saved_games.pickle', 'rb') as fichier:
        mon_dictionnaire = pickle.load(fichier)

    # Ajouter un élément au dictionnaire
    mon_dictionnaire[fic_name] = jeu

    # Sauvegarder le dictionnaire mis à jour dans le fichier binaire avec pickle
    with open('saved_games.pickle', 'wb') as fichier:
        pickle.dump(mon_dictionnaire, fichier)


def effacer_jeu(fic_name):
  
    # Charger le dictionnaire depuis le fichier binaire avec pickle
    with open('saved_games.pickle', 'rb') as fichier:
        mon_dictionnaire = pickle.load(fichier)

    del mon_dictionnaire[fic_name]

    # Sauvegarder le dictionnaire mis à jour dans le fichier binaire avec pickle
    with open('saved_games.pickle', 'wb') as fichier:
        pickle.dump(mon_dictionnaire, fichier)

          
def charger_jeu(path):
    with open(path, "rb") as file:
        d = pickle.load(file)
    return d


def save_game(path, jeu):
    # Sauvegarde de l'instance de la classe Jeu dans un fichier
    with open(path, "wb") as file:
        pickle.dump(jeu, file)


def load_game(path):     
    # Rechargement de l'instance de la classe Jeu depuis le fichier
    with open(path, "rb") as file:
        jeu = pickle.load(file)
    return jeu


def afficher(d):
    msg=""
    print('{')
    for case, elmts in d.items():
        msg+=str(case)+": {"
        for k, objts in d[case].items():            
            msg+=str(k)+": ["
            if k=="bob":
                for objt in objts:
                    msg+=str(objt)+", "
            else:
                msg+=str(objts)+", "
                
            msg+="]}, "
        msg+=""
        print(msg)
        msg=""
            
    print("}") 



def get_Case(listeCase,x,y):
        for case in listeCase:
            if case.x == x and case.y == y:
                return case
        return None
   



    

   