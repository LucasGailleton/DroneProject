maxX:int
maxY:int
baseX:int
baseY:int
Danger ={(1,3),(2,3)}
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
    global visZonr
    global battery
    battery=100
    visZonr={zoneof(PosX,PosY,maxX,maxY)}


def  zoneof(x:int,y:int):
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
    global visZonr
    if(not(crashed==0 and airborn==1 and docked==0 and battery>0)):
        return Exception
    possible,t=mov_poss(PosX,PosY)
    print(possible)
    choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))
    while(choix<0 or choix>t-1):
        print(possible)
        choix=int(input("choisissez l'action à effectuer en tapant son indice\n"))

    PosX=possible[choix][0]
    PosY=possible[choix][1]
    battery-=1
    if(zoneof(PosX,PosY) not in visZonr):
        visZonr.append(zoneof(PosX,PosY))
    if((PosX,PosY) in Danger):
        obstacledistance=0
    else:
        obstacledistance=2

def mov_poss(x,y):
    poss=[]
    t=0
    if(x+1<maxX):
        poss.append((x+1,y))
        t+=1
    if(x-1>0):
        poss.append((x-1,y))
        t+=1
    if(y+1<maxY):
        poss.append((x,y+1))
        t+=1
    if(y-1>0):
        poss.append((x,y-1))
        t+=1
    return poss , t

def avoid_maneuver():
    return 1


#main
init()
movestep(PosX,PosY)
print(PosX)
print(PosY)
