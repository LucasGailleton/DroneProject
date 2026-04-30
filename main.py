import random as r
import re
import sys 
sys.setrecursionlimit(5000)

class State:
    def __init__(self,posX:int,posY:int,battery:int,crashed:int,docked:int,airborne:int,visZones:list,obstacle_distance:int):
        
        # Position de la base et du drone
        self.posX = posX
        self.posY = posY
        
        # États du drone (Booléens ou Int)
        self.battery = battery
        self.crashed = crashed
        self.docked = docked
        self.airborne = airborne
        
        # Données d'environnement
        self.visZones = frozenset(visZones)    # Zones déjà visitées
        self.obstacle_distance = obstacle_distance
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.posX == other.posX and 
                self.posY == other.posY and 
                self.battery == other.battery and 
                self.crashed == other.crashed and 
                self.docked == other.docked and 
                self.airborne == other.airborne and 
                self.visZones == other.visZones and 
                self.obstacle_distance == other.obstacle_distance)

    def __hash__(self):
        return hash((self.posX, self.posY, self.battery, self.crashed, 
                    self.docked, self.airborne, self.visZones, self.obstacle_distance))

    def generer_transitions(self, maxX, maxY, baseX, baseY, Danger):

        transitions_possibles = []

        # TAKEOFF_CMD
        if self.crashed == 0 and self.airborne == 0 and self.docked == 0 and self.battery > 0:

            if((self.posX, self.posY) in Danger) :
                nouv_obst_dist = 0
            else :
                nouv_obst_dist = 2

            etat_suiv = State(self.posX, self.posY, self.battery, self.crashed, self.docked, 1, self.visZones, nouv_obst_dist)
            
            transitions_possibles.append(Transition(self, etat_suiv, "takeoff_cmd"))

        # MOVE_STEP
        if(self.crashed == 0 and self.airborne == 1 and self.docked == 0 and self.battery > 0) :

            if(self.posX - 1 >= 0) :
                if((self.posX - 1, self.posY) in Danger) :
                    nouv_obst_dist = 0
                else :
                    nouv_obst_dist = 2

            
                etat_suiv = State(self.posX - 1, self.posY, self.battery - 1, self.crashed, self.docked, self.airborne,
                                   self.visZones | frozenset([zoneOf(self.posX - 1, self.posY, maxX, maxY)]), nouv_obst_dist)
                transitions_possibles.append(Transition(self, etat_suiv, "move_step"))

            if(self.posX + 1 < maxX) :
                if((self.posX + 1, self.posY) in Danger) :
                    nouv_obst_dist = 0
                else :
                    nouv_obst_dist = 2
                etat_suiv = State(self.posX + 1, self.posY, self.battery - 1, self.crashed, self.docked, self.airborne, 
                                  self.visZones | frozenset([zoneOf(self.posX + 1, self.posY, maxX, maxY)]), nouv_obst_dist)
                transitions_possibles.append(Transition(self, etat_suiv, "move_step"))

            if(self.posY - 1 >= 0) :
                if((self.posX, self.posY - 1) in Danger) :
                    nouv_obst_dist = 0
                else :
                    nouv_obst_dist = 2
                etat_suiv = State(self.posX, self.posY - 1, self.battery - 1, self.crashed, self.docked, self.airborne,
                                   self.visZones | frozenset([zoneOf(self.posX, self.posY - 1, maxX, maxY)]), nouv_obst_dist)
                transitions_possibles.append(Transition(self, etat_suiv, "move_step"))

            if(self.posY + 1 < maxY) :
                if((self.posX, self.posY + 1) in Danger) :
                    nouv_obst_dist = 0
                else :
                    nouv_obst_dist = 2
                etat_suiv = State(self.posX, self.posY + 1, self.battery - 1, self.crashed, self.docked, self.airborne,
                                   self.visZones | frozenset([zoneOf(self.posX, self.posY + 1, maxX, maxY)]), nouv_obst_dist)
                transitions_possibles.append(Transition(self, etat_suiv, "move_step"))

        # AVOID_MANEUVER
        if(self.crashed == 0 and self.airborne == 1 and self.docked == 0 and self.battery > 1) :
            
            voisins = []

            if self.posX - 1 >= 0 :
                voisins.append((self.posX - 1, self.posY))

            if self.posX + 1 < maxX : 
                voisins.append((self.posX + 1, self.posY))

            if self.posY - 1 >= 0 :   
                voisins.append((self.posX, self.posY - 1))

            if self.posY + 1 < maxY : 
                voisins.append((self.posX, self.posY + 1))

            voisins_safe = []

            for v in voisins :
                if(v not in Danger) :
                    voisins_safe.append(v)

            if len(voisins_safe) > 0:
                for vX, vY in voisins_safe:
                    etat_suiv = State(vX, vY, self.battery - 2, self.crashed, self.docked, self.airborne, 
                                      self.visZones | frozenset([zoneOf(vX, vY, maxX, maxY)]), 2)
                    transitions_possibles.append(Transition(self, etat_suiv, "avoid_maneuver"))
            else:
                for vX, vY in voisins:
                    etat_suiv = State(vX, vY, self.battery - 2, self.crashed, self.docked, self.airborne, 
                                      self.visZones | frozenset([zoneOf(vX, vY, maxX, maxY)]), 0)
                    transitions_possibles.append(Transition(self, etat_suiv, "avoid_maneuver"))
        
        # RETURN_HOME
        if(self.crashed == 0 and self.airborne == 1 and self.docked == 0 and self.battery > 0) :
            if(self.posX < baseX) :
                nouv_posX = self.posX + 1
            elif(self.posX > baseX) :
                nouv_posX = self.posX - 1
            else :
                nouv_posX = self.posX

            if(self.posY < baseY) :
                nouv_posY = self.posY + 1
            elif(self.posY > baseY) :
                nouv_posY = self.posY - 1
            else :
                nouv_posY = self.posY

            if((nouv_posX, nouv_posY) in Danger) :
                nouv_obst_dist = 0
            else :
                nouv_obst_dist = 2

            etat_suiv = State(nouv_posX, nouv_posY, self.battery - 1, self.crashed, self.docked, self.airborne, 
                                  self.visZones | frozenset([zoneOf(nouv_posX, nouv_posY, maxX, maxY)]), nouv_obst_dist)
            transitions_possibles.append(Transition(self, etat_suiv, "return_home"))
        
        # CHARGE_STEP
        if(self.crashed == 0 and self.docked == 1) :
            if(self.battery <= 95) :
                nouv_bat = self.battery + 5
            else :
                nouv_bat = 100
            etat_suiv = State(self.posX, self.posY, nouv_bat, self.crashed, self.docked, self.airborne, self.visZones, self.obstacle_distance)
            transitions_possibles.append(Transition(self, etat_suiv, "charge_step"))
        
        # EMERGENCY_STOP
        etat_suiv = State(self.posX, self.posY, self.battery, 1, 0, 0, self.visZones, 0)
        transitions_possibles.append(Transition(self, etat_suiv, "emergency_stop"))

        # DOCK_CMD
        if(self.airborne == 1 and self.crashed == 0 and self.docked == 0 and (self.posX, self.posY) == (baseX, baseY)) :
            etat_suiv = State(self.posX, self.posY, self.battery, self.crashed, 1, 0, self.visZones, self.obstacle_distance)
            
            transitions_possibles.append(Transition(self, etat_suiv, "dock_cmd"))

        # UNDOCK_CMD
        if(self.airborne == 0 and self.crashed == 0 and self.docked == 1 and (self.posX, self.posY) == (baseX, baseY) and self.battery > 0) :
            etat_suiv = State(self.posX, self.posY, self.battery, self.crashed, 0, 1, self.visZones, self.obstacle_distance)
            
            transitions_possibles.append(Transition(self, etat_suiv, "undock_cmd"))

        return transitions_possibles

