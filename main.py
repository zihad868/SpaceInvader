import pygame
import os
import os.path
import random
import math
from pygame import mixer


# Intilize the pygme
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('back.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon =  pygame.image.load("ufo2.png")
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load('space.png')
playerX = 360
playerY = 520
playerX_change = 0


#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score = font.render("Score: "+str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    game_over = font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


space = 0

def player(X,Y):
    screen.blit(playerImg,(X,Y))

# Enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# Ready - Can't see bullte on the screen
# Fire - The bullet currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 520
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def enemy(X,Y,i):
    screen.blit(enemyImg[i],(X,Y))


def fire_bullte(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16, y+10))


def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+ (math.pow(enemyY-bulletY,2)))

    if distance <27:
        return True
    else:
        return False


#Game Loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        # key stock press control left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
                print("L")

            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                print("R")

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                   bullet_sound = mixer.Sound('background.wav')
                   bullet_sound.play()
                   # Get the current x cordinate of the spaceship
                   bulletX = playerX
                   fire_bullte(bulletX,bulletY)
                space += 1
                print("Space: ",space)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # cheaking for boundary of spaceship
    playerX += playerX_change


    if playerX <= 0:
        playerX = 0
    elif playerX >=735:
        playerX = 735


    # Enemy Movement
    for i in range(num_of_enemies):

       # Game Over
       if enemyY[i] >450:
           for j in range(num_of_enemies):
               enemyY[j]=2000
           game_over_text()
           break

       enemyX[i] += enemyX_change[i]
       if enemyX[i] <= 0:
           enemyX_change[i] = 4
           enemyY[i] += enemyY_change[i]
       elif enemyX[i] >=735:
           enemyX_change[i] =  -4
           enemyY[i] += enemyY_change[i]

        # Collision
       collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
       if collision:
           collision_sound = mixer.Sound('background.wav')
           collision_sound.play()
           bulletY = 480
           bullet_state = "ready"
           score_value += 1
           enemyX[i] = random.randint(0, 735)
           enemyY[i] = random.randint(50, 150)

       enemy(enemyX[i], enemyY[i],i)

    # Buttet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullte(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()