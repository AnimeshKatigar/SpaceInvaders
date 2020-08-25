import math
import random
import pygame
from pygame import mixer

pygame.init()
# Creating Screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("bk.png")


#Background Music
mixer.music.load("Cinematic-electronic-track.mp3")
mixer.music.play(-1)


# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

# Bullets
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 12
bullet_state = "ready"

# Ready state means it is not visible
# Fire state means actually fire


#Score

score_value = 0
font = pygame.font.Font('Dealer Strikes.otf', 32)
textX = 10
textY = 10

#Game Over text
gameover_font = pygame.font.Font('MAREN-font_V01.ttf', 64)

#Name
fnt = pygame.font.Font('space age.ttf', 55)
X = 130
Y = 10

# Enemy
enemyimg = []
enemyX = []
enemyY =[]
enemyX_change = []
enemyY_change = []
num_of_enemies = 8

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(30)

def show_name(x,y):
    name = fnt.render("~Space Invaders~", True, (255, 255, 255))
    screen.blit(name, (x, y))

def show_score(x,y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = gameover_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (270, 250))

def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance <= 27:
        return True
    return False


# Gameloop
running = True
while running:

    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":  # Only fires if bullets out of the window
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # Adding Boundaries for the spcaceship(Player)
        playerX = 736

    enemyX += enemyX_change


    # Enemy Movement
    for i in range(num_of_enemies):

        #GameOver
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            game_over_text()

        #Enemy Boundaries
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

            # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)



        enemy(enemyX[i], enemyY[i], i)



    # Bullet Movement
    if bulletY <= -5:  # Reloading the bullet if this goes beyond window
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change  # Bullet goes above the screen



    player(playerX, playerY)
    show_name(X, Y)
    show_score(textX, textY)
    pygame.display.update()
