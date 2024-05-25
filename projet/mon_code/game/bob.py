import random
import copy
from game.methods import *
from game.nourriture import *
from game.ftRZO import *
from game.case import *


num_bob=0
    
class Bob():
    dflt_eSpawn=100 #100
    dflt_eMax=200 #200
    dflt_eMother=150 
    dflt_eBirth=50 
    dflt_velocity = 1 
    dflt_Mutv=0.5
    dflt_Mutp=0.5
    dflt_Mutm=0.5
    dflt_Mutmem=0.5
    dflt_e_SR=150 # l'energie min pour la reproduction sexuelle
    dflt_eBirth_SR=100 # l'energie initiale de Child
    dflt_mass=1        
    dflt_perception_score=1
     
    def __init__(self):
        self.eSpawn=self.dflt_eSpawn
        self.eMax=self.dflt_eMax
        self.eMother=self.dflt_eMother
        self.eBirth=self.dflt_eBirth
        self.velocity =self.dflt_velocity
        self.x=0
        self.y=0
        self.speedBuffer = 0
        self.age=0
        self.memoryPoint=0
        self.nb_Nouriture_Memorisable = self.memoryPoint#nb de nouritures qu'on  peut encore memoriser (espace libre) 
        self.nb_Cases_Memorisable = 2*self.memoryPoint #nb de cases qu'on peut encore memoriser (espace libre) 

        self.casesMemorisees=[]
       
        self.listFoodMemorise=[]
       
        global num_bob
        self.id=num_bob
        num_bob+=1

        self.Mutv=self.dflt_Mutv
        self.Mutp=self.dflt_Mutp
        self.Mutmem=self.dflt_Mutmem
        self.Mutm=self.dflt_Mutm
        
        self.mass=self.dflt_mass

        self.perception_score=self.dflt_perception_score
        self.destination=None
        self.buffer_nourriture=None

        self.est_mort=False

        self.deja_deplace=False
        self.e_SR=self.dflt_e_SR
        self.eBirth_SR=self.dflt_eBirth_SR

        #-------------------------
        self.proprietaire = 1
       


    @classmethod
    def set_parametres(cls, eSpawn, eMax, eMother, eBirth, velocity,Mutv,mass,perception_score,Mut_m,Mut_p,Mut_mem,e_SR,eBirth_SR, **d):
        cls.dflt_eSpawn=int(eSpawn)
        cls.dflt_eMax=int(eMax)
        cls.dflt_eMother=int(eMother)
        cls.dflt_eBirth=int(eBirth)
        cls.dflt_velocity =float(velocity)
        cls.dflt_Mutv=float(Mutv)
        cls.dflt_Mutm=float(Mut_m)
        cls.dflt_Mutp=float(Mut_p)
        cls.dflt_Mutmem=float(Mut_mem)
        cls.dflt_mass=float(mass)
        cls.dflt_perception_score=int(perception_score)
        cls.dflt_e_SR=float(e_SR)
        cls.dflt_eBirth_SR=float(eBirth_SR)
    def set_parametres_bob(self,Mutv, Mut_m, Mut_mem, Mut_p, **d):
        self.Mutv=float(Mutv)
        self.Mutm=float(Mut_m)
        self.Mutmem=int(Mut_mem)
        self.Mutp=int(Mut_p)

    def __str__(self):
        global num_bob
        return "bob"+str(self.id)+"("+str(self.x)+","+str(self.y)+")(e_SR="+str(self.e_SR)+"eBirth_SR="+str(self.eBirth_SR)+")"
    
    def set_case(self, i, j):
        self.get_case(self).set_i_j(self, i, j)   
    def set_case(self,new_case):
        self.case = new_case
    def set_ebirth(self):
        self.eSpawn-=self.eBirth
    def set_velocity(self, new_velocity):
        self.velocity = new_velocity
    def set_speedBuffer(self, new_speedBuffer):
        self.speedBuffer = new_speedBuffer
    def set_eSpawn(self, new_eSpawn):
        self.eSpawn = new_eSpawn
    def set_mass(self,mass):
        self.mass=mass
    def set_memoryPoint(self,memoryPoint):
        self.memoryPoint=memoryPoint
        self.nb_Cases_Memorisable=2*memoryPoint
        self.nb_Nouriture_Memorisable=memoryPoint

    def get_size_bob(self)  :
        return (self.img_bob.get_width(), self.img_bob.get_height())
    def get_position(self):
        return (self.x, self.y)
    def get_velocity(self):
        return self.velocity
    def get_speedBuffer(self):
        return self.speedBuffer
    def get_eSpawn(self):
        return self.eSpawn
    def get_mass(self):
        return self.mass
    def set_perception_score(self, p):
        self.perception_score=p
    def get_position(self):
        return (self.x, self.y)
    def get_emax(self):
        return self.eMax
    def get_age(self):
        return self.age
    def get_perception(self):
        return self.perception_score
    
    def set_position(self, x, y):
        self.x=x
        self.y=y
    
    def changer_propriete(self):
        self.proprietaire = 0


    def objets_visibles(self, world):
        # Clear previous perceptions
        nourritures_visibles = []
        bobs_visibles = []
        bob_i, bob_j = self.get_position()

        max_distance = self.perception_score      
        for dx in range(-max_distance, max_distance + 1):
            for dy in range(-max_distance, max_distance + 1):
                neighbor_x = bob_i + dx
                neighbor_y = bob_j + dy

                distance = abs(dx) + abs(dy)
                if distance <= max_distance and (neighbor_x, neighbor_y) in world:
                    if "nourriture" in world[(neighbor_x, neighbor_y)] :   
                        nourritures_visibles.append(world[(neighbor_x, neighbor_y)]['nourriture'])
                    else:
                        bobs_visibles.extend(world[(neighbor_x, neighbor_y)]['bob'])
                        
        
        return nourritures_visibles, bobs_visibles
    

    def nettoyer_nourriture_memorise(self):
        #print("nettoyer_nourriture_memorise pour", self)
        res=[]
        bob_i, bob_j = self.get_position()

        max_distance = self.perception_score 

        liste=[f.get_position() for f in self.listFoodMemorise]     
        for dx in range(-max_distance, max_distance + 1):
            for dy in range(-max_distance, max_distance + 1):
                distance = abs(dx) + abs(dy)
                neighbor_x = bob_i + dx
                neighbor_y = bob_j + dy
                if  distance <= max_distance and (neighbor_x, neighbor_y) in liste:
                    res.append((neighbor_x, neighbor_y))
        for e in self.listFoodMemorise:
            if e.get_position() in res:
                #print("remove")
                self.listFoodMemorise.remove(e)
                self.nb_Nouriture_Memorisable=self.nb_Nouriture_Memorisable+1

        return res


    def preciserDestinationNouriture(self,world):
        destination=None
        nourritures_visibles, bobs_visibles = self.objets_visibles(world)
        #print("Nourritures visibles pour", self, ":", end=" ")
        for e in nourritures_visibles:
            print(e, end=" ")
        print(" ")
        for element1 in nourritures_visibles:# permet d'enlever de la memoire les nourritures qu'on est actuelement cappable de voir et de liberer les points
                for element2 in self.listFoodMemorise:
                    if(element1.__eq__(element2)):#on utilise la methode eq vu qu on les copies des norrirutes dans listFoodMemorise
                        self.listFoodMemorise.remove(element2)
                        self.nb_Nouriture_Memorisable=self.nb_Nouriture_Memorisable+1
        # permet d'enlever de la memoire les nourritures que normalement on est actuelement cappable de les voir mais elles ne sont plus là
        self.nettoyer_nourriture_memorise()
        
        if nourritures_visibles:  # Check if the destination list is not empty
            # Utilisation de la fonction distance comme clé de tri
           

            dest= sorted(nourritures_visibles, key=lambda n: (calcule_distance(self, n), -n.get_energie() ))[0]
            destination =dest 

        elif bobs_visibles:
            bobs_visibles.remove(self)
            if bobs_visibles:                           
                dest=sorted(bobs_visibles, key=lambda b: (calcule_distance(self, b), b.get_mass()))[0]
                if self.is_predator(dest):
                    destination =dest
        if destination == None:#si il n y a aucune nourriture dans notre perception on check les nourritures memorisées
            if self.listFoodMemorise:
                temp = sorted(self.listFoodMemorise, key=lambda food: food.get_energie(), reverse=True)[0]
                destination=temp
                
        return destination   


    def predateurTrouvePerception(self,world, destination):
        pretadeur_trouve=False
        # destination =  self.preciserDestinationNouriture(world)
        _, bobs_visibles= self.objets_visibles(world)
        lp=[b for b in bobs_visibles if b.is_predator(self) and b!=self]
     
        for b_pretador in (lp):
           
            if destination!=None and calcule_distance(b_pretador, destination) <= calcule_distance(b_pretador, self):
                pretadeur_trouve =True
                break
            if destination==None:
                pretadeur_trouve =True
                break
        return pretadeur_trouve,lp
    

    def choisirPositionMemoire(self,positionsPossibles):
        positionsCopies= list(positionsPossibles)
        for position in positionsPossibles:
            if position in self.casesMemorisees:
                positionsCopies.remove(position)
        if positionsCopies :
            return random.choice(positionsCopies)
        else:
            return random.choice(positionsPossibles)


    def move_alea(self,world, nb_lignes, nb_collones,listeCases,interface):
        pos_i, pos_j= self.get_position()
        l=[]
        #mouvement à droite
        if pos_i<=nb_lignes-2:
            l.append((pos_i+1,pos_j))
        #mouvement à gauche
        if pos_i>0:
            l.append((pos_i-1,pos_j))
        #mouvement haut
        if pos_j<=nb_collones-2:
            l.append((pos_i,pos_j+1))
        #mouvement bat
        if pos_j>0:
            l.append((pos_i,pos_j-1))
       
        pos_i, pos_j=self.choisirPositionMemoire(l)

        self.effacer_bob(world, self.get_position())

        case = get_Case(listeCases, pos_i, pos_j)
        case.gerer_propriete(interface)
        ajouter(world, "bob",self, pos_i, pos_j)


    def move_to_destination(self, world, destination,listeCases, interface):
        x, y=destination.get_position() 
        self.effacer_bob(world, (self.x, self.y))
        copieX=self.x
        copieY=self.y
        position_possibles=[]

        if x > self.x:
            copieX += 1
            position_possibles.append((copieX, self.y))
        elif x < self.x:
            copieX -= 1
            position_possibles.append((copieX, self.y))
        
       
        if y > self.y:
            copieY += 1
            position_possibles.append((self.x, copieY))
        elif y < self.y:
            copieY -= 1
            position_possibles.append((self.x, copieY))
        
        if position_possibles:# si le bob est déja dans la case de sa destination 
            self.x, self.y = self.choisirPositionMemoire(position_possibles)

        case = get_Case(listeCases, self.x, self.y)
        case.gerer_propriete(interface)
        ajouter(world, "bob",self, self.x, self.y)
       

    def move_away(self, detected_bob, world, nb_lignes, nb_collones,listeCases,interface):
        self.effacer_bob(world, (self.x, self.y))
        copieX=self.x
        copieY=self.y
        position_possibles=[]
        if detected_bob.x > self.x > 0:
            copieX-= 1
        elif detected_bob.x < self.x < nb_lignes:
            copieX+= 1
        position_possibles.append((copieX, self.y))
        if detected_bob.y > self.y > 0:
            copieY-= 1
        elif detected_bob.y < self.y < nb_collones:
            copieY+= 1
        position_possibles.append((self.x, copieY))
        
        self.x, self.y = self.choisirPositionMemoire(position_possibles)
        case = get_Case(listeCases, self.x, self.y)
        case.gerer_propriete(interface)
        ajouter(world, "bob",self, self.x, self.y)


    def memoriserCaseVisite(self,ancienX,ancienY):
        
        if(ancienX,ancienY) not in self.casesMemorisees:
            if  self.nb_Cases_Memorisable >0: #si on peut encore stocker des case visitées
                
                self.casesMemorisees.append((ancienX,ancienY))# on stocke la case dont les coordonnées sont passées en param 
                self.nb_Cases_Memorisable = self.nb_Cases_Memorisable -1 # on decremente le nb de cases visitées qu'on peut memoriser
            else:   
                if self.casesMemorisees:      #sinon si la liste des cases memorisées n'est pas vide 
                    self.casesMemorisees.pop(0) #on supprime la case la plus ancienne dont on se souvient 
                    self.casesMemorisees.append((ancienX,ancienY)) #et on stocke la position de la case qu'on vient de visiter 


    def nourritures_plus_visibles(self,world,destination,anciennes_nourritures_visibles):#retourne les nourriture qu'on ne voit plus
        nouvelles_nourritures_visibles, _= self.objets_visibles(world)
        if anciennes_nourritures_visibles:
            if destination in anciennes_nourritures_visibles:
                anciennes_nourritures_visibles.remove(destination)
            return [nourriture for nourriture in anciennes_nourritures_visibles if nourriture not in nouvelles_nourritures_visibles]
        return[]
         

    def memoriserNourriture(self,nourriture):#procedure qui permet de memoriser une nouriture 
            copie_food = copy.deepcopy(nourriture)# copie profonde comme ca la memoire du bob 
            self.listFoodMemorise.append(copie_food)
            self.nb_Nouriture_Memorisable=self.nb_Nouriture_Memorisable-1
            self.nb_Cases_Memorisable= self.nb_Cases_Memorisable-2
            if self.casesMemorisees:
                self.casesMemorisees.pop(0)
            if self.casesMemorisees:
                self.casesMemorisees.pop(0)


    def memoriserLesNourritures(self,world,destination,anciennes_nourritures_visibles):# procedure qui permet de memoriser l ensemble de nourriture qu on ne voit plus en fonction de leur energie et du points restants 
      
        nourritures_plus_visibles= self.nourritures_plus_visibles(world,destination,anciennes_nourritures_visibles)
       
        nourriture_A_memorise=sorted(nourritures_plus_visibles, key=lambda food: food.get_energie(), reverse=True)
       
        if(nourriture_A_memorise): 
            for nourriture in nourriture_A_memorise:

                if self.nb_Nouriture_Memorisable>0:
                    self.memoriserNourriture(nourriture)
                else:
                    break


    def move(self, world, nb_lignes, nb_collones,listeCases,interface):#mouvement a une case adjacente 
        ancienX =self.x
        ancienY =self.y #pour stocker cette position dans la liste des cases à memorisées 
        nourritures_visibles, _= self.objets_visibles(world)
        
        destination =  self.preciserDestinationNouriture(world)
        predateur_trouve,lp=self.predateurTrouvePerception(world, destination)
       
        if predateur_trouve:
            
            closest=sorted(lp, key=lambda p: calcule_distance(p, self))[0]
           
            self.move_away(closest, world, nb_lignes, nb_collones,listeCases)
            
        else:
            if destination==None:
             
                self.move_alea(world, nb_lignes, nb_collones,listeCases,interface)

            else:
                self.move_to_destination(world, destination,listeCases,interface)

        self.memoriserLesNourritures(world,destination,nourritures_visibles)#on memorise les nourritures qu'on ne voit plus  
        self.memoriserCaseVisite(ancienX,ancienY)# apres avoir effectuer le deplacement vers une case on memorise la position precedente 



    def deplacementParTick(self,world, position, nb_lignes, nb_collones, reproduction_parthenogenese_active, reproduction_sexuelle_active, age_active,listeCases,interface):
        
        for _ in range(int(self.get_velocity())):
            
            self.move(world, nb_lignes, nb_collones,listeCases,interface)
            
            if (self.consommation(world, (self.x, self.y)) ):
                if reproduction_sexuelle_active:
                    if "bob" in world[(self.x, self.y)]:
                        bobs = list(world[(self.x, self.y)]["bob"])
                        bobs.remove(self)
                        for other_bob in bobs:
                            if self.sexual_reproduction(other_bob, world, self.x, self.y):
                                break
                elif reproduction_parthenogenese_active:
                    if self.reproduction_parthenogenese(world,self.x, self.y)  :
                        break
                
                break
        self.deja_deplace=True
        
            
        if age_active:
            if self.age <= 50:
                energie = self.get_eSpawn() + 0.1
                self.set_eSpawn(energie)
            else:
                energie = self.get_eSpawn() -0.2
                self.set_eSpawn(energie)          
        self.manage_speedBuffer()         
        # gére la perte d'energie       
        self.manage_energy()
        

    def increment_age(self):
        self.age += 1


    def is_predator(self, other):
        return (other.mass/self.mass)<(2/3)


    def eat_bob(self, other, world):
        if e:=self.eSpawn+0.5*(other.eSpawn*(1-self.mass/other.mass))<self.eMax:
            self.set_eSpawn(e)
        else:
            self.set_eSpawn(self.eMax)
        other.est_mort=True


    def reproduction_parthenogenese(self, world, pos_i, pos_j):
        if self.eSpawn>=self.eMax:
            
            new_bob = Bob()
            new_bob.set_eSpawn(self.eBirth)        
            Bv = self.get_velocity()
            
            Cv = random.uniform(max(0.3,self.get_velocity()-self.Mutv),self.get_velocity()+self.Mutv)
            Cm=random.uniform(max(0.3,self.get_mass()-self.Mutm),self.get_mass()+self.Mutm)
            Cp=random.randint(max(0,self.perception_score-self.Mutp), self.perception_score+self.Mutp)
            Cmem=random.randint(max(0,self.memoryPoint-self.Mutmem), self.memoryPoint+self.Mutmem)

            new_bob.set_mass(max(0, Cm))
            new_bob.set_velocity(Cv)
            new_bob.set_perception_score(Cp)
            new_bob.set_memoryPoint(Cmem)
            new_bob.age=0
            
            ajouter(world, "bob", new_bob, pos_i, pos_j)
            self.set_eSpawn(max(0, self.eSpawn - self.eMother))
            return True
        return False


    def sexual_reproduction(self, bob2, world, pos_i, pos_j):
        if self.eSpawn >= self.eBirth and bob2.eSpawn >= bob2.eBirth:
            self.eSpawn -= 100
            bob2.eSpawn -= 100

            new_bob = Bob()
            new_bob.set_eSpawn(100)  # initial energy # De
        

            # mutation for each characteristic
            Cv= random.uniform(max(0.3,(self.get_velocity() + bob2.get_velocity()) / 2 - self.Mutv), (self.get_velocity() + bob2.get_velocity()) / 2 + self.Mutv)
            Cm = random.uniform(max(0.3,(self.get_mass() + bob2.get_mass()) / 2 - self.Mutm), (self.get_mass() + bob2.get_mass()) / 2 + self.Mutm)
            Cp = random.randint(max(0,(self.perception_score + bob2.perception_score) // 2 - self.Mutp), (self.perception_score + bob2.perception_score) // 2 + self.Mutp)
            Cmem=random.randint(max(0,(self.memoryPoint + bob2.memoryPoint)// 2 - self.Mutmem), (self.memoryPoint + bob2.memoryPoint)// 2 + self.Mutmem)
            
            new_bob.set_mass(Cm)
            new_bob.set_velocity(Cv)
            new_bob.set_perception_score(Cp)
            new_bob.age=0
            new_bob.set_memoryPoint(Cmem)

            ajouter(world, "bob", new_bob, pos_i, pos_j)

            return True
        return False    


    def manage_speedBuffer(self):
        if isinstance(self.get_velocity(), float):
            self.set_velocity(self.get_speedBuffer() + self.get_velocity() )
            self.set_speedBuffer( self.get_velocity() - int(self.get_velocity()))

 
    def effacer_bob(self, world, position):
        world[position]["bob"].remove(self)
        
        if len(world[position]["bob"])==0:            
            del world[position]["bob"]
        if len(world[position])==0:            
            del world[position]
 

    def eat_food(self, world,food):
        if (e:=self.eMax-self.eSpawn)>0:
            if e>=food.get_energie():
                self.set_eSpawn(self.eSpawn+food.get_energie())
                food.set_energie(0)
                
            else:
                self.set_eSpawn(self.eSpawn+e)
                food.set_energie(food.get_energie()-e)
    

    def consommation(self, world, position): 
        if "nourriture" in world[position]:
            nourriture_max=world[position]["nourriture"]
            self.eat_food(world, nourriture_max)
            if nourriture_max.get_energie()<=0:
                nourriture_max.effacer_nourriture(world, position)
            
            return True
        else:
            bobs=list(world[position]["bob"])
            bobs.remove(self)
           
            if bobs:
                b=sorted(bobs, key=lambda b: b.mass)[0]#manger le plus petit
                if self.is_predator(b):
                    self.eat_bob(b, world)
                    return True
        return False
    
    
    def energy_lost(self):
        eMin = 0.5
        return max(eMin, (self.mass*(self.get_velocity()**2)+self.perception_score/5+self.memoryPoint/5))# la consommation depend de la vitesse, la masse, la perception et la memoire  
     
      
    def manage_energy(self):
        # lorsque le bob ne bouge pas : la vitesse est egale à 0 ?? /!\
        
        energie= self.get_eSpawn() - self.energy_lost()
        self.set_eSpawn(energie)
    
def calcule_distance(obj1, obj2):
    xi1, yi1 = obj1.get_position()
    xi2, yi2 = obj2.get_position()
    dx = abs(xi1 - xi2)
    dy = abs(yi1 - yi2)        
    return dx + dy 

