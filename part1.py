import random as r


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
        self.visZones = visZones    # Zones déjà visitées
        self.obstacle_distance = obstacle_distance
        self.transi:[]

    def transitions(self) :
        return self.transi
    
    def remplir_transition(self) :
        if (self.crashed == 0 and self.airborne == 0 and self.docked == 0 and self.battery > 0) :
            etat_suiv = State(self.posX, self.posY, self.battery, self.crashed, self.docked, 1, self.visZones, self.obstacle_distance)
            self.transi.append(Transition(self, etat_suiv, "takeoff_cmd"))

        if (self.crashed == 0 and self.airborne == 1 and self.docked == 0 and self.battery > 0) :
            states_possibles = state_poss(self, 1)
            
            for s in states_possibles :
                self.transi.append(Transition(self, s, "move_step" + (s.posX, s.posY)))
            
            (homeX, homeY) = return_home()

            self.transi.append(Transition(self, State(homeX, homeY, self.battery, self.crashed, self.docked, self.airborne, self.visZones, self.obstacle_distance)), "return_home")

        if (self.crashed == 0 and self.airborne == 0 and self.docked == 0 and self.battery > 1) :
            states_possibles = state_poss(self, 1)
            
            for s in states_possibles :
                self.transi.append(Transition(self, s, "move_step" + (s.posX, s.posY)))

        if(crashed == 0 and docked == 1) :
            if(battery <= 95) :
                bat = battery + 5
            else :
                bat = 100
            etat_suiv = State(self.posX, self.posY, bat, self.crashed, self.docked, self.airborne, self.visZones, self.obstacle_distance)
            self.transi.append(Transition(self, etat_suiv, "charge_step"))

        etat_suiv = State(self.posX, self.posY, self.battery, 1, 0, 0, self.visZones, 0)
        self.transi.append(Transition(self, etat_suiv, "emergency_stop"))

    def eq(self, other):
        if not isinstance(other, State):
            return False

        return (self.posX == other.posX) and (self.posY == other.posY) and (self.battery == other.battery) and (self.crashed == other.crashed) and (self.docked == other.docked) and (self.airborne == other.airborne) and (tuple(self.visZones) == tuple(other.visZones)) and (self.obstacle_distance == other.obstacle_distance)

    def __hash__(self):
        return hash((self.posX, self.posY, self.battery, self.crashed, self.docked, self.airborne, tuple(self.visZones), self.obstacle_distance))


class Transition:
    def __init__(self, src: State, dest: State, label: str):
        self.src = src
        self.dest = dest
        self.etiq = label

    def destination(self) :
        return self.dest
    
    
maxX:int
maxY:int
baseX:int
baseY:int
Danger =[]
Zonecount=4
grille:list

s_courant:State

def init():
    global maxX
    maxX= int(input("rentrer la taille max x :"))

    global maxY
    maxY= int(input("rentrer la taille max y :"))

    global baseX 
    baseX= int(input("rentrer x de la base :"))

    while(baseX<0 or baseX>maxX):
        baseX= int(input("rentrer x de la base :"))

    global baseY
    baseY= int(input("rentrer y de la base :"))

    while(baseY<0 or baseY>maxY):
        baseY= int(input("rentrer y de la base :"))

    global posX 
    posX= int(input("rentrer x du drone :"))
    while(posX<0 or posX>maxX):
        posX= int(input("rentrer x du drone :"))

    global posY
    posY= int(input("rentrer y du drone :"))
    while(posY<0 or posY>maxY):
        posY= int(input("rentrer y du drone :"))

    global airborne
    airborne=1

    global docked 
    docked=0

    global crashed
    crashed=0

    global obstacle_distance
    obstacle_distance = 2

    global visZones
    global battery
    battery=100
    visZones=[zoneOf(posX,posY)]

    global s_courant
    s_courant= State(posX,posY,battery,crashed,docked,airborne,visZones,obstacle_distance)

