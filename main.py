import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()


# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('Spiderbg.jpg')
background = pygame.transform.scale(background, (800, 600))

# Sound
mixer.music.load("spidertheme.mp3")
mixer.music.play()

# Caption and Icon
pygame.display.set_caption("SPIDY GAME")
icon = pygame.image.load('spiderweb.png')
pygame.display.set_icon(icon)

# web

webImg = pygame.image.load('web.png')
webImg = pygame.transform.scale(webImg, (150, 150))
webX = 480
webY = 350
web2Img = pygame.image.load('web2.webp')
web2Img = pygame.transform.scale(web2Img, (150, 150))
web2X = 10
web2Y = 300

# Player
playerImg = pygame.image.load('Shootingspider.png')
playerImg = pygame.transform.scale(playerImg, (150, 150))
playerX = 350
playerY = 450
playerX_change = 0


# web
websImg = []
websX = []
websY = []
websX_change = []
websY_change = []
num_of_webs = 10

for i in range(num_of_webs):
    websImg.append(pygame.image.load('spider.png'))
    websX.append(random.randint(100, 600))
    websY.append(random.randint(0,600))
    websX_change.append(1)
    websY_change.append(3)

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 16

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('goblin (1).png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 180))
    enemyX_change.append(2)
    enemyY_change.append(10)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('web1.png')
bulletImg = pygame.transform.scale(bulletImg, (50, 50))
bulletX = 0
bulletY = 380
bulletX_change = 2
bulletY_change = 2
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 200))


def player(x, y):
    screen.blit(playerImg, (x, y))

def web(x, y):
    screen.blit(webImg, (x, y))


def web2(x, y):
    screen.blit(web2Img, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
def webs(x, y, i):
    screen.blit(websImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def isCollision(websX, websY, bulletX, bulletY):
    distance = math.sqrt(math.pow(websX - bulletX, 2) + (math.pow(websY - bulletY, 2)))
    if distance < 10:
        return True
    else:
        return False

black=(0,0,0)
end_it=False
while (end_it==False):
    screen.fill(black)
    myfont=pygame.font.SysFont("Britannic Bold", 40)
    nlabel=myfont.render("Welcome in Spidy World", 1, (255, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            end_it=True
    screen.blit(nlabel,(200,200))
    pygame.display.flip()
# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_BACKSPACE:
                playerY_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound('shootsound.mp3')
                    bulletSound.play()
                    # Get the current x cordinate of the screen
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 650:
        playerX = 650

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 380:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]



        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound('shoot.mp3')
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

# webs Movement
    for i in range(num_of_webs):


        websX[i] += websX_change[i]
        if websX[i] <= 0:
            websX_change[i] = 0.5
            websY[i] += websY_change[i]
        elif websX[i] >= 700:
            websX_change[i] = -0.5
            websY[i] += websY_change[i]



        # Collision
        collision = isCollision(websX[i], websY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound('shoot.mp3')
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value -= 1
            websX[i] = random.randint(100, 736)
            websY[i] = random.randint(50, 700)

        webs(websX[i], websY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 400
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    web(webX, webY)
    web2(web2X, web2Y)
    pygame.display.update()