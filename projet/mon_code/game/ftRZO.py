from game.joueur import *
from game.jeu import *
import ctypes
from ctypes import c_char_p, CDLL
from threading import Thread, Event
import threading
import time
import ast


# A coder return l'id du joueur qui possede une case de coord (x,y), sinon return 0 si personne ne la possede  
def id_joueur_case(x,y):
    return 1


#A coder : le joueur dont l'id est en parametre abandonne la propriete de la case de coord (x,y)
# cad appeler dans le programme de l'autre joueur la ft abandonner_propriete (que j'ai code dans la classe Case) a partir de l'objet case de coord (x,y)






#retourne un id pour un nouveau joueur


#def bob_joueursAdverses(): #retourne une liste de liste [[x,y,masse], [x,y,masse], ...] des bobs des joueurs adverses x,y (coordonnees du bob) et sa masse 
    #utiliser la fonction mesBobs de la classe Jeu ou le joueur retourne les 3infos de ses bob dans une liste de liste  [[x,y,masse], [x,y,masse], ...] 
    #return [[1,1,1]] # je retourne [[1,1,1]] pour tester

#idjoueur = create_id()# je recupere l'id du joueur

MAX_JOUEUR = 6


def create_list(n):
    return [{'id': -1} for _ in range(n)]



class Interface:
    def __init__(self, jeu):

        self.idjoueur = None


        self.jeu=jeu
        self.library_path = './mon_code/game/projet_envoi/libprojetReseau.so'
        self.loading = False
        self.listUsers = create_list(MAX_JOUEUR)
        self.messages_list = []  # Liste pour stocker les messages reçus
        self.message_lock = threading.Lock()  
        self.stop_event = Event()
        self.info_adversaire = {}
        self.var_id_libre_ad = 1
        self.test_id = None
        self.demande_etat_case=-1
        self.autre_joueur_a_la_case=0

    def load_library(self):
        lib = CDLL(self.library_path)
        lib.envoi.argtypes = [c_char_p]
        lib.envoi.restype = None
        lib.reception.argtypes = []
        lib.reception.restype = c_char_p
        lib.ferme_socket.argtypes = []
        lib.ferme_socket.restype = None
        return lib


    '''--------------------------------------------Fonction C lien--------------------------------------------------'''

    def send_message(self, message):
        lib = self.load_library()
        message_c = ctypes.create_string_buffer(message.encode('utf-8'))
        lib.envoi(message_c)


    def receive_message(self):
        lib = self.load_library()
        message_ptr = lib.reception()
        if message_ptr:
            mess = ctypes.c_char_p(message_ptr).value.decode('utf-8')
            
            with self.message_lock:
                self.messages_list.append(mess)
            



    def boucle_ecoute(self):
        while not self.stop_event.is_set():

            self.receive_message()

    
    def boucle_analyse(self):
        while not self.stop_event.is_set():

            if self.messages_list:
                with self.message_lock:
                    while self.messages_list:
                        message = self.messages_list.pop(0)
                        self.analyse_message(message)
            time.sleep(0.1)

    '''-------------------------------------------demarage et stopage du jeu---------------------------------------------------'''
    
    def start_game(self) : 
        self.start1 = Thread(target=self.boucle_ecoute)
        self.start2 = Thread(target=self.boucle_analyse)
        self.start1.start()
        self.start2.start()
        

    def stop_game(self):
        lib = self.load_library()

        self.stop_event.set()

        self.start1.join()
        self.start2.join()
        
    '''---------------------------------------------utilitiare liste des connectés------------------------------------------------'''
        


    def getUsers(self):
        return self.listUsers
    
    def setUsers(self, liste):
        self.listUsers = liste

    def display_users(self):
        for user in self.listUsers:
            print(user)
    
    def nb_users(self):
        n=0
        for user in self.listUsers:
            if user['id'] != -1:
                n+=1
        return n

    '''------------------------------------------analyse des messages reçus----------------------------------------------------'''
    
    def decoupe(self, mess, delimiteur=","):
        dico ={}
        tab = mess.split(delimiteur)
        dico[tab[0]] = tab[1:]
        return dico 


    def analyse_protocol(self,dico):
        for cle in dico:
            match cle:
                case "n":
                    self.connexionUtilisateur(dico[cle])
                case "r":
                    self.DeconnexionUtilisateur(dico[cle])
                case "k":
                    self.analyse_info_adversaire(dico[cle])
                case "u" :
                    self.analyse_id_libre_ad(dico[cle])
                case "p" :
                    self.analyse_rep_id_libre_ad(dico[cle])
                case "j" : 
                    self.analyse_autre_joueur_abandonne_propriete(dico[cle])
                case "x":
                    self.analyse_rep_autre_joueur_abandonne_propriete(dico[cle])
                case "v":
                    self.analyse_autre_Joueur_Possede_Case(dico[cle])
                case "w":
                    self.analyse_autre_Joueur_Possede_Case(dico[cle])



    def analyse_message(self,message):
        dico=self.decoupe(message)
        self.analyse_protocol(dico)
        
    '''---------------------------------------- Fonction pour le jeu en lui-même ------------------------------------------------------'''

    def JmeConnecte(self,id):
        self.send_message("n,"+ str(id))

    def connexionUtilisateur(self, tab):
        
        id_user = tab[0]
        listeUsers = self.getUsers()
        i = 0
        for user in listeUsers:
            if listeUsers[i]["id"] == -1:
                listeUsers[i]["id"] = int(id_user)
                self.setUsers(listeUsers)
                self.display_users()
                break
            i += 1

    '''---------------------------------------------------'''

    def JmeDeConnecte(self,id):
        self.send_message("r,"+ str(id))

    
    def DeconnexionUtilisateur(self, tab):
        id_user = int(tab[0])
        listeUsers = self.getUsers()
        i = 0
        for user in listeUsers:
            if listeUsers[i]["id"] == id_user:
                listeUsers[i]["id"] = -1
                self.setUsers(listeUsers)
                
                self.display_users()
                break
            i += 1

    '''---------------------------------------------------'''

    def id_libre(self, id):
        for user in self.listUsers:
            if user['id'] == id:
                return False
        return True


    def id_libre_adversaire(self, id) :
        self.send_message("u,"+str(id))
        i = 0
        while i<10 :
            if self.var_id_libre_ad == 0:
                print ("la var est passe a 0")
                self.var_id_libre_ad = 1
                return 0
            i+=1
            time.sleep(0.02)
        return 1


    def analyse_id_libre_ad(self, tab):
        print("je rentre dans analyse_id,"+str(tab[0])+","+str(self.idjoueur))
        if self.idjoueur == int(tab[0]):
            print("je vais envoye la rep a cedric:")
            self.send_message("p,"+str(self.idjoueur))

    def analyse_rep_id_libre_ad(self,tab):
        print("je rentre dans analyse_rep_id"+str(tab[0]))
        if self.test_id == int(tab[0]):
            print("je suis rentre dans le if de analyse rep")
            self.connexionUtilisateur(tab)
            self.var_id_libre_ad = 0



    def create_id(self):
        for i in range(1,MAX_JOUEUR):
            self.test_id = i
            if self.id_libre(i) and self.id_libre_adversaire(i):
                self.JmeConnecte(i)
                self.idjoueur = i
                self.test_id = None
                return i
            i+=1

    def get_mon_id(self):
        return self.idjoueur
    '''---------------------------------------------------'''



    def give_info(self):
        self.send_message("k,"+str(self.idjoueur)+","+str(self.jeu.mesBobs()))
            


    
    def analyse_info_adversaire(self,tab):
        mon_id = self.get_mon_id()
        id_user = int(tab[0])

        if( mon_id != id_user):
            ma_tab = tab[1:]
            str_list = ','.join(ma_tab)
            actual_list = ast.literal_eval(str_list)
            self.info_adversaire[id_user] = actual_list

    def get_info_adversaire(self):
        valeurs_collees = []
        for liste in self.info_adversaire.values():
            valeurs_collees.extend(liste)
        return valeurs_collees
    
    '''------------------------------------------------------'''
    
    def autre_joueur_abandonne_propriete(self,x,y):
        self.send_message("j,"+str(self.idjoueur)+","+str(x)+","+str(y))
        print("j'ai envoye une demande de propriete")
        i = 0
        while i<10 :
            if self.demande_etat_case != -1:
                t = self.demande_etat_case
                self.demande_etat_case = -1
                return t
            i+=1
            time.sleep(0.02)
        return -1



    def analyse_autre_joueur_abandonne_propriete(self,tab):
        id_envoyeur = int(tab[0])
        if self.idjoueur != id_envoyeur:
            x = int(tab[1])
            y = int(tab[2])
            case = get_Case(self.jeu.listeCases,x,y)
            print("j'analyse la demande de propriete de cedric")
            if case.je_possede_propriete() :
                case.abandonner_propriete(self.jeu)
                val = self.jeu.check_nourriture_existe(x,y)
                self.send_message("x,"+str(id_envoyeur)+","+str(val))


    def analyse_rep_autre_joueur_abandonne_propriete(self,tab):
        if int(tab[0]) == self.idjoueur:
            print("j'ai recus la rep de la demande de propriete")
            self.demande_etat_case = int(tab[1])



    '''------------------------------------------------------'''
    def autre_Joueur_Possede_Case(self, x, y) :
        self.send_message("v,"+str(self.idjoueur)+","+str(x)+","+str(y))
        print("j'ai envoye une demande de possession de case")
        i = 0
        while i<10 :
            if self.autre_joueur_a_la_case == 1:
                self.autre_joueur_a_la_case = 0
                return 1
            i+=1
            time.sleep(0.02)
        return 0


    def analyse_autre_Joueur_Possede_Case(self,tab):
        id_envoyeur = int(tab[0])
        if self.idjoueur != id_envoyeur:
            x = int(tab[1])
            y = int(tab[2])
            case = get_Case(self.jeu.listeCases,x,y)
            print("j'analyse la demande de propriete de cedric")
            if case.je_possede_propriete() :
                self.send_message("w,"+str(id_envoyeur)+","+str(1))

    def analyse_rep_autre_Joueur_Possede_Case(self,tab):
        if int(tab[0]) == self.idjoueur:
            print("j'ai recus la rep de la demande de propriete")
            self.autre_joueur_a_la_case = int(tab[1])