class Transition:
    def __init__(self, src: State, dest: State, label: str):
        self.src = src
        self.dest = dest
        self.etiq = label

    def destination(self):
        return self.dest
    

def init():

    maxX= int(input("rentrer la taille max x :"))


    maxY= int(input("rentrer la taille max y :"))

  
    baseX= int(input("rentrer x de la base :"))

    while(baseX<0 or baseX>maxX):
        baseX= int(input("rentrer x de la base :"))


    baseY= int(input("rentrer y de la base :"))

    while(baseY<0 or baseY>maxY):
        baseY= int(input("rentrer y de la base :"))

    
    posX= int(input("rentrer x du drone :"))
    while(posX<0 or posX>maxX):
        posX= int(input("rentrer x du drone :"))

    
    posY= int(input("rentrer y du drone :"))
    while(posY<0 or posY>maxY):
        posY= int(input("rentrer y du drone :"))

    
    airborne=0

    docked=0 

    crashed=0

    obstacle_distance = 2

    battery=100
    visZones=[zoneOf(posX,posY,maxX,maxY)]

    s_courant= State(posX,posY,battery,crashed,docked,airborne,visZones,obstacle_distance)
    return maxX,maxY,baseX,baseY,s_courant

def explore(s : State, S : set, maxDepth : int, maxBreadth: int, maxX, maxY, baseX, baseY, Danger):

    if s in S:
        return
    
    S.add(s)
    
    if (maxDepth != -1 and maxDepth <= 0) :
        return
    
    count = 0
    
    for t in s.generer_transitions(maxX, maxY, baseX, baseY, Danger):

        if maxBreadth != -1 and count >= maxBreadth:
            break

        if maxDepth == -1 :
            d_prime = -1 
        else :
            d_prime = maxDepth - 1

        explore(t.destination(), S, d_prime, maxBreadth, maxX, maxY, baseX, baseY, Danger)
        count += 1