def state_poss(s:State,bat_loss):
    global baseX
    global baseY
    global Danger
    poss=[]
    if(s.posX+1<maxX):
        posiX=s.posX+1
        posiY=s.posY
        if(posiX==baseX and posiY==baseY):
            dock=1
            air=0
        else:
            dock=0
            air=1
        if(s.crashed):
            air=0
        if((posiX,posiY) in Danger):
            obs=0
        else:
            obs=2
        if((posiX,posiY) not in s.visZones):
            tab=s.visZones + [(posiX, posiY)]
        else:
            tab=s.visZones
        poss.append(State(posiX,posiY,s.battery-bat_loss,s.crashed,dock,air,tab,obs))
    if(s_courant.posX-1>=0):
        posiX=s.posX-1
        posiY=s.posY
        if(posiX==baseX and posiY==baseY):
            dock=1
            air=0
        else:
            dock=0
            air=1
        if(s.crashed):
            air=0
        if((posiX,posiY) in Danger):
            obs=0
        else:
            obs=2
        if((posiX,posiY) not in s.visZones):
            tab=s.visZones + [(posiX, posiY)]
        else:
            tab=s.visZones
        poss.append(State(posiX,posiY,s.battery-bat_loss,s.crashed,dock,air,tab,obs))
    if(s_courant.posY+1<maxY):
        posiX=s.posX
        posiY=s.posY+1
        if(posiX==baseX and posiY==baseY):
            dock=1
            air=0
        else:
            dock=0
            air=1
        if(s.crashed):
            air=0
        if((posiX,posiY) in Danger):
            obs=0
        else:
            obs=2
        if((posiX,posiY) not in s.visZones):
            tab=s.visZones + [(posiX, posiY)]
        else:
            tab=s.visZones
        poss.append(State(posiX,posiY,s.battery-bat_loss,s.crashed,dock,air,tab,obs))
    if(s_courant.posY-1>=0):
        posiX=s.posX
        posiY=s.posY-1
        if(posiX==baseX and posiY==baseY):
            dock=1
            air=0
        else:
            dock=0
            air=1
        if(s.crashed):
            air=0
        if((posiX,posiY) in Danger):
            obs=0
        else:
            obs=2
        if((posiX,posiY) not in s.visZones):
            tab=s.visZones + [(posiX, posiY)]
        else:
            tab=s.visZones
        poss.append(State(posiX,posiY,s.battery-bat_loss,s.crashed,dock,air,tab,obs))
    return poss

def  zoneOf(x:int,y:int):
    global maxX
    global maxY
    if(x<=maxX/2 and y<=maxY/2):
        return 1
    elif(x<=maxX/2 and y>maxY/2):
        return 2
    elif(x>maxX/2 and y<=maxY/2):
        return 3
    elif(x>maxX/2 and y>maxY/2):
        return 4

def movestep():
    global posX
    global posY
    global battery
    global airborne
    global crashed
    global docked
    global obstacle_distance
    global visZones
    if(not(crashed==0 and airborne==1 and docked==0 and battery>0)):
        return Exception
    possible=mov_poss(posX,posY)
    print(possible)
    choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))
    while(choix<0 or choix>len(possible)-1):
        print(possible)
        choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))

    posX=possible[choix][0]
    posY=possible[choix][1]
    battery-=1
    if(zoneOf(posX,posY) not in visZones):
        visZones.append(zoneOf(posX,posY))
    if((posX,posY) in Danger):
        obstacle_distance=0
    else:
        obstacle_distance=2
    if((posX,posY)==(baseX,baseY)):
        docked=1
        airborne=0

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

def avoid_maneuver():
    global posX
    global posY
    global battery
    global airborne
    global crashed
    global docked
    global obstacle_distance
    global visZones
    if(not(crashed==0 and airborne==1 and docked==0 and battery>1)):
        return Exception
    possible=mov_poss(posX,posY)
    for i in range(len(possible)-1,-1,-1):
        if(possible[i] in Danger):
            possible.pop(i)
    if(len(possible)):
        print(possible)
        choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))
        while(choix<0 or choix>len(possible)-1):
            print(possible)
            choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))

        posX=possible[choix][0]
        posY=possible[choix][1]
        if(zoneOf(posX,posY) not in visZones):
            visZones.append(zoneOf(posX,posY))
        obstacle_distance=2
        battery-=2
    else:
        battery-=1
        movestep()



def afficher() :
    global maxX
    global maxY
    global posX
    global posY
    global baseX
    global baseY
    global Danger

    ligne = " - "

    case_drone = " d "
    case_crash =" X "
    case_base = " b "
    case_obstacle = " o "

    for i in range (0, maxX) :
        for j in range(0, maxY) :
            if(i == posX and j == posY) :
                if(not crashed):
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

def danger() :
    global maxX
    global maxY
    global Danger

    i = r.randint(0, maxX - 1)
    j = r.randint(0, maxY - 1)
    taux_danger = float(input("Choisissez un taux de danger (entre 0 et 1) :"))
    while(taux_danger<0 or taux_danger>1):
        taux_danger = float(input("Choisissez un taux de danger (entre 0 et 1) :"))
    b = int(maxX*maxY*taux_danger)
    n = 0

    while(n < b) :
        if((i, j) not in Danger and (i, j) != (posX, posY) and (i,j) != (baseX, baseY)) :
            Danger.append((i, j))
            n += 1
        i = r.randint(0, maxX - 1)
        j = r.randint(0, maxY -1)
            
