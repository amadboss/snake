import pygame
import sys
import time
import random

#Taille de l'ecran en pixel
taille_ecran_x = 1920
taille_ecran_y = 1080

#initialisation de pygame
pygame.init()

#initialisation du plateau de jeux
game_window = pygame.display.set_mode((taille_ecran_x, taille_ecran_y))

# couleur
noir = pygame.Color(0,0,0)
blanc = pygame.Color(255,255,255)
rouge = pygame.Color(255,0,0)
gris = pygame.Color(192,192,192)
rect_taille = 30

def init_vars():
    global tete, corp, pomme, pomme_bool, score, direction, mur, nb_mur, j
    direction = "RIGHT"
    j = 0
    tete = [120,60]
    corp = [[120,60]]
    nb_mur = random.randrange(5,30)
    mur = []
    pomme = [random.randrange(1,(taille_ecran_x // rect_taille)) * rect_taille,random.randrange(1,(taille_ecran_y // rect_taille)) * rect_taille]
    pomme_bool = True
    score = 0
init_vars()

def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (taille_ecran_x / 10, 15)
    game_window.blit(score_surface, score_rect)

def genere_mur():    
    for i in range(nb_mur):
        print("on entre",i,"fois")
        #double tableau style [[0], [1260, 780], [1], [90, 450], [2], [1350, 960], [3], [1830, 30]]
        mur.extend(([i],[random.randrange(1,(taille_ecran_x // rect_taille)) * rect_taille,random.randrange(1,(taille_ecran_y // rect_taille)) * rect_taille]))
        print(mur,"et i",i)
genere_mur()

while True:
    time.sleep(0.05)
    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:
            if ( event.key == pygame.K_UP
                and direction != "DOWN"):
                direction = "UP"
            elif  ( event.key == pygame.K_DOWN 
                and direction != "UP"):
                direction = "DOWN"
            elif  ( event.key == pygame.K_LEFT
                and direction != "RIGHT"):
                direction = "LEFT"
            elif  ( event.key == pygame.K_RIGHT
                    
                and direction != "LEFT"):
                direction = "RIGHT"
    
    if direction == "UP":
        tete[1] -= rect_taille
    elif direction == "DOWN":
        tete[1] += rect_taille
    elif direction == "LEFT":
        tete[0] -= rect_taille
    else:
        tete[0] += rect_taille
        
    if tete[0] < 0:
        tete[0] = taille_ecran_x - rect_taille
    elif tete[0] > taille_ecran_x - rect_taille:
        tete[0] = 0
    elif tete[1] < 0:
        tete[1] = taille_ecran_y - rect_taille
    elif tete[1] > taille_ecran_y - rect_taille:
        tete[1] = 0
        
    #eating apple
    corp.insert(0, list(tete))
    if tete[0] == pomme[0] and tete[1] == pomme[1]:
        score += 1
        pomme_bool = False
    else:
        corp.pop()

    # spawn food
    if not pomme_bool:
        pomme = [random.randrange(1,(taille_ecran_x // rect_taille)) * rect_taille, random.randrange(1,(taille_ecran_y // rect_taille)) * rect_taille]
        pomme_bool = True
        
    #remplisage du plateau en noir
    game_window.fill(noir)
    #spawn de la pomme
    pygame.draw.rect(game_window,rouge, pygame.Rect(pomme[0], pomme[1], rect_taille // 2, rect_taille// 2))
    #pour chaque mure dans le tableau. aficher un carer gris corespondant a la valeur du tableau sous jaccent 
    for j in range(0,nb_mur,2):
        pygame.draw.rect(game_window,gris, pygame.Rect(mur[j+1][0], mur[j+1][1], rect_taille, rect_taille))
        if tete[0] == mur[j+1][0] and tete[1] == mur[j+1][1]:
            init_vars()
    for pos in corp:
        pygame.draw.rect(game_window, blanc, pygame.Rect(pos[0] , pos[1] ,rect_taille , rect_taille ))
        
    
    # game over condiditons

    for block in corp[1:]:
        if tete[0] == block[0] and tete[1] == block[1]:
            init_vars()

    show_score(blanc, 'arial', 20)
    pygame.display.update()