def  zoneOf(x:int,y:int,maxX : int, maxY : int):
    if(x<=maxX/2 and y<=maxY/2):
        return 1
    elif(x<=maxX/2 and y>maxY/2):
        return 2
    elif(x>maxX/2 and y<=maxY/2):
        return 3
    elif(x>maxX/2 and y>maxY/2):
        return 4

def mov_poss(x,y):
    poss=[]
    if(x+1<maxX):
        poss.append((x+1,y))
    if(x-1>=0):
        poss.append((x-1,y))
    if(y+1<maxY):
        poss.append((x,y+1))
    if(y-1>=0):
        poss.append((x,y-1))
    return poss

def movestep(MaxX,MaxY,baseX,baseY,Danger,s_courant):
    if(s_courant.crashed==0 and s_courant.airborne==1 and s_courant.docked==0 and s_courant.battery>0):
        state_possible:list
        state_possible=state_poss(maxX,maxY,baseX,baseY,Danger,s_courant,1)
        print("[",end="")
        for i in range(0,len(state_possible),1):
            print(f"({state_possible[i].posX}, {state_possible[i].posY}),", end="")
        print("]")
        choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))
        while(choix<0 or choix>len(state_possible)-1):
            print("[")
            for i in state_possible:
                print("("+state_possible[i].posX+","+state_possible[i].posY+")"+",")
            print("]")
            choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))
        s_courant=state_possible[choix]
    else:
        print("Action Impossible")
    return s_courant


def state_poss(MaxX,MaxY,baseX,baseY,Danger,s:State,bat_loss):
    poss=[]
    if(s.posX+1<maxX):
        posiX=s.posX+1
        posiY=s.posY
        air=s.airborne
        if(s.crashed):
            air=0
        if((posiX,posiY) in Danger):
            obs=0
        else:
            obs=2
        if(zoneOf(posiX,posiY,maxX,maxY) not in s.visZones):
            tab=s.visZones | frozenset([zoneOf(posiX, posiY,maxX,maxY)])  
        else:
            tab=s.visZones
        poss.append(State(posiX,posiY,s.battery-bat_loss,s.crashed,s.docked,air,tab,obs))
    if(s_courant.posX-1>=0):
        posiX=s.posX-1
        posiY=s.posY
        air=s.airborne
        if(s.crashed):
            air=0
        if((posiX,posiY) in Danger):
            obs=0
        else:
            obs=2
        if(zoneOf(posiX,posiY,maxX,maxY) not in s.visZones):
            tab=s.visZones | frozenset([zoneOf(posiX, posiY,maxX,maxY)])
        else:
            tab=s.visZones
        poss.append(State(posiX,posiY,s.battery-bat_loss,s.crashed,s.docked,air,tab,obs))
    if(s_courant.posY+1<maxY):
        posiX=s.posX
        posiY=s.posY+1
        air=s.airborne
        if(s.crashed):
            air=0
        if((posiX,posiY) in Danger):
            obs=0
        else:
            obs=2
        if(zoneOf(posiX,posiY,maxX,maxY) not in s.visZones):
            tab=s.visZones | frozenset([zoneOf(posiX, posiY,maxX,maxY)])
        else:
            tab=s.visZones
        poss.append(State(posiX,posiY,s.battery-bat_loss,s.crashed,s.docked,air,tab,obs))
    if(s_courant.posY-1>=0):
        posiX=s.posX
        posiY=s.posY-1
        air=s.airborne
        if(s.crashed):
            air=0
        if((posiX,posiY) in Danger):
            obs=0
        else:
            obs=2
        if(zoneOf(posiX,posiY,maxX,maxY) not in s.visZones):
            tab=s.visZones | frozenset([zoneOf(posiX, posiY,maxX,maxY)])
        else:
            tab=s.visZones
        poss.append(State(posiX,posiY,s.battery-bat_loss,s.crashed,s.docked,air,tab,obs))
    return poss