def takeoff_cmd() :
    global crashed
    global airborne
    global docked
    global battery
    global Danger
    global posX
    global posY
    global obstacle_distance

    if(crashed == 0 and airborne == 0 and docked == 0 and battery > 0) :
        airborne = 1
        if((posX, posY) in Danger) :
            obstacle_distance = 0
        else :
             obstacle_distance = 2

def return_home() :
    global crashed
    global airborne
    global docked
    global battery
    global Danger
    global posX
    global posY
    global baseX
    global baseY
    global obstacle_distance
    global visZones

    if(crashed == 0 and airborne == 1 and docked == 0 and battery > 0) :
        if(posX < baseX) :
            nextX = posX + 1

        elif(posX > baseX) :
            nextX = posX - 1

        else :
            nextX = posX

        if(posY < baseY) :
            nextY = posY + 1

        elif(posY > baseY) :
            nextY = posY - 1

        else :
            nextY = posY

        posX = nextX
        posY = nextY
        battery = battery - 1
        visZones.append(zoneOf(nextX, nextY))

        if((nextX, nextY) in Danger):
           obstacle_distance = 0
        else :
            obstacle_distance = 2

    return (posX, posY)

def charge_step() :
    global crashed
    global airborne
    global docked
    global battery
    global Danger
    global posX
    global posY
    global obstacle_distance

    if(crashed == 0 and docked == 1) :
        battery = battery + 5 if battery <= 95 else 100


def emergency_stop() :
    global crashed
    global airborne
    global docked
    global obstacle_distance

    crashed = 1
    airborne = 0
    docked = 0
    obstacle_distance = 0


def auto(fich) :
    f=open(fich,'r')
    #init
    global maxX
    maxX= f.readline()[9]

    global maxY
    maxY= f.readline()[9]

    print(maxX)
    global baseX 
    baseX= f.readline()[11]

    if(baseX<0 or baseX>maxX):
        print("initialisation incorrecte\n")
        return

    global baseY
    baseY= f.readline()[11]

    if(baseY<0 or baseY>maxY):
        print("initialisation incorrecte\n")
        return

    global posX 
    posX= f.readline()[12]
    if(posX<0 or posX>maxX):
        print("initialisation incorrecte\n")
        return

    global posY
    posY= f.readline()[12]
    if(posY<0 or posY>maxY):
        print("initialisation incorrecte\n")
        return

    global airborne
    airborne=1

    global docked 
    docked=0 

    global crashed
    crashed=0

    global obstacle_distance
    obstacle_distance = 2

    global visZones
    global battery
    battery=100
    visZones=[zoneOf(posX,posY)]
    #parcours
    while():
        if(not(crashed==0 and airborne==1 and docked==0 and battery>0)):
            return Exception
        possible=mov_poss(posX,posY)
        choix=f.readline()[0]
        
        if(choix<0 or choix>len(possible)-1):
            print(possible)
            print("mouvement impossible\n")

        posX=possible[choix][0]
        posY=possible[choix][1]
        battery-=1
        if(zoneOf(posX,posY) not in visZones):
            visZones.append(zoneOf(posX,posY))
        if((posX,posY) in Danger):
            obstacle_distance=0
            emergency_stop()
        else:
            obstacle_distance=2
        if((posX,posY)==(baseX,baseY)):
            docked=1
            airborne=0


def explore(s : State, S, maxDepth, maxBreadth) :
    if(s in S) :
        return
    S.append(s)
    if(maxDepth != -1 and maxDepth <= 0) :
        return
    count = 0
    t : Transition
    for t in s.transi :
        if(maxBreadth != -1 and count >= maxBreadth) :
            break
        if(maxDepth == -1) :
            d = -1
        else :
            d = maxDepth - 1
        explore(t.destination(), S, d, maxBreadth)
        count += 1
    

def explorer_etats() :
    states : list[State]
    s0 = State(maxX, maxY, baseX, baseY, posX, posY, battery, crashed, docked, airborne, visZones, obstacle_distance)
    explore(s0, states, -1, -1)

    a_explorer = states
    deja_visite = list[State]
    deja_visite.append(s0)

    for s in a_explorer :
        
        s.remplir_transitions()
        explore(s, a_explorer, -1, -1)
        deja_visite.append(s)


#main
#init()
#danger()
#afficher()
"""init()
danger()
afficher()
states : list
s0 = State(posX, posY, battery, crashed, docked, airborne, visZones, obstacle_distance)
explore(s0, states, -1, -1)

a_explorer = states
deja_visite = []
deja_visite.append(s0)

for s in a_explorer :
    s.remplir_transitions()
    explore(s, a_explorer, -1, -1)
    deja_visite.append(s)"""
      




"""Transition{
State src;
State cible;
action;
float proba;}"""
