import random as r

maxX:int
maxY:int
baseX:int
baseY:int
Danger ={}
Zonecount=4
grille:list
PosX:int
PosY:int
battery:int
crashed:int
docked:int
airborn:int
visZonr:list
obstacledistance:int

def init():
    global maxX
    maxX= int(input("rentrer la taille max x"))
    global maxY
    maxY= int(input("rentrer la taille max y"))
    global baseX 
    baseX= int(input("rentrer x de la base"))
    while(baseX<0 or baseX>maxX):
        baseX= int(input("rentrer x de la base"))
    global baseY
    baseY= int(input("rentrer y de la base"))
    while(baseY<0 or baseY>maxY):
        baseY= int(input("rentrer y de la base"))
    global PosX 
    PosX= int(input("rentrer x du drone"))
    while(PosX<0 or PosX>maxX):
        PosX= int(input("rentrer x du drone"))
    global PosY
    PosY= int(input("rentrer y du drone"))
    while(PosY<0 or PosY>maxY):
        PosY= int(input("rentrer y du drone"))
    global airborn
    airborn=1
    global docked 
    docked=0 
    global crashed
    crashed=0
    global visZones
    global battery
    battery=100
    visZones={zoneOf(PosX,PosY)}


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
    global PosX
    global PosY
    global battery
    global airborn
    global crashed
    global docked
    global obstacledistance
    global visZones
    if(not(crashed==0 and airborn==1 and docked==0 and battery>0)):
        return Exception
    possible=mov_poss(PosX,PosY)
    print(possible)
    choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))
    while(choix<0 or choix>len(possible)-1):
        print(possible)
        choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))

    PosX=possible[choix][0]
    PosY=possible[choix][1]
    battery-=1
    if(zoneOf(PosX,PosY) not in visZones):
        visZones.append(zoneOf(PosX,PosY))
    if((PosX,PosY) in Danger):
        obstacledistance=0
    else:
        obstacledistance=2

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
    global PosX
    global PosY
    global battery
    global airborn
    global crashed
    global docked
    global obstacledistance
    global visZones
    if(not(crashed==0 and airborn==1 and docked==0 and battery>1)):
        return Exception
    possible,t=mov_poss(PosX,PosY)
    for i in range(len(possible)-1,-1,-1):
        if(possible[i] in Danger):
            possible.pop(i)
    if(len(possible)):
        print(possible)
        choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))
        while(choix<0 or choix>t-1):
            print(possible)
            choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))

        PosX=possible[choix][0]
        PosY=possible[choix][1]
        if(zoneOf(PosX,PosY) not in visZones):
            visZones.append(zoneOf(PosX,PosY))
        obstacle_distance=2
    else:
        battery-=1
        movestep()



def afficher() :
    global maxX
    global maxY
    cases = "|__|"*maxX
    for i in range(0, maxY) :
            print(cases)


def danger(grille) :
    global maxX
    global maxY
    global Danger
    i = r.random(0, maxX)
    j = r.random(0, maxY)
    taux_danger = int(input("Choisissez un taux de danger (entre 0 et 1) :"))

    for n in range(0, len(grille)*taux_danger) :
        if((i, j) not in Danger) :
            Danger[n] = (i, j)
        i = r.random(0, maxX)
        j = r.random(0, maxY)
            
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

#main
init()
#movestep()
avoid_maneuver()
print(PosX)
print(PosY)
afficher()