def avoid_maneuver(MaxX,MaxY,baseX,baseY,Danger,s_courant):
    if(s_courant.crashed==0 and s_courant.airborne==1 and s_courant.docked==0 and s_courant.battery>1):
            
        state_possible:list
        state_possible=state_avoid(MaxX,MaxY,baseX,baseY,Danger,s_courant)
        print("[",end="")
        for i in range(0,len(state_possible),1):
            print(f"({state_possible[i].posX}, {state_possible[i].posY}),", end="")
        print("]")
        choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))
        while(choix<0 or choix>len(state_possible)-1):
            print("[")
            for i in state_possible:
                print("("+state_possible[i].posX+","+state_possible[i].posY+")"+",")
            print("]")
            choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))
        s_courant=state_possible[choix]
    else:
        print("Action Impossible")
    return s_courant
def state_avoid(MaxX,MaxY,baseX,baseY,Danger,s:State):
    res=[]
    state_possible=state_poss(MaxX,MaxY,baseX,baseY,Danger,s_courant,2)
    for i in range(0,len(state_possible),1):
        if(state_possible[i].obstacle_distance!=0):
            res.append(state_possible[i])
    if(len(res)>0):
        return res
    else:
        return state_possible

def afficher(maxX,maxY,baseX,baseY,Danger,s_courant) :

    ligne = " - "

    case_drone = " d "
    case_crash =" X "
    case_base = " b "
    case_obstacle = " o "

    for i in range (0, maxX) :
        for j in range(0, maxY) :
            if(i == s_courant.posX and j == s_courant.posY) :
                if(not s_courant.crashed):
                    print(case_drone, end="")
                else:
                    print(case_crash, end="")
            elif(i == baseX and j == baseY) :
                 print(case_base, end="")
            elif((i, j) in Danger) :
                print(case_obstacle, end="")
            else :
                print(ligne, end="")
        print("\n")
    print("battery:",end="")
    print(s_courant.battery)

def danger(maxX : int, maxY : int, baseX : int, baseY : int) :

    taux_danger = float(input("Choisissez un taux de danger (entre 0 et 1) :"))

    while(taux_danger<0 or taux_danger>1):
        taux_danger = float(input("Choisissez un taux de danger (entre 0 et 1) :"))

    cases = []
    for i in range(maxX):
        for j in range(maxY):
            if (i, j) != (baseX, baseY):
                cases.append((i, j))
    
    nb_dangers = int(maxX * maxY * taux_danger)
    nb_dangers = min(nb_dangers, maxX*maxY)

    return r.sample(cases, nb_dangers)
            
def takeoff_cmd(Danger,s_courant) :

    if(s_courant.crashed == 0 and s_courant.airborne == 0 and s_courant.docked == 0 and s_courant.battery > 0) :
        s_courant.airborne = 1
        if((s_courant.posX, s_courant.posY) in Danger) :
            s_courant.obstacle_distance = 0
        else :
             s_courant.obstacle_distance = 2
    return s_courant