#A coder PS:utiliser la ft get_postions_mesNourritures() de la classe jeu
    def get_nourriture_adverssaire(self):
        return [[1,1]]
        



    









'''----------------------------------------------------------------------------------------------------------'''
'''------------------------------------------- Notre Main ---------------------------------------------------'''
'''----------------------------------------------------------------------------------------------------------'''



if __name__ == "__main__":

    '''----------------------- Bonjour ----------------------------'''

    interface = Interface()
    interface.start_game()
    time.sleep(1)

    '''------------------------------------------------------------'''
    

    mon_id = interface.create_id()
    print("c'est mon id:"+str(mon_id))

    time.sleep(0.1)

    mo = interface.create_id()
    print("c'est mon 2eme id:"+str(mo))
    
    time.sleep(0.1)
    ''''
    mon = interface.create_id()
    print("c'est mon 3eme id:"+str(mon))
    time.sleep(1)
    
    time.sleep(0.07)

    print("j'ai combien dutilisateur :"+str(interface.nb_users()))

    time.sleep(0.07)

    interface.JmeDeConnecte(mo)
    '''''

    rep = interface.get_info_adversaire(mon_id)
    
    print(rep)
    



    '''----------------------- Au revoir ----------------------------'''

    time.sleep(0.1)
    interface.stop_game()

    '''------------------------------------------------------------'''
