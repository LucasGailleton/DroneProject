import random as r


class State:
    def __init__(self, maxX, maxY,baseX,baseY,posX,posY,battery,crashed,docked,airborne,visZones,obstacle_distance):
        # Dimensions de la carte
        self.maxX = maxX
        self.maxY = maxY
        
        # Position de la base et du drone
        self.baseX = baseX
        self.baseY = baseY
        self.posX = posX
        self.posY = posY
        
        # États du drone (Booléens ou Int)
        self.battery = battery
        self.crashed = crashed
        self.docked = docked
        self.airborne = airborne
        
        # Données d'environnement
        self.vis_Zones = visZones    # Zones déjà visitées
        self.obstacle_distance = obstacle_distance

        self.transi : []

    def transitions(self) :
        return self.transi
    
    def remplir_transition(self) :
        if (self.crashed == 0 and self.airborne == 0 and self.docked == 0 and self.battery > 0) :
            etat_suiv = State(maxX, maxY, baseX, baseY, posX, posY, battery, crashed, docked, 1, visZones, obstacle_distance)
            self.transi.append(Transition(self, etat_suiv, "takeoff_cmd"))
        if (self.crashed == 0 and self.airborne == 1 and self.docked == 0 and self.battery > 0) :
            etat_suiv = State(maxX, maxY, baseX, baseY, posX, posY, battery - 1, crashed, docked, airborne, visZones, obstacle_distance)
            self.transi.append(Transition(self, etat_suiv, "move_step"))
    

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
posX:int
posY:int
battery:int
crashed:int
docked:int
airborne:int
visZones:list
obstacle_distance:int

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
init()
danger()
afficher()
states : list[State]
s0 = State(maxX, maxY, baseX, baseY, posX, posY, battery, crashed, docked, airborne, visZones, obstacle_distance)
explore(s0, states, -1, -1)

a_explorer = states
deja_visite = []
deja_visite.append(s0)

for s in a_explorer :

    deja_visite.append(s)
      




"""Transition{
State src;
State cible;
action;
float proba;}"""