def return_home(maxX,maxY,baseX,baseY,Danger,s_courant) :

    if(s_courant.crashed == 0 and s_courant.airborne == 1 and s_courant.docked == 0 and s_courant.battery > 0) :
        if(s_courant.posX < baseX) :
            nextX = s_courant.posX + 1

        elif(s_courant.posX > baseX) :
            nextX = s_courant.posX - 1

        else :
            nextX = s_courant.posX

        if(s_courant.posY < baseY) :
            nextY = s_courant.posY + 1

        elif(s_courant.posY > baseY) :
            nextY = s_courant.posY - 1

        else :
            nextY = s_courant.posY

        s_courant.posX = nextX
        s_courant.posY = nextY
        s_courant.battery = s_courant.battery - 1
        s_courant.visZones | frozenset([zoneOf(nextX, nextY,maxX,maxY)])

        if((nextX, nextY) in Danger):
           s_courant.obstacle_distance = 0
        else :
            s_courant.obstacle_distance = 2
    else:
        print("Action Impossible")
    return s_courant

def charge_step(s_courant) :
    if(s_courant.crashed == 0 and s_courant.docked == 1) :
        s_courant.battery = s_courant.battery + 5 if s_courant.battery <= 95 else 100
    return s_courant

def emergency_stop(s_courant) :

    s_courant.crashed = 1
    s_courant.airborne = 0
    s_courant.docked = 0
    s_courant.obstacle_distance = 0
    return s_courant


def auto(maxX,maxY,baseX,baseY,Danger,s_courant,valeurs) :
    act=0
    #parcours
    while(s_courant.crashed==0 and act<len(valeurs)):
        action=valeurs[act]
        act+=1
        match action:
            case 1:
                s_courant=movestep_auto(maxX,maxY,baseX,baseY,valeurs[act],valeurs[act+1],Danger,s_courant)
                act+=2
            case 2:
                s_courant=avoid_maneuver_auto(maxX,maxY,baseX,baseY,valeurs[act],valeurs[act+1],Danger,s_courant)
                act+=2
            case 3:
                s_courant=return_home(maxX,maxY,baseX,baseY,Danger,s_courant)
            case 4:
                s_courant=charge_step(s_courant)
            case 5:
                s_courant=emergency_stop(s_courant)
            case 6:
                s_courant=takeoff_cmd(Danger,s_courant)
            case 7:
                s_courant=dock_cmd(baseX,baseY,s_courant)
            case 8:
                s_courant=undock_cmd(s_courant)
        if(s_courant==1):
            return 1        
        afficher(maxX,maxY,baseX,baseY,Danger,s_courant)

def avoid_maneuver_auto(maxX,maxY,baseX,baseY,a,b,Danger,s_courant):
    if(s_courant.crashed==0 and s_courant.airborne==1 and s_courant.docked==0 and s_courant.battery>1):
        state_possible:list
        state_possible=state_avoid(maxX,maxY,baseX,baseY,Danger,s_courant)
        posiX=a
        posiY=b
        if((posiX<0 or posiX>maxX or (posiX!=s_courant.posX and posiX!=s_courant.posX+1 and posiX!=s_courant.posX-1)) or (posiY<0 or posiY>maxY or (posiY!=s_courant.posY and posiY!=s_courant.posY+1 and posiY!=s_courant.posY-1))):
            print("action impossible mauvaise coordonnées")
        else:
            air=s_courant.airborne
            if(s_courant.crashed):
                air=0
            if((posiX,posiY) in Danger):
                obs=0
            else:
                obs=2
            if(zoneOf(posiX,posiY,maxX,maxY) not in s_courant.visZones):
                tab=s_courant.visZones | frozenset([zoneOf(posiX, posiY,maxX,maxY)])
            else:
                tab=s_courant.visZones
            niu=State(posiX,posiY,s_courant.battery-2,s_courant.crashed,s_courant.docked,air,tab,obs)
            s_courant=niu
    else:
        print("Action Impossible")
        return 1
    return s_courant

def movestep_auto(maxX,maxY,baseX,baseY,a,b,Danger,s_courant):
    if(s_courant.crashed==0 and s_courant.airborne==1 and s_courant.docked==0 and s_courant.battery>1):
        posiX=a
        posiY=b
        if((posiX<0 or posiX>maxX or (posiX!=s_courant.posX and posiX!=s_courant.posX+1 and posiX!=s_courant.posX-1)) or (posiY<0 or posiY>maxY or (posiY!=s_courant.posY and posiY!=s_courant.posY+1 and posiY!=s_courant.posY-1))):
            print("action impossible movestep_auto")
        else:
            air=s_courant.airborne
            if(s_courant.crashed):
                air=0
            if((posiX,posiY) in Danger):
                obs=0
            else:
                obs=2
            if(zoneOf(posiX,posiY,maxX,maxY) not in s_courant.visZones):
                tab=s_courant.visZones | frozenset([zoneOf(posiX, posiY,maxX,maxY)])
            else:
                tab=s_courant.visZones
            niu=State(posiX,posiY,s_courant.battery-1,s_courant.crashed,s_courant.docked,air,tab,obs)
            s_courant=niu
    else:
        print("Action Impossible")
    return s_courant

