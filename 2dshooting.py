import pygame
from random import randint

#initialize pygame
pygame.init()


#constant for game
WIDTH, HEIGHT = 600, 800
FPS = 30

#constant for colors (RGB VALUES)
RED = (255, 0,0)
BLUE = (0, 255, 0)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
WHITE = (255,255,255)


#global variable
SCORE = 0
LIFE = 3
GAMEOVER = False


#defining screen 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2d Shooter Game')  #set title
font32 = pygame.font.SysFont('Arial', 32) #initialize font style

#game over text
GameOverText = font32.render('Game Over', True, RED)


#single player instance
player = pygame.Rect(270, 700, 30, 30)

#its give new fresh enemy on every call
class Enemy :
    def spawnEnemy(this) :
        return pygame.Rect(randint(0, WIDTH-30), 0, 30, 30)

#its fire new fresh bullet form player on every call
class bullet: 
    def fire(this): 
        return pygame.Rect(player.x, player.y-30, 30, 30)

clock = pygame.time.Clock()

#list of gameobjects
fires = []
enemies = []

#main loop
running = True
while running : 
    
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
        #handling movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if player.x > 0: player.x -= 30
            if event.key == pygame.K_RIGHT:
                if player.x < WIDTH-30: player.x += 30
            if event.key == pygame.K_SPACE:
                fires.append(bullet().fire())


    #logic for spawning the enemies
    if GAMEOVER == False and len(enemies) < 5:
        enemies.append(Enemy().spawnEnemy())

    #display
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, player)

    #render enimes
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)
        enemy.y += randint(1,5)
        
    #render fires
    for fire in fires:
        pygame.draw.rect(screen, YELLOW, fire)
        fire.y -= 15

    #display score
    ScoreText = font32.render('Score : '+str(SCORE), True, WHITE)
    screen.blit(ScoreText, (450, 10))

    #display lifes
    LifeText = font32.render('lifes : '+str(LIFE), True, WHITE)
    screen.blit(LifeText, (20, 10))
   
    #bullet hit enemy
    for fire in fires:
        for enemy in enemies:
            if fire.colliderect(enemy):
                enemies.remove(enemy)
                fires.remove(fire)
                SCORE += 1
                break

    
    #if enemy crossed player line reduce life
    for enemy in enemies:
        if enemy.y > HEIGHT-30:
            LIFE -= 1
            enemies.remove(enemy)
            break


    #end game
    if LIFE <= 0:
        screen.blit(GameOverText, (250, 350))
        enemies = []
        GAMEOVER = True

    #bullets disposal to reduce extra calculation of bullets
    for fire in fires:
        if fire.y < 0 :
            fires.remove(fire)
            break

    #update Screen with limit 
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()

