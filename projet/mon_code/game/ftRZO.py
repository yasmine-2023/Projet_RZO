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
        self.send_list = [] #Liste des messages à envoyer
        self.messages_list = []  # Liste pour stocker les messages reçus
        self.message_lock = threading.Lock()  
        self.send_lock = threading.Lock()
        self.stop_event = Event()
        self.info_adversaire = {}
        self.info_nourriture = {}
        self.var_id_libre_ad = 1
        self.test_id = None
        self.demande_etat_case=-1
        self.autre_joueur_a_la_case=0
        self.lib = self.load_library()
        self.coordonnées_possession = (-1,-1)
        self.coordonner_abandon_nourriture = (-1,-1)
        self.val_retour_ad_abandonne_nouri = 0
        self.coordonnées_abandon = (-1,-1)
        self.nb_rep_autre_joueur_abandonne_propriete = 0
        self.recurtion_autre_joueur_abandon = 0
        self.nb_rep_autre_joueur_possede_case = 0
        self.recurtion_autre_joueur_possetion=0
        self.quelquun_attend = 0
        self.nb_rep_synchro = 0
        self.recurtion_synchronisation = 0
        self.je_peux_reprendre = 0
        self.nb_rep_info_nourriture_recus = 0
        self.recurtion_donner_nouriturre = 0
        self.recurtion_donner_bob = 0
        self.nb_rep_info_bob_recus = 0
        self.nb_rep_possede_case = 0
        self.nb_rep_abandon_nourriture = 0

        self.nb_truc_analyser = 0
        self.nb_synchronisation = 0
        

        self.semaphore = threading.Semaphore(2)
        

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
        #print("je vais mettre le message sur la liste:",message)
        self.send_list.append(message)
        #print("j'ai mis le message sur la liste:",message)

    def faire_envoi(self, message):
        
        message_c = ctypes.create_string_buffer(message.encode('utf-8'))
        self.lib.envoi(message_c)
        #print(message_c, " a ete envoye par la fonction c")


    def receive_message(self):
        message_ptr = self.lib.reception()

        if message_ptr:
            mess = ctypes.c_char_p(message_ptr).value.decode('utf-8')
            
            with self.message_lock:
                self.messages_list.append(mess)
                #print("je met le message sur la liste d'attente :",mess)
                #print("voici la liste actuel :", self.messages_list)
            



    def boucle_ecoute(self):
        
        while not self.stop_event.is_set():

            self.receive_message()

    
    def boucle_analyse(self):
        while not self.stop_event.is_set():

            if self.messages_list:
                with self.message_lock:
                    while self.messages_list:
                        message = self.messages_list.pop(0)
                        print("je vais lance l'analyse du message:",message)
                        #self.analyse_message(message)
                        #thread = Thread(target=self.analyse_message, args=(message,))
                        #thread.start()
                        thread = threading.Thread(target=self.analyse_message_with_semaphore, args=(message,))
                        thread.start()
    
    def analyse_message_with_semaphore(self, message):
        with self.semaphore:
            self.analyse_message(message)
                        
                        
            


    def boucle_envoi(self):
        while not self.stop_event.is_set():

            if self.send_list:
                with self.send_lock:
                    while self.send_list:
                        
                        a_envoye = self.send_list.pop(0)
                        #print("je recupere le message a envoye de la liste :",a_envoye)
                        self.faire_envoi(a_envoye)
                        print("j'ai fais l'envoie du message:", a_envoye)
                        
            
        
    '''-------------------------------------------demarage et stopage du jeu---------------------------------------------------'''
    
    def start_game(self) : 
        
        self.start1 = Thread(target=self.boucle_ecoute)
        self.start2 = Thread(target=self.boucle_analyse)
        self.start3 = Thread(target=self.boucle_envoi)
        self.start1.start()
        self.start2.start()
        self.start3.start()
        

    def stop_game(self):

        self.stop_event.set()

        self.start1.join()
        self.start2.join()
        self.start3.join()
        
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
        #print("janalyse le protocol pour :",dico)
        for cle in dico:
            match cle:
                case "n":
                    self.connexionUtilisateur(dico[cle])
                case "r":
                    self.nb_truc_analyser +=1
                    self.DeconnexionUtilisateur(dico[cle])
                case "k":
                    #print("ça rentre dans le match case pour k")
                    self.nb_truc_analyser +=1
                    self.analyse_info_adversaire(dico[cle])
                case "u" :
                    self.nb_truc_analyser +=1
                    self.analyse_id_libre_ad(dico[cle])
                case "p" :
                    self.nb_truc_analyser +=1
                    self.analyse_rep_id_libre_ad(dico[cle])
                case "j" :
                    self.nb_truc_analyser +=1 
                    self.analyse_autre_joueur_abandonne_propriete(dico[cle])
                case "x":
                    self.nb_truc_analyser +=1
                    #print("on rentre dans le match case pour l'abandon de la case :",self.coordonnées_possession)
                    self.analyse_rep_autre_joueur_abandonne_propriete(dico[cle])
                case "v":
                    self.nb_truc_analyser +=1
                    self.analyse_autre_Joueur_Possede_Case(dico[cle])
                case "w":
                    self.nb_truc_analyser +=1
                    #print("on rentre dans le match case pour analyse rep possession", self.coordonnées_possession)
                    self.analyse_rep_autre_Joueur_Possede_Case(dico[cle])
                case "y":
                    self.nb_truc_analyser +=1
                    self.analyse_info_ad_nourriture(dico[cle])
                case "o":
                    self.nb_truc_analyser +=1
                    self.analyse_adverssaire_abandonne_nourriture(dico[cle])
                case "i":
                    self.nb_truc_analyser +=1
                    self.analyse_rep_adverssaire_abandonne_nourriture(dico[cle])
                case "syn":
                    self.analyse_quelqun_mattend(dico[cle])
                    print("match syn")
                case "synack":
                    self.analyse_tu_na_plus_a_mattendre(dico[cle])
                    print("match synack")
                case "ack":
                    self.analyse_je_peux_reprendre(dico[cle])
                    print("match ack")
                case "nok":
                    self.analyse_rep_info_ad_nourriture(dico[cle])
                case "bok":
                    self.analyse_rep_info_adversaire(dico[cle])

    def analyse_message(self,message):
        #print("je suis rentre dans l'analyse du message:",message)
        dico=self.decoupe(message)
        #print("j'ai bien decoupe mon message:",message)
        self.analyse_protocol(dico)

        
        
    '''---------------------------------------- Fonction pour le jeu en lui-même ------------------------------------------------------'''

    def JmeConnecte(self,id):
        self.send_message("n,"+ str(id))

    def connexionUtilisateur(self, tab):
        id_user = int(tab[0])
        listeUsers = self.getUsers()
        
        if any(user['id'] == id_user for user in listeUsers):
            return
        
        i = 0
        for user in listeUsers:
            if listeUsers[i]["id"] == -1:
                listeUsers[i]["id"] = id_user
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
                #print ("la var est passe a 0")
                self.var_id_libre_ad = 1
                return 0
            i+=1
            time.sleep(0.02)
        return 1


    def analyse_id_libre_ad(self, tab):
        #print("je rentre dans analyse_id,"+str(tab[0])+","+str(self.idjoueur))
        if self.idjoueur == int(tab[0]):
            #print("je vais envoye la rep a cedric:")
            self.send_message("p,"+str(self.idjoueur))
        self.nb_truc_analyser -=1

    def analyse_rep_id_libre_ad(self,tab):
        #print("je rentre dans analyse_rep_id"+str(tab[0]))
        if self.test_id == int(tab[0]):
            #print("je suis rentre dans le if de analyse rep")
            self.connexionUtilisateur(tab)
            self.var_id_libre_ad = 0
        self.nb_truc_analyser -=1




    def create_id(self):
        print("le tableau est mis en attente")
        for i in range(1,MAX_JOUEUR):
            self.test_id = i
            if self.id_libre(i) and self.id_libre_adversaire(i):
                self.idjoueur = i
                tab = [self.test_id]
                self.connexionUtilisateur(tab)
                self.JmeConnecte(i)
                self.test_id = None
                print("le tableau arrete l' attente")
                return i
            i+=1

    def get_mon_id(self):
        return self.idjoueur
    '''---------------------------------------------------'''



    def give_info(self):
        #print("je donne mes information à ced")
        

        n = self.nb_users()-1
        

        if ( n != 0) :
            self.send_message("k,"+str(self.idjoueur)+","+str(self.jeu.mesBobs()))
            start_time = time.time()

            while self.nb_rep_info_bob_recus <= n:
                
                confirm = self.nb_rep_info_bob_recus

                if time.time() - start_time >= 3:  # Si plus d'une demi seconde s'est écoulée
                    return 
                #    self.recurtion_donner_bob +=1
                #    if self.recurtion_donner_bob == 2 :
                #        self.recurtion_donner_bob = 0
                #        self.nb_rep_info_bob_recus = 0
                #        return 
                #     self.nb_rep_info_bob_recus = 0
                #     print('on lance recurtion')
                #     return self.give_info()
                
                
                if confirm == n:
                    self.recurtion_donner_bob = 0
                    self.nb_rep_info_bob_recus = 0
                    return

                time.sleep(0.1)
    
    def analyse_info_adversaire(self,tab):
        mon_id = self.idjoueur
        id_user = int(tab[0])
        if( mon_id != id_user):
            ma_tab = tab[1:]
            str_list = ','.join(ma_tab)
            actual_list = ast.literal_eval(str_list)
            self.info_adversaire[id_user] = actual_list
            #print("liste des bobs de ced bien mis a jour:", actual_list)
            self.send_message("bok,"+str(self.idjoueur))


    def analyse_rep_info_adversaire(self,tab):
        mon_id = self.idjoueur
        id_user = int(tab[0])
        if( mon_id != id_user):
            self.nb_rep_info_bob_recus +=1    
        

    def get_info_adversaire(self):
        valeurs_collees = []
        for liste in self.info_adversaire.values():
            valeurs_collees.extend(liste)
        #print("la valeur des bobs de ced retorune est :",valeurs_collees)
        return valeurs_collees
    
    '''------------------------------------------------------'''
    
    def autre_joueur_abandonne_propriete(self,x,y):
        self.send_message("j,"+str(self.idjoueur)+","+str(x)+","+str(y))
        self.coordonnées_abandon=(x,y)
        #print("le joueur d'id :"+str(self.idjoueur)+", a envoye une demande d'abandon de propriete pour la case :"+str(x)+","+str(y))
        n = self.nb_users()-1
        start_time = time.time()

        if ( n != 0) :
            while self.nb_rep_autre_joueur_abandonne_propriete <= n:
                
                confirm = self.nb_rep_autre_joueur_abandonne_propriete

                if time.time() - start_time >= 3:  # Si plus d'une demi seconde s'est écoulée
                    self.recurtion_autre_joueur_abandon +=1
                    if self.recurtion_autre_joueur_abandon == 2 :
                        self.recurtion_autre_joueur_abandon = 0
                        self.coordonnées_abandon=(-1,-1)
                        self.nb_rep_autre_joueur_abandonne_propriete = 0
                        print("on retourne -1 suite a trop de temps")
                        return -1
                    self.nb_rep_autre_joueur_abandonne_propriete = 0
                    print('on lance recurtion')
                    return self.autre_joueur_abandonne_propriete(x, y)
                
                if self.demande_etat_case != -1:
                    t = self.demande_etat_case
                    self.demande_etat_case = -1
                    self.coordonnées_abandon=(-1,-1)
                    self.nb_rep_autre_joueur_abandonne_propriete =0    
                    self.recurtion_autre_joueur_abandon = 0
                    print(" reponse à la demande abandon de propriete d'id:"+str(self.idjoueur)+", et de coordonnées de case :"+str(x)+","+str(y))
                    return t
                
                if confirm == n:
                    self.nb_rep_autre_joueur_abandonne_propriete +=1

                time.sleep(0.1)
    
        #print("le joueur d'id :"+str(self.idjoueur)+", na pas eu de reponse de l'abandon pour la case :"+str(x)+","+str(y))
        print("le nombre de rep attendu est :",n)
        print("le nombre de reponse est:",self.nb_rep_autre_joueur_abandonne_propriete)
        print("on est direct sortie")
        self.coordonnées_abandon=(-1,-1)
        self.nb_rep_autre_joueur_abandonne_propriete =0  
        self.recurtion_autre_joueur_abandon = 0
        return -1



    def analyse_autre_joueur_abandonne_propriete(self,tab):
        id_envoyeur = int(tab[0])
        if self.idjoueur != id_envoyeur:
            x = int(tab[1])
            y = int(tab[2])
            case = get_Case(self.jeu.listeCases,x,y)
            #print("j'analyse la demande du joueur d'id :"+str(id_envoyeur) +", pour que j'abandonne la case de coordonnées: "+str(x)+","+str(y))
            #print("possession de la case :"+str(x)+","+str(y)+"; est :"+ str(r))
            if case.je_possede_propriete() :
                
                val = self.jeu.check_nourriture_existe(x,y)
                val=round(val)
                
                case.abandonner_propriete(self.jeu)
                self.send_message("x,"+str(id_envoyeur)+","+str(x)+","+str(y)+","+str(val))
            else :
                self.send_message("x,"+str(id_envoyeur)+","+str(x)+","+str(y)+","+str(-1))
        self.nb_truc_analyser -=1


    def analyse_rep_autre_joueur_abandonne_propriete(self,tab):
        #print("je rentre dans l'analyse de la rep du joueur "+str(tab[0])+" pour l'abandon de la case :"+str(tab[1])+","+str(tab[2]))
        if int(tab[0]) == self.idjoueur  and self.coordonnées_abandon== (int(tab[1]), int(tab[2])):
            #print("j'ai analise la rep de la demande d'abandon pour la case :", self.coordonnées_abandon)
            self.nb_rep_autre_joueur_abandonne_propriete +=1
            n = int(tab[3])
            #print("la valeur de la reponse est :",n)
            if n !=-1 :
                self.demande_etat_case = n
        self.nb_truc_analyser -=1

    """-------------------------------------------------------------------------------------------"""

    def autre_Joueur_Possede_Case(self, x, y) :
        self.coordonnées_possession =(x,y)
        n = self.nb_users()-1
        start_time = time.time()

        if ( n != 0) :
            self.send_message("v,"+str(self.idjoueur)+","+str(x)+","+str(y))
            start_time = time.time()
            while self.nb_rep_possede_case <= n:
                
                confirm = self.nb_rep_possede_case

                if time.time() - start_time >= 3: 
                    print("le joueur d'id :"+str(self.idjoueur)+", n'a pas eu de reponse qu'un autre joueur possede la case :"+str(x)+","+str(y))
                    self.autre_joueur_a_la_case = 0
                    self.coordonnées_possession = (-1,-1) 
                    self.nb_rep_possede_case = 0
                    return 0
        
                if self.autre_joueur_a_la_case == 1:
                    self.autre_joueur_a_la_case = 0
                    self.coordonnées_possession = (-1,-1)
                    self.nb_rep_possede_case = 0
                    print("le joueur d'id :"+str(self.idjoueur)+", a recus une reponse qu'un autre joueur possede la case :"+str(x)+","+str(y))
                    return 1
                
                if confirm == n:
                    print("le joueur d'id :"+str(self.idjoueur)+", a recus une reponse quauquun autre joueur possede la case :"+str(x)+","+str(y))
                    self.autre_joueur_a_la_case = 0
                    self.coordonnées_possession = (-1,-1)
                    self.nb_rep_possede_case = 0
                    return 0
        self.coordonnées_possession = (-1,-1)
        return 0


    def analyse_autre_Joueur_Possede_Case(self,tab):
        id_envoyeur = int(tab[0])
        if self.idjoueur != id_envoyeur:
            x = int(tab[1])
            y = int(tab[2])
            case = get_Case(self.jeu.listeCases,x,y)
            #print("j'analyse la demande du joueur d'id :"+str(id_envoyeur) +", pour savoir si je possede la case de coordonnées: "+str(x)+","+str(y))
            #r=case.je_possede_propriete()
            #print("possession de la case :"+str(x)+","+str(y)+"; est :"+ str(r))
            if case.je_possede_propriete() :
                self.send_message("w,"+str(id_envoyeur)+","+str(x)+","+str(y))
            else :
                self.send_message("w,"+str(id_envoyeur)+",-2,-2")
        

    def analyse_rep_autre_Joueur_Possede_Case(self,tab):
        self.nb_rep_possede_case +=1
        #print("je rentre dans l'analyse de la rep du joueur "+str(tab[0])+" pour possession de la case :"+str(tab[1])+","+str(tab[2]))
        if int(tab[0]) == self.idjoueur  and self.coordonnées_possession == (int(tab[1]), int(tab[2])):
            #print("j'ai recus la rep de la demande de possession pour la case :",self.coordonnées_possession)
            self.autre_joueur_a_la_case = 1
        



    "---------------------------------------- nourriture -------------------------------------"




    def give_info_nourriture(self):
        #print("je donne mes information à ced")
        n = self.nb_users()-1
        start_time = time.time()

        if ( n != 0) :
            self.send_message("y,"+str(self.idjoueur)+","+str(self.jeu.get_positions_mesNourritures()))
            start_time = time.time()
            while self.nb_rep_info_nourriture_recus <= n:
                
                confirm = self.nb_rep_info_nourriture_recus

                if time.time() - start_time >= 3:  # Si plus d'une demi seconde s'est écoulée
                    return
                #     self.recurtion_donner_nouriturre +=1
                #     if self.recurtion_donner_nouriturre == 2 :
                #         self.recurtion_donner_nouriturre = 0
                        
                #         self.nb_rep_info_nourriture_recus = 0
                #         print("on retourne -1 suite a trop de temps")
                #         return 
                #     self.nb_rep_info_nourriture_recus = 0
                #     print('on lance recurtion')
                #     return self.give_info_nourriture()
                
                
                if confirm == n:
                    self.recurtion_donner_nouriturre = 0
                    self.nb_rep_info_nourriture_recus = 0
                    return

                time.sleep(0.1)
    
    
    def analyse_info_ad_nourriture(self,tab):
        mon_id = self.idjoueur
        id_user = int(tab[0])

        if( mon_id != id_user):
            ma_tab = tab[1:]
            str_list = ','.join(ma_tab)
            actual_list = ast.literal_eval(str_list)
            self.info_nourriture[id_user] = actual_list
            #print("liste des bobs de ced bien mis a jour:", actual_list)
            self.send_message("nok,"+str(self.idjoueur))


    def analyse_rep_info_ad_nourriture(self,tab):
        mon_id = self.idjoueur
        id_user = int(tab[0])
        if( mon_id != id_user):
            self.nb_rep_info_nourriture_recus +=1    
        self.nb_truc_analyser -=1






    def get_nourritures_adverssaires(self):
        valeurs_collees = []
        for liste in self.info_nourriture.values():
            valeurs_collees.extend(liste)
        #print("la valeur des nourritures de ced retorune est :",valeurs_collees)
        return valeurs_collees
    
    

    '''---------------------------------------------------------------'''
    def adverssaire_abandonne_nourriture(self,x,y):
        self.coordonner_abandon_nourriture = (x,y)
        n = self.nb_users()-1
        start_time = time.time()

        if ( n != 0) :
            self.send_message("o,"+str(self.idjoueur)+","+str(x)+","+str(y))
            start_time = time.time()
            while self.nb_rep_abandon_nourriture <= n:
                
                confirm = self.nb_rep_abandon_nourriture

                if time.time() - start_time >= 3: 
                    self.val_retour_ad_abandonne_nouri = 0
                    self.coordonner_abandon_nourriture = (-1,-1)
                    return 0
                
                if self.val_retour_ad_abandonne_nouri == 1:
                    self.val_retour_ad_abandonne_nouri = 0
                    self.coordonner_abandon_nourriture = (-1,-1)
                    print("le joueur d'id :"+str(self.idjoueur)+", a recus une reponse qu'un autre joueur abandonne la nouriture situe :"+str(x)+","+str(y))
                    return 1
                
                if confirm == n:
                    self.val_retour_ad_abandonne_nouri = 0
                    self.coordonner_abandon_nourriture = (-1,-1)
                    return 0
                    
        self.coordonner_abandon_nourriture = (-1,-1)
        return 0



    def analyse_adverssaire_abandonne_nourriture(self,tab):
        iduser = int(tab[0])
        if self.idjoueur != iduser:
            x = int(tab[1])
            y = int(tab[2])
            #print("le joueur d'id :"+str(self.idjoueur)+", est en train d'analyser la demande d'abandonne la nouriture situe :"+str(x)+","+str(y))
            nour = self.jeu.get_nourriture(x,y)

            if nour != None :
                nour.abandonner_propriete_nourriture()
                self.send_message("i,"+str(iduser)+","+str(x)+","+str(y)+","+str(1))
                #print("le joueur d'id :"+str(self.idjoueur)+", a abandonne la nouriture situe :"+str(x)+","+str(y))
            else : 
                self.send_message("i,"+str(iduser)+","+str(x)+","+str(y)+","+str(0))
                #print("le joueur d'id :"+str(self.idjoueur)+", n'avais pas la nouriture situe :"+str(x)+","+str(y))


    def analyse_rep_adverssaire_abandonne_nourriture(self,tab):
        self.nb_rep_abandon_nourriture += 1
        iduser = int(tab[0])
        x = int(tab[1])
        y = int(tab[2])

        if self.idjoueur == iduser and self.coordonner_abandon_nourriture == (x,y) : 
            if int(tab[3]) == 1 : 
                self.val_retour_ad_abandonne_nouri = 1
                print("le joueur d'id :"+str(iduser)+", a confirmer avoir bien abandonner pas la nouriture situe :"+str(x)+","+str(y))
                
        
    '''---------------------------------------------------------------'''

    def synchronisation_joueurs(self):
        self.nb_synchronisation+=1
        print("on a lancé la synchronisation des joueurs numero :",self.nb_synchronisation)
        # print("le nombre de truc restant a analyser est :",self.nb_truc_analyser)
        # while self.nb_truc_analyser !=0:
        #     print("le nombre de truc restant a analyser est :",self.nb_truc_analyser)
        #     time.sleep(0.05)
        
        nombre_rep_a_attendre = self.nb_users()-1
        
        if nombre_rep_a_attendre !=0 : 
            start_time = time.time()
            print("quelquun attend =",self.quelquun_attend)

            if self.quelquun_attend == 1 :
                print("quelquun m'attend deja")
                self.send_message("synack,"+str(self.idjoueur))
                while self.je_peux_reprendre == 0:
                    time.sleep(0.2)
                print("jai pu reprendre")
                self.je_peux_reprendre = 0
                self.quelquun_attend = 0
                return     

            if self.quelquun_attend == 0 :
                print("personne ne m'attendais")
                self.send_message("syn,"+str(self.idjoueur))
                if ( nombre_rep_a_attendre != 0) :
                    print("j'attend la rep de ced")
                    while self.nb_rep_synchro<= nombre_rep_a_attendre:
                        print("je rentre dans le while")
                        confirm = self.nb_rep_synchro

                        if time.time() - start_time >= 5:  
                            return
                        #     self.recurtion_synchronisation +=1
                        #     if self.recurtion_synchronisation == 2 :
                        #         self.recurtion_synchronisation = 0
                        #         self.nb_rep_synchro = 0
                        #         print("recurtion fini et toujours pas de rep")
                        #         return 
                        #     self.nb_rep_synchro = 0
                        #     print('on lance recurtion')
                        #     return self.synchronisation_joueurs()
                    
                        if confirm == nombre_rep_a_attendre:
                            self.send_message("ack,"+str(self.idjoueur))
                            self.nb_rep_synchro = 0
                            self.recurtion_synchronisation=0
                            print("j'ai eu la rep de ced et c'est bon je peux reprendre")
                            return
                        time.sleep(0.2)
    


    def analyse_tu_na_plus_a_mattendre(self,tab):
        if self.idjoueur != int(tab[0]):
            print("j'analyse le fait que ced m'ai dis que je n'ai plus a attendre")
            self.nb_rep_synchro +=1
        
        
    def analyse_je_peux_reprendre(self,tab):
        if self.idjoueur != int(tab[0]):
            print("j'analyse le fait que ced m'ai dis que je pouvais reprendre")
            self.je_peux_reprendre = 1
        


    def analyse_quelqun_mattend(self,tab):
        if self.idjoueur != int(tab[0]):
            print("j'analyse le fait que ced m'ai dis qu'il m'attendais")
            self.quelquun_attend = 1
        
        
        

    
	
	
    






