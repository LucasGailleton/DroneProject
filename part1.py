import random as r

maxX = 5
maxY = 5
        
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


afficher()



