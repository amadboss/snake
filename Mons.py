from tkinter import *
from random import randint
window = Tk()
hauteur = window.winfo_screenheight()
largeur = window.winfo_screenwidth()
largeur = str(int(largeur/2))
hauteur = str(int(hauteur/1.1))
window.geometry(largeur+"x"+hauteur+"0")
LargeurPlateau = int(largeur) 
HauteurPlateau = int(hauteur)
#premier canva qu'on va placer a partir du haut
Plateau = Canvas(window, width = LargeurPlateau, height = HauteurPlateau, bg = "black")
Plateau.pack(side="top")


NombreDeCases= 40
LargeurCase = (LargeurPlateau / NombreDeCases)
HauteurCase = (HauteurPlateau / NombreDeCases)
print(LargeurCase)
print(HauteurCase)
def init_serpent (x, y):

    #on definit les 4 position des coin pour crée le serpent
    x1 = x * LargeurCase
    y1 = y * HauteurCase
    x2 = x1 + LargeurCase
    y2 = y1 + HauteurCase

    #remplissage du rectangle
    Plateau.create_rectangle(x1,y1,x2, y2, fill="white")

#On renvoie une case aléatoire
def case_aleatoire():

    AleatoireX = randint(0, NombreDeCases - 1)
    AleatoireY = randint(0, NombreDeCases - 1)

    return (AleatoireX, AleatoireY)

# affiche le serpent, l'argument étant la liste snake
def dessine_serpent(snake):

    #tant qu'il y a des cases dans snake
    for case in snake:

        # on récupère les coordonées de la case
        x, y = case
        # on colorie la case
        init_serpent(x, y)

########################################################################################################################

#On retourne le chiffre 1 si la case est dans le snake, 0 sinon
def etre_dans_snake(case):

    if case in SNAKE:
        EtreDedans = 1
    else:
        EtreDedans = 0

    return EtreDedans

#On renvoie un fruit aléatoire qui n'est pas dans le serpent
def fruit_aleatoire():

    # choix d'un fruit aléatoire
    FruitAleatoire = case_aleatoire()

    # tant que le fruit aléatoire est dans le serpent
    while (etre_dans_snake(FruitAleatoire)):
        # on prend un nouveau fruit aléatoire
        FruitAleatoire = case_aleatoire



#On renvoie un fruit aléatoire qui n'est pas dans le serpent
def fruit_aleatoire():

    # choix d'un fruit aléatoire
    FruitAleatoire = case_aleatoire()

    # tant que le fruit aléatoire est dans le serpent
    while (etre_dans_snake(FruitAleatoire)):
        # on prend un nouveau fruit aléatoire
        FruitAleatoire = case_aleatoire

    return FruitAleatoire

def dessine_fruit():

    global FRUIT

    x, y = FRUIT

    x1 = x * LargeurCase
    y1 = y * HauteurCase
    x2 = x1 + LargeurCase
    y2 = y1 + HauteurCase

    #On remplie l'ovale en rouge pour le fruit

    Plateau.create_rectangle(x1, y1, x2, y2, fill = "red")

########################################################################################################################

#Ces quatres fonctions permettent le déplacement dans quatres directions du serpent
#elles mettent à jour les coordonées du mouvement
def left_key(event):
    global MOUVEMENT
    MOUVEMENT = (-1, 0)

def right_key(event):
    global MOUVEMENT
    MOUVEMENT = (1, 0)

def up_key(event):
    global MOUVEMENT
    MOUVEMENT = (0, -1)

def down_key(event):
    global MOUVEMENT
    MOUVEMENT = (0, 1)

# indique les fonctions à appeler suite à une pression sur les flèches (ne fonctionne que si la fenêtre a le focus)
window.bind("<Left>", left_key)
window.bind("<Right>", right_key)
window.bind("<Up>", up_key)
window.bind("<Down>", down_key)


# met à jour la variable PERDU indiquant si on a perdu
def serpent_mort(NouvelleTete):

    global PERDU

    NouvelleTeteX, NouvelleTeteY = NouvelleTete

    # si le serpent se mange lui-même (sauf au démarrage, c'est-à-dire: sauf quand MOUVEMENT vaut (0, 0))
    # OU si on sort du canvas
    if (etre_dans_snake(NouvelleTete) and MOUVEMENT != (0, 0)) or NouvelleTeteX < 0 or NouvelleTeteY < 0 or NouvelleTeteX >= NombreDeCases or NouvelleTeteY >= NombreDeCases:
        # alors, on a perdu
        PERDU = 1

# met à jour le snake
def mise_a_jour_snake():

    global SNAKE, FRUIT

    # on récupère les coordonées de la tête actuelle
    (AncienneTeteX, AncienneTeteY) = SNAKE[0]
    # on récupère les valeurs du mouvement
    MouvementX, MouvementY = MOUVEMENT
    # on calcule les coordonées de la nouvelle tête
    NouvelleTete = (AncienneTeteX + MouvementX, AncienneTeteY + MouvementY)
    # on vérifie si on a perdu
    serpent_mort(NouvelleTete)
    # on ajoute la nouvelle tête
    SNAKE.insert(0, NouvelleTete)

    # si on mange un fruit
    if NouvelleTete == FRUIT:
        # on génère un nouveau fruit
        FRUIT = fruit_aleatoire()
    # sinon
    else:
        # on enlève le dernier élément du serpent (c'est-à-dire: on ne grandit pas)
        SNAKE.pop()
        

# fonction principale
def tache():

    # on met à jour l'affichage et les événements du clavier
    #window.update
    window.update_idletasks()
    # on met à jour le snake
    mise_a_jour_snake()
    # on supprime tous les éléments du plateau
    Plateau.delete("all")
    # on redessine le fruit
    dessine_fruit()
    # on redessine le serpent
    dessine_serpent(SNAKE)

    # si on a perdu
    if PERDU:
        exit()
    # sinon
    else:
        # on rappelle la fonction principale
        window.after(20, tache)

########################################################################################################################

# le snake initial: une liste avec une case aléatoire
SNAKE = [case_aleatoire()]
# le fruit initial
FRUIT = fruit_aleatoire()
# le mouvement initial, une paire d'entiers représentant les coordonées du déplacement, au départ on ne bouge pas
MOUVEMENT = (0, 0)
# la variable permettant de savoir si on a perdu, sera mise à 1 si on perd
PERDU = 0

# on appellera la fonction principale pour la première fois juste après être entré dans la boucle de la fenêtre
window.after(0, tache())
#window.mainloop()
