import random as r

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
        emergency_stop()
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
    b = int(maxX*maxY*taux_danger)

    for n in range(0, b) :
        if((i, j) not in Danger) :
            Danger.append((i, j))
        i = r.randint(0, maxX - 1)
        j = r.randint(0, maxY -1)
            
def takeoff_cmd() :
    global crashed
    global airbornee
    global docked
    global battery
    global Danger
    global posX
    global posY
    global obstacle_distance

    if(crashed == 0 and airbornee == 0 and docked == 0 and battery > 0) :
        airbornee = 1
        if((posX, posY) in Danger) :
            obstacle_distance = 0
            emergency_stop()
        else :
             obstacle_distance = 2

def return_home() :
    global crashed
    global airbornee
    global docked
    global battery
    global Danger
    global posX
    global posY
    global baseX
    global baseY
    global obstacle_distance
    global visZones

    if(crashed == 0 and airbornee == 1 and docked == 0 and battery > 0) :
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
           emergency_stop()
        else :
            obstacle_distance = 2

def charge_step() :
    global crashed
    global airbornee
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
    global airbornee
    global docked
    global obstacle_distance

    crashed = 1
    airbornee = 0
    docked = 0
    obstacle_distance = 0





#main
init()
danger()
afficher()
while(not crashed):
    choix=int(input("movstep:1 avoidmaneuveur:2 returnhome:3 returnhome:4 chargestep:5 takeoff_cmd:6\n"))
    while(choix!=1 and choix!=2 and choix!=3 and choix!=4 and choix!=5 and choix!=6):
        choix=int(input("movstep:1 avoidmaneuveur:2 returnhome:3 movstep:4 avoidmaneuveur:5 returnhome:6\n"))
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



"""Transition{
State src;
State cible;
action;
float proba;}"""