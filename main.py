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
        self.tOut:list

class Transition:
    def __init__(self, src: State, dest: State, action: str,p:float):
        self.src=src
        self.dest=dest
        self.action=action
        self.p
    


    
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

    
    posX= int(input("rentrer x du drone :"))
    while(posX<0 or posX>maxX):
        posX= int(input("rentrer x du drone :"))

    
    posY= int(input("rentrer y du drone :"))
    while(posY<0 or posY>maxY):
        posY= int(input("rentrer y du drone :"))

    
    airborne=1

    docked=0 

    crashed=0

    obstacle_distance = 2

    battery=100
    visZones=[zoneOf(posX,posY)]
    global s_courant
    s_courant= State(posX,posY,battery,crashed,docked,airborne,visZones,obstacle_distance)


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

"""def movestep_old():
    global s_courant
    if(not(s_courant.crashed==0 and s_courant.airborne==1 and s_courant.docked==0 and s_courant.battery>0)):
        return Exception
    possible=mov_poss(s_courant.posX,s_courant.posY)
    state_possible=state_poss()
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
        airborne=0"""

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

def movestep():
    global s_courant
    if(not(s_courant.crashed==0 and s_courant.airborne==1 and s_courant.docked==0 and s_courant.battery>0)):
        return Exception
    state_possible:list
    state_possible=state_poss(s_courant,1)
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
        if((i, j) not in Danger and (i, j) != (s_courant.posX, s_courant.posY) and (i,j) != (baseX, baseY)) :
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




def mess(step,avoid):
    i=1


    return

#main
#init()
#danger()
#afficher()
mode=int(input("(1):manuel (2):auto (3):exhaustif"))
while(mode!=1 and mode!=2 and mode!=3):
    mode=int(input("(1):manuel (2):auto (3):exhaustif"))
if(mode==1):
    init()
    danger()
    afficher()
    while(not s_courant.crashed):
        #message=mess()
        choix=int(input("(1):Movstep (2):AvoidManeuveur (3):ReturnHome (4):Charge_Step (5):Emergency_Stop (6):Takeoff_cmd\n"))
        while(choix!=1 and choix!=2 and choix!=3 and choix!=4 and choix!=5 and choix!=6):
            choix=int(input("(1):movstep (2):avoidmaneuveur (3):returnhome (4):charge_step (5):emergency_stop (6):takeoff_cmd\n"))
        match choix:
            case 1:
                movestep()
            case 2:
                avoid_maneuver()
            case 3:
                return_home()
            case 4:
                charge_step()
            case 5:
                emergency_stop()
            case 6:
                takeoff_cmd()
        afficher()
elif(mode==2):
    fichier=input("nom du fichier commande:")
    auto(fichier)




"""Transition{
State src;
State cible;
action;
float proba;}"""
