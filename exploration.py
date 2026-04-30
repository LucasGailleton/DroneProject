import random as r
import sys
sys.setrecursionlimit(5000)


class State:
    def __init__(self, posX : int, posY : int, battery : int, crashed : int, docked : int, airborne : int, visZones : list, obstacle_distance : int):

        self.posX = posX
        self.posY = posY

        self.battery = battery
        self.crashed = crashed
        self.docked = docked
        self.airborne = airborne
        
        self.visZones = frozenset(visZones) 
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


def zoneOf(x : int, y : int, maxX : int, maxY : int):

    if(x<=maxX/2 and y<=maxY/2):
        return 1
    elif(x<=maxX/2 and y>maxY/2):
        return 2
    elif(x>maxX/2 and y<=maxY/2):
        return 3
    elif(x>maxX/2 and y>maxY/2):
        return 4


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

if __name__ == "__main__":

    grid_maxX = 6
    grid_maxY = 6
    base_X = 0
    base_Y = 0
    liste_danger = danger(grid_maxX, grid_maxY, base_X, base_Y)

    zone_base = zoneOf(base_X, base_Y, grid_maxX, grid_maxY)
    s0 = State(base_X, base_Y, 100, 0, 0, 0, [zone_base], 2)

    etats_visites = set()

    print("Lancement de l'exploration...")
    explore(s0, etats_visites, maxDepth=10000, maxBreadth=20, maxX=grid_maxX, maxY=grid_maxY, baseX=base_X, baseY=base_Y, Danger=liste_danger)
    
    print(f"Exploration terminée ! L'algorithme a découvert {len(etats_visites)} états.")
