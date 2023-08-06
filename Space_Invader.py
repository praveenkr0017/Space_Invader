import pygame
import random
from math import *

#Initialization og game must write this statement
pygame.init()


score_value=0
#Display of score
font = pygame.font.Font('godofwar.ttf',32)

scorex=10
scorey=10

def show_score(x,y):
    score = font.render('Score : ' + str(score_value) ,True,(200,200,255))
    screen.blit(score,(scorex,scorey))

#Game Over
over = pygame.font.Font('godofwar.ttf',50)
def gameover():
     gameover= over.render('Game Over' ,True,(200,200,255))
     screen.blit(gameover,(250,280))
isgameover=False

#Loading Background image
bg=pygame.image.load('background.png')

#Setting game screen size
screen = pygame.display.set_mode((800,600))

#Setting game title
pygame.display.set_caption("Space Invader ")

#Setting game logo
icon=pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Collision
def iscollision(x1,y1,x2,y2):
    d=sqrt(pow((x1-x2),2)+pow((y1-y2),2))
    if d<=28:
        return True
    else:
        return False

#Collision between player spaceship and enemy
def iscollision_player_and_enemy(x1,y1,x2,y2):
    if (x1-45<=x2 and x2<=x1+52) and (y1-57<=y2 and y2<=y1+64 ):
        return True
    else:
        return False

#Sound Effects
    #Background music
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)             #-1 is to play the music continuosly within the game loop
    #Loading bullet sound
bullet_sound = pygame.mixer.Sound('laser.wav')
    #Collision sound
collision_sound = pygame.mixer.Sound('explosion.wav')
    #Collision of enemy and spaceship.
col_sound = pygame.mixer.Sound('exp.wav')

#Player configurations
player_img=pygame.image.load('spaceship.png')
playerx=370
playery=450
def player(x,y):
    screen.blit(player_img,(x,y))
playerx_change=0
playery_change=0
    
#Enemy configurations
enemy_img = []
enemyx = []
enemyy =[]
enemyx_change =[]
enemyy_change =[]


# Multiple Enemy configurations
num_of_enemies=12
for i in range(num_of_enemies):
    if i<5:
        enemy_img.append(pygame.image.load('ufo.png'))
    else:
        enemy_img.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0,736))
    enemyy.append(random.randint(10,200))
    def enemy(x,y,i):
        screen.blit(enemy_img[i],(x,y))
    enemyx_change.append(4)
    enemyy_change.append(64)


#Bullet configurations
bullet_img=pygame.image.load('bullet.png')
def bullet(x,y):
    screen.blit(bullet_img,(x,y))
bullety=-9999
bulletx_change=0
bullety_change=-5
bullet_state='ready'    
#Bullet_state='ready' means bullet is ready to be fired but is not visible
#Bullet_state='fire' means bullet is firedand  is visible on screen

###############################################################################################

#Game Loop
run=True
while run:
    #Filling of colour according to RGB format
    screen.fill((0,0,0))

    #Setting background image
    screen.blit(bg,(0,0))
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        #Movement of player spaceship
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerx_change= -5
            if event.key == pygame.K_RIGHT:
                playerx_change= 5
            if event.key == pygame.K_UP:
                playery_change=-5
            if event.key == pygame.K_DOWN:
                playery_change=5
            if event.key == pygame.K_SPACE:
                if bullety<=0 or bullet_state=='ready' :
                    bullet_sound.play()
                    bullet_state = 'fire'
                    #Bullet configuration
                    bulletx=playerx+16
                    bullety=playery+16
        elif event.type == pygame.KEYUP:
            playerx_change=0
            playery_change=0

###############################################################################################

    #Setting boundation of player spaceship within the display screen
    playery+=playery_change 
    playerx+=playerx_change
    if playerx<=-2:
        playerx=0
    elif playerx>=738:
        playerx=736
    elif playery>=523:
        playery=523
    elif playery<=0:
        playery=0

    #To show the bullet on display screen continously
    if bullet_state == 'fire':
        bullety+=bullety_change
        #Movement of bullet
        bullet(bulletx,bullety)
        
            
            
    #To show the player space ship on display screen continously
    player(playerx,playery)

    #Multiple enemy
    for i in range(num_of_enemies):
        #Confinding the movement of enemy within the display screen.
        if enemyx[i]<=-2:
            enemyx_change[i]=3
            enemyy[i]+=enemyy_change[i]
        elif enemyx[i]>=738:
            enemyx_change[i]=-3
            enemyy[i]+=enemyy_change[i]
        #Movement of enemy
        enemyx[i]+=enemyx_change[i]
        #As soon as enemy go below the game display screen they regenerate
        if enemyy[i]>=535:
            enemyx[i]=random.randint(0,736)
            enemyy[i]=random.randint(10,200)

         #Collision
        if bullet_state == 'fire':
            collision=iscollision(bulletx,bullety,enemyx[i],enemyy[i])
            if collision and isgameover==False:
                collision_sound.play()
                score_value+=1
                bullet_state='ready'
                print(score_value,'  ',end='')
                enemyx[i]=random.randint(0,736)
                enemyy[i]=random.randint(10,200)

        #Collision between player and enemies.
        collision_player_and_enemy =iscollision_player_and_enemy(playerx,playery,enemyx[i],enemyy[i])
        if collision_player_and_enemy:
            if isgameover==False:
                col_sound.play()
            isgameover=True
            

        #To show the enemy on display screen continously
        if isgameover==True:
            gameover()
        else:
            enemy(enemyx[i],enemyy[i],i)
        
    '''#To terminate the game loop
    if collision_player_and_enemy:
        gameover()
        break
    '''
    #Score display continuosly on screen
    show_score(scorex,scorey)      
    

    #To implement any thing on the game display screen below statement must be implemented
    pygame.display.update()

print('Quit')
#To end game code
pygame.quit()
