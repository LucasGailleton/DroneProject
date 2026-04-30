Erwan FONTAINE, Lucas GAILLETON

# Manuel d'utilisation

### 1. Configuration Initiale

Après avoir choisie un mode, le programme vous demandera de définir les paramètres de l'environnement :

    Taille de la grille : Dimensions max en X et Y.

    Position de la base : Coordonnées où le drone peut se docker et recharger.

    Position de départ : Où se trouve le drone au début.

    Taux de danger : Un coefficient entre 0 et 1 (ex: 0.2 pour 20% d'obstacles).

    Maxdepth(uniquement pour le mode 3):

    maxBreadth(uniquement pour le mode 3): 

### 2. Les Modes de Fonctionnement
Au lancement, le programme vous demandera de choisir un mode:
#### Mode 1 : Manuel
D'abord vous devez faire la configuration initiale et l'interface affiche la grille.

Ensuite, vous contrôlez le drone en temps réel via le clavier, en saisissant le numéro de l'action souhaitée (voir tableau des commandes). Si l'action est impossible alors rien ne se passe.

L'interface affiche la grille après chaque action.

Vous saisissez le numéro de l'action souhaitée (voir tableau des commandes) et le programme s'arrete en cas de crash ou si vous choisissez l'action de quitter(action 9).

#### Mode 2 : Automatique
D'abord vous devez faire la configuration initiale et l'interface affiche la grille.
Nous avons fais le choix que la configuration initiale se fasse à la main et non dans le fichier de commandes, car notre génération de danger est aléatoire et donc il serait impossible de comparer plusieurs séquence de commande différente sur la même grille. 
Une solution à ce problèmes serait d'ajouter une fonction de lecture d'une grille (dans un fichier par exemple) mais nous nn'avons pas eu le temps de l'implémenter.

Ensuite, vous donnez le nom d'un fichier texte qui contient une séquence de commandes que le drone executera.

Format du fichier : Une suite de chiffres séparés par des espaces ou des retours à la ligne (on peut y ajouter du texte qui ne sera pas pris en compte).

    Exemple : 
        6 (Décollage)
        1 5 5 (mov_step vers la case 5,5)
        3 (return_home)
    ou 
        6 1 5 5 3

L'interface affiche la grille après chaque action.

Lorsque l'éxecution des commandes du fichier est terminé(ou en cas d'erreur dù à une action impossible), on vous demandera à nouveau un fichier de commandes(afin de pouvoir tester d'autre séquence de commande sur le même environnement),taper "x" pour mettre fin au programme.



#### Mode 3 : Exhaustif (Analyse)
D'abord vous devez faire la configuration initiale.
Ensuite,
  

### 3. Tableau des Commandes

|ID	|Commande	|Description|	Coût Batterie|
|-|-|-|-|
|1	|MoveStep|	Déplacement d'une case (Haut, Bas, Gauche, Droite).	|-1%
|2	|AvoidManeuver|	Déplacement d'une case en évitant les case avec un obstacle. Si toutes les cases accessibles ont un obstacle, propose les même cases que MoveStep.|	-2%
|3	|ReturnHome	|Le drone calcule seul le chemin vers la base et fais un déplacement d'une case vers celle-ci (Haut, Bas, Gauche, Droite,Diagonales).	|-1%
|4	|ChargeStep	|Recharge la batterie par paliers de +5% (doit être docké).|	+5%
|5	|EmergencyStop|	Arrêt d'urgence immédiat. Entraîne un crash.	|0
|6	|Takeoff	|Décollage du drone. Nécessaire au début pour bouger.	|0
|7	|Dock	|Atterrissage et arrimage à la base (si sur la case base).|	0
|8	|Undock	|Décollage de la base pour permettre le décollage.	|0
|9|Quitter|Met fin au programme en mode manuel||

### 4. Lecture de l'Interface (Symboles)


La grille s'affiche ainsi :

    - : Case vide (sûre).

    d : Position actuelle de votre drone.

    b : Emplacement de la station de recharge (Base).

    o : Obstacle / Zone de danger détectée.

    X : Emplacement du crash (fin de partie).