def dock_cmd(baseX,baseY,s_courant):
    if(s_courant.airborne==1 and s_courant.crashed==0 and s_courant.docked==0 and s_courant.posX==baseX and s_courant.posY==baseY):
        s_courant.docked=1
        s_courant.airborne=0
    else:
        print("Action Impossible")
    return s_courant

def undock_cmd(s_courant):
    if(s_courant.battery>0 and s_courant.crashed==0 and s_courant.docked==1):
        s_courant.docked=0
        s_courant.airborne=1

    else:
        print("Action Impossible")
        return 1
    return s_courant

########################################################################################
#-----------------------------------------MAIN-----------------------------------------#
########################################################################################

mode=int(input("(1):manuel (2):auto (3):exhaustif"))
while(mode!=1 and mode!=2 and mode!=3):
    mode=int(input("(1):manuel (2):auto (3):exhaustif"))
if(mode==1):
    maxX,maxY,baseX,baseY,s_courant=init()
    Danger=danger(maxX,maxY,baseX,baseY)
    afficher(maxX,maxY,baseX,baseY,Danger,s_courant)
    while(not s_courant.crashed):
        choix=int(input("(1):Movstep (2):AvoidManeuveur (3):ReturnHome (4):Charge_Step (5):Emergency_Stop (6):Takeoff_cmd (7):dock_cmd (8):undock_cmd (9)quitter\n"))
        while(choix!=1 and choix!=2 and choix!=3 and choix!=4 and choix!=5 and choix!=6 and choix!=7 and choix!=8 and choix!=9):
            choix=int(input("(1):movstep (2):avoidmaneuveur (3):returnhome (4):charge_step (5):emergency_stop (6):takeoff_cmd (7):dock_cmd (8):undock_cmd (9)quitter\n"))
        match choix:
            case 1:
                s_courant=movestep(maxX,maxY,baseX,baseY,Danger,s_courant)
            case 2:
                s_courant=avoid_maneuver(maxX,maxY,baseX,baseY,Danger,s_courant)
            case 3:
                s_courant=return_home(maxX,maxY,baseX,baseY,Danger,s_courant)
            case 4:
                s_courant=charge_step(s_courant)
            case 5:
                s_courant=emergency_stop(s_courant)
            case 6:
                s_courant=takeoff_cmd(Danger,s_courant)
            case 7:
                s_courant=dock_cmd(baseX,baseY,s_courant)
            case 8:
                s_courant=undock_cmd(s_courant)
            case 9:
                break
        afficher(maxX,maxY,baseX,baseY,Danger,s_courant)
elif(mode==2):
    maxX,maxY,baseX,baseY,s_courant=init()
    Danger=danger(maxX,maxY,baseX,baseY)
    while(True):
        fichier=input("Nom du fichier commande (x pour quitter): ")
        if(fichier=="x"):
            break
        try:
            with open(fichier, 'r') as f:
                # On lit tout le contenu d'un coup pour ne rien rater
                contenu = f.read()
                
                # \d+ cherche toutes les suites de chiffres dans le texte
                valeurs = [int(n) for n in re.findall(r'\d+', contenu)]
        except FileNotFoundError:
            print("Erreur : Le fichier est introuvable.")
        auto(maxX,maxY,baseX,baseY,Danger,s_courant,valeurs)
elif(mode==3):
    grid_maxX,grid_maxY,base_X,base_Y,s0=init()
    liste_danger = danger(grid_maxX, grid_maxY, base_X, base_Y)


    etats_visites = set()

    print("Lancement de l'exploration...")
    explore(s0, etats_visites, maxDepth=10000, maxBreadth=20, maxX=grid_maxX, maxY=grid_maxY, baseX=base_X, baseY=base_Y, Danger=liste_danger)
    
    print(f"Exploration terminée ! L'algorithme a découvert {len(etats_visites)} états uniques.")
