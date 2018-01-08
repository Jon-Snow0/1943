'''Matthew Paulin
January 25, 2017
1943 main program'''
#####modules#########
from classes import *#import the classes program
from random import randint as r #import the random module
import pygame#pygame module
pygame.init()#initialize pygame

############main variables#########
width=800#width of the screen
height=600#height of the screen
screen=pygame.display.set_mode((width,height))#setting a surface
red=(255,0,0)#red RGB value
green=(0,255,0)#green RGB value
pause = False#boolean to control if the game is paused
frame=0#frame for all the plane gifs is 0 (start of the gif)
framecount=0#frame counter
game=1#controls which screen is drawn(start, main, end)
score=0#score for the multiplayer option
multiplayer=False#boolean the controls if the mode is 2 player
playerone=True#boolean for 2 player mode that changes depending on the current player's number (P1, P2)
font = pygame.font.Font("typewriter.ttf",30)#smaller typewriter font
font1 = pygame.font.Font("typewriter.ttf",70)#larger typewriter font for end screen
bullets=[]#list for the bullets
enemy=[]#list for the enemy planes
sx=[]#list for the horizontal speed of the bullets
sy=[]#list for the vertical speed of the bullets
upgrades=[]#list for the upgrades

######loading images######
#loading and resizing the start screen background
startback=pygame.image.load('startback.jpg')
startback.convert_alpha()
startback=pygame.transform.scale(startback, (width, height))

#loading and resizing the endscreen background
endback=pygame.image.load('endback.jpg')
endback.convert_alpha()
endback=pygame.transform.scale(endback, (width, height))

#loading and resizing the choose mode picture
player1=pygame.image.load('1player.png')
player1.convert_alpha()
player1=pygame.transform.scale(player1, (130, 75))

#loading and resizing the water moving background
water=pygame.image.load('water.png')
water.convert_alpha()
water=pygame.transform.scale(water, (width,height))

#lists for different clouds
cloud=[]#list of images
cloudw=[]#width
cloudh=[]#height
cloudx=[]#x-value
cloudy=[]#y-value
for i in range(4):#loading and resizing the different clouds to random sizes
    cloud.append(pygame.image.load('cloud.png'))
    cloud[i].convert_alpha()
    cloudw.append(r(100,width//2))
    cloudh.append(r(50, height//4))
    cloud[i]=pygame.transform.scale(cloud[i],(cloudw[i],cloudh[i]))
    cloudx.append(0)
    cloudy.append(0)

backx=0#background's x coordinate
backy=0#first background's y coordinate
backy1=0-height#second background's y coordinate
#random x and y values for the clouds
cloudx[0]=r(0,width-cloudw[0])
cloudy[0]=r(-height,-height+height//2)
cloudx[1]=r(0,width-cloudw[1])
cloudy[1]=r(-height+height//2,0)
cloudx[2]=r(0,width-cloudw[2])
cloudy[2]=r(0,height//2)
cloudx[3]=r(0,width-cloudw[3])
cloudy[3]=r(height//2,height)

#loading the pause image
pauseimg=(pygame.image.load('pause.png'))
pauseimg = pauseimg.convert_alpha()
pauseimg = pygame.transform.scale(pauseimg, (width,height//3))

#######music and sound effects#########
#loading music and sound effects and setting the volumes
#pause sound
pauses = pygame.mixer.Sound('pause.wav')
pauses.set_volume(0.4)
#explosion sound
boom = pygame.mixer.Sound('boomsound.wav')   # 
boom.set_volume(0.2)
#upgrade sound
upgradesound = pygame.mixer.Sound('upgradesound.wav')   # 
upgradesound.set_volume(0.2)
#plane shooting sound
shoot = pygame.mixer.Sound('shootsound.wav')   # 
shoot.set_volume(0.2)
#game over sound
gameover = pygame.mixer.Sound('game over.wav')   # 
gameover.set_volume(0.4)
#title theme
titlesong = pygame.mixer.Sound('titlesong.wav')   # 
titlesong.set_volume(0.6)
titlesong.play()#play the title theme when the game starts
#final game over sound
endsong = pygame.mixer.Sound('endsong.wav')   # 
endsong.set_volume(0.4)
#main background song
pygame.mixer.music.load('gamesong0.wav')  #
pygame.mixer.music.set_volume(0.6)

################ FUNCTIONS #################
def upgrade(object):
    '''determines if an upgrade appears randomly when a plane is destroyed'''
    randnum=r(1,50)#random number b/w 1 and 50
    if randnum==1:#if the number is 1
        mytup=(morebullets,health,autofireimg)#tuple to choose type of upgrade
        upgrades.append(Upgrade(object, mytup[r(0,2)]))#append the upgrade to the list of upgrades

def redraw():
    '''draw all the objects, background images on the screen
    checks for collisions and pops objects out of lists before they are drawn if the have no hp left'''
    #drawing moving background
    screen.blit(water,(backx,backy))
    screen.blit(water,(backx,backy1))
    #drawing clouds
    for i in range(len(cloud)):
        screen.blit(cloud[i],(cloudx[i],cloudy[i]))
    #drawing the upgrades
    for i in range(len(upgrades)):
        upgrades[i].tl-=1#reduce the time left for the upgrades to remain on screen
        upgrades[i].draw(screen)
        upgrades[i].move()#moving the upgrades away from the edges
    for i in range(len(upgrades)-1,-1,-1):
        if player.ucollides(upgrades[i]):#iff the upgrades collide with the player
            upgradesound.play()#sound effect
            if upgrades[i].t==health:#if the upgrade is health, restore hp
                player.hp=100
            elif upgrades[i].t==morebullets:#if the upgrade is more bullets, add a bullet if the player has less that 5
                if player.numbullets<5:
                    player.numbullets+=1
                    player.autofire=False
            else:#if the upgrade is autofire, let the user fire the bullets automatically by holding spacebar
                player.autofire=True
            upgrades.pop(i)#pops the upgrade images from the list
        elif upgrades[i].tl<=0:#if the upgrade has no time left
            upgrades.pop(i)#despawn
    for i in range(len(player.t)):#draw the player's plane with the current frame of the gif
        player.t[i]= player.t[i].convert_alpha()
        player.t[i]=pygame.transform.scale(player.t[i], (player.w, player.h))
    player.draw(screen, frame)
    for i in range(len(bullets)-1,-1,-1):#cycles through all the bullets
        if bullets[i].hp<=0:                    #if the bullet has hit something
            bullets[i].explode(screen)          #draw bullet explosion images
            if bullets[i].frame>5:              #if the explosion's frame is more than 5, pop the bullet and speed values from their lists
                bullets.pop(i)
                sx.pop(i)
                sy.pop(i)
    for i in range(len(bullets)-1,-1,-1):       #cycles through remainng bullets              
        if bullets[i].y>height or bullets[i].y<-50 or bullets[i].x>width or bullets[i].x<-50:#pop the bullets if they go offscreen
            bullets.pop(i)
            sx.pop(i)
            sy.pop(i)
    for i in range(len(bullets)):               #cycles though remaining bullets and resizes and draws them
        bullets[i].t=bullets[i].t.convert_alpha()
        bullets[i].t=pygame.transform.scale(bullets[i].t, (bullets[i].w,bullets[i].h))
        bullets[i].bdraw(screen)
    for i in range(len(enemy)-1,-1,-1):#cycles through all the enemy planes
        if enemy[i].hp<=0:#if the enemy has no hp left, explode
            enemy[i].explode(screen)
            if enemy[i].frame>=9:#if the explosion is finished, pop the plane from the list
                player.score+=enemy[i].score1
                upgrade(enemy[i])#create a chance for an upgrade
                enemy.pop(i)
    player.explode(screen)#explodes the player if no hp is left
    if player.frame>=9:#if the player's explosion is finished, play sound effect, move to end screen
        pygame.mixer.music.stop()
        endsong.play()
        game=3
    for i in range(len(enemy)):#cycles through remaining enemies
        for j in range(len(enemy[i].t)):#cycles through the gifs for all the enemy planes and draws and resizes them
            enemy[i].t[j]= enemy[i].t[j].convert_alpha()
            enemy[i].t[j]=pygame.transform.scale(enemy[i].t[j], (enemy[i].w, enemy[i].h))
        enemy[i].draw(screen, frame)
    if playerone:#if the first player is going in multiplayer mode, load the player's score 
        scoretxt=font.render('P1 SCORE: '+str(player.score), 1, (0,0,0))
        screen.blit(scoretxt,(25,0))
        
    elif multiplayer:#if the second player is going in multiplayer mode, load the player's score and the previous player's score
        scoretxt=font.render('P1 SCORE: '+str(score), 1, (0,0,0))
        screen.blit(scoretxt,(25,0))
        scoretxt=font.render('P2 SCORE: '+str(player.score), 1, (0,0,0))
        screen.blit(scoretxt,(500, 0))
    #draws an hp bar in the bottom left
    pygame.draw.rect(screen, green, ((0,height-25),(200,25)),0)
    pygame.draw.rect(screen, red, ((player.hp*2,height-25),(200-player.hp*2,height-25)),0)
    pygame.display.update()#update the display
    

############## MAIN PROGRAM ################
inPlay = True #start the game                                        
print('press p to pause') #instructions
print('Use the arrow keys to move and space to shoot')#instructions
while inPlay:#while in the game
    for event in pygame.event.get():#get the keyboard and mouse events
        if event.type == pygame.QUIT: #if the user tries to exit the window        
            inPlay = False#kill the program
        if event.type == pygame.KEYDOWN:#if the event is a key being pressed
            if event.key == pygame.K_SPACE and game==2 and pause==False:#if the key pressed is space and the game is resumed and in the main mode
                shoot.play()#play the shoot sound effect
                #spawns the corresponding number of bullets and their directions, speed, etc. depending on the number of bullets
                if player.numbullets==1:
                    bullets.append(Bullet(player, 20,20,0,0,-1,10,10))
                elif player.numbullets==2:
                    bullets.append(Bullet(player, 20,20,0,1,-2,10,10))
                    bullets.append(Bullet(player, 20,20,0,-1,-2,10,10))
                elif player.numbullets==3:
                    bullets.append(Bullet(player, 20,20,0,1,-2,10,10))
                    bullets.append(Bullet(player, 20,20,0,-1,-2,10,10))
                    bullets.append(Bullet(player, 20,20,0,0,-1,10,10))
                elif player.numbullets==4:
                    bullets.append(Bullet(player, 20,20,0,1,-2,10,10))
                    bullets.append(Bullet(player, 20,20,0,-1,-2,10,10))
                    bullets.append(Bullet(player, 20,20,0,1,-1,10,10))
                    bullets.append(Bullet(player, 20,20,0,-1,-1,10,10))
                elif player.numbullets==5:
                    bullets.append(Bullet(player, 20,20,0,1,-2,10,10))
                    bullets.append(Bullet(player, 20,20,0,-1,-2,10,10))
                    bullets.append(Bullet(player, 20,20,0,1,-1,10,10))
                    bullets.append(Bullet(player, 20,20,0,-1,-1,10,10))
                    bullets.append(Bullet(player, 20,20,0,0,-1,10,10))
                for i in range(player.numbullets):#cycles through the number of bullets and append x and y speed values
                    sx.append(1)
                    sy.append(1)
            elif event.key == pygame.K_p and game==2:#if the game is in the main mode and p is pressed
                if pause:#if the game is paused
                    pause=False#unpause
                    game=2
                    pygame.mixer.music.play(loops = -1)#restart teh music
                else:#if the game is not paused
                    pygame.mixer.music.stop()#stop the music
                    pauses.play()#play the pause sound
                    pause=True#pause the game
    if pause==False and game==2:#while the game is not paused
            keys = pygame.key.get_pressed()#get a list of keys pressed
            if keys[pygame.K_DOWN]:#if the down arrow key is pressed
                player.down()#move the player down
                if player.wcollides()==True:#if the player collides with a wall
                    player.up()#undo the movement
            elif keys[pygame.K_UP]:#if the up arrow key is pressed
                player.up()#move the player up
                if player.wcollides()==True:#if the player collides with a wall
                    player.down()#undo the movement
            elif keys[pygame.K_LEFT]:#if the left arrow key is pressed
                player.left()#move left
                if player.wcollides()==True:#if teh player collides with a wall
                    player.right()#undo the movement
            elif keys[pygame.K_RIGHT]:#if the right arrow key is pressed
                player.right()#move right
                if player.wcollides()==True:#if the player collides with a wall
                    player.left()#undo the movement
            elif keys[pygame.K_SPACE]:#if the spacebar is pressed
                if player.autofire and framecount%10==0:#if autofire is on and the frame is at a certain number
                    #shoot a bullet and pla the sound effect
                    shoot.play()
                    #spawns the corresponding number of bullets and their directions, speed, etc. depending on the number of bullets
                    if player.numbullets==1:
                        bullets.append(Bullet(player, 20,20,0,0,-1,10,10))
                    elif player.numbullets==2:
                        bullets.append(Bullet(player, 20,20,0,1,-2,10,10))
                        bullets.append(Bullet(player, 20,20,0,-1,-2,10,10))
                    elif player.numbullets==3:
                        bullets.append(Bullet(player, 20,20,0,1,-2,10,10))
                        bullets.append(Bullet(player, 20,20,0,-1,-2,10,10))
                        bullets.append(Bullet(player, 20,20,0,0,-1,10,10))
                    elif player.numbullets==4:
                        bullets.append(Bullet(player, 20,20,0,1,-2,10,10))
                        bullets.append(Bullet(player, 20,20,0,-1,-2,10,10))
                        bullets.append(Bullet(player, 20,20,0,1,-1,10,10))
                        bullets.append(Bullet(player, 20,20,0,-1,-1,10,10))
                    elif player.numbullets==5:
                        bullets.append(Bullet(player, 20,20,0,1,-2,10,10))
                        bullets.append(Bullet(player, 20,20,0,-1,-2,10,10))
                        bullets.append(Bullet(player, 20,20,0,1,-1,10,10))
                        bullets.append(Bullet(player, 20,20,0,-1,-1,10,10))
                        bullets.append(Bullet(player, 20,20,0,0,-1,10,10))
                    for i in range(player.numbullets):#add x and y speeds to their list
                        sx.append(1)
                        sy.append(1)
                
    
    if game==1: #Start screen, draws an image and two start buttons and moves to the main screen after the user presses one
        screen.blit(startback, (0,0))
        screen.blit(player1, (136, height-80))
        screen.blit(player1, (403, height-80))
        screen.blit(player1, (533, height-80))
        #gets the position of the cursor and if mouse is pressed, sets all variables to their starting values and moves to the main screen
        (mx,my)=pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if my>=height-80 and my<=height-5:
                if mx>=136 and mx<=266:
                    framecount=0
                    score=0
                    enemy=[]
                    sx=[]
                    sy=[]
                    bullets=[]
                    upgrades=[]
                    player=Plane(300,300, 100, 75, images, 100)
                    autofire=False
                    multiplayer=False
                    playerone=True
                    pygame.mixer.music.play(loops = -1)
                    titlesong.stop()
                    game=2
                elif mx>403 and mx<663:
                    playerone=True
                    multiplayer=True
                    framecount=0
                    score=0
                    enemy=[]
                    sx=[]
                    sy=[]
                    upgrades=[]
                    bullets=[]
                    player=Plane(300,300, 100, 75, images, 100)
                    autofire=False
                    titlesong.stop()
                    pygame.mixer.music.play(loops = -1)
                    game=2
                    
        pygame.display.update() #updates the display

    elif game==3: #Start screen, draws an image and a start button and moves to the main screen after the user presses start
        screen.blit(endback, (0,0))
        endtxt=font1.render('Game Over', 1, (0,0,0)) #############
        endtxt1=font.render('click to continue', 1, (0,0,0))
        screen.blit(endtxt,(230, 0))
        screen.blit(endtxt1,(240, 500))
        if multiplayer and playerone == False:
            if score>player.score:
                wintxt=font1.render('P1 Wins!!', 1, (255,255,255))
            else:
                wintxt=font1.render('P2 Wins!!', 1, (255,255,255))
            screen.blit(wintxt, (230,100))
        #gets the position of the cursor and if mouse is pressed, sets all variables to their starting values and moves to the main screen
        (mx,my)=pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if multiplayer:
                if playerone:
                    score=player.score
                    framecount=0
                    enemy=[]
                    sx=[]
                    sy=[]
                    bullets=[]
                    upgrades=[]
                    player=Plane(300,300, 100, 75, images, 100)
                    autofire=False
                    playerone=False
                    game=2
                    gameover.stop()
                    pygame.mixer.music.play(loops = -1)
                else:
                    game=1
                    endsong.stop()
                    titlesong.play()
            else:
                game=1
                endsong.stop()
                titlesong.play()
                    
        pygame.display.update() #updates the display
    elif game==2 and pause==False:#if the game is not paused and on the main screen
        framecount+=1#add to the frame count
        if framecount%4==0:#controls gif frames
            frame = (frame+1)%4
        if framecount%(300-2*(framecount//1000))==0:#spawns enemy fighters in one of 4 patterns
            randnum=r(1,4)
            if randnum==1:#|
                randx=r(0,width-100)
            elif randnum==2:#V
                randx=r(100,width-200)
            elif randnum==3:#/
                randx=r(0,width-300)
            else:#\
                randx=r(300,width-100)
            for i in range(3):#append objects to the list
                if randnum==1:#|
                    enemy.append(Plane(randx,-300-(i*75), 100, 75, images1, 10))
                elif randnum==2:#V
                    if i==2:
                        enemy.append(Plane(randx+(100),-300-75, 100, 75, images1, 10))
                    else:
                        enemy.append(Plane(randx-(i*100),-300-(i*75), 100, 75, images1, 10))
                elif randnum==3:#/
                    enemy.append(Plane(randx+(i*100),-300-(i*75), 100, 75, images1, 10))
                else:#\
                    enemy.append(Plane(randx-(i*100),-300-(i*75), 100, 75, images1, 10))
        elif framecount%(1000-2*(framecount//1000))==0:#add jets at a random y location
            randy=r(0,200)
            for i in range(3):#append jets to the enemy list
                enemy.append(Plane(-300-(i*100),randy, 150, 75, images2, 20))
        elif framecount%(2500-2*(framecount//1000))==0:#adds a boss plane and appends it to the enemy list
            enemy.append(Plane(width,100, 250,200,images3,100))
            
        for i in range(len(enemy)):#cycles through the enemies. If they are off screen spawn them just outside the screen to come in again
            if enemy[i].y>height+50:
                enemy[i].y=-150
            if enemy[i].x>width+50:
                enemy[i].x=-300
            randnum=r(0,200)
            if randnum==50 and enemy[i].t==images1: #appends bullets at a random time to the fighters
                bullets.append(Bullet(enemy[i], 20,20,1,0,1,5,10))
                sx.append(1)
                sy.append(1)
            elif 50<=randnum<=51 and enemy[i].t==images3:#appends bullets when the jets reach the centre of the screen
                bullets.append(Bullet(enemy[i], 25,25,1,0,1,5,15))
                bullets.append(Bullet(enemy[i], 25,25,1,-1,1,5,15))
                bullets.append(Bullet(enemy[i], 25,25,1,1,1,5,15))
                for k in range(3):
                    sx.append(1)
                    sy.append(1)
                    
                
            if enemy[i].t==images2 and enemy[i].x==width//2:#appends 3 bullets at a random time for the boss
                bullets.append(Bullet(enemy[i], 10,30,1,0,1,40,20))
                sx.append(int(((bullets[-1].x+bullets[-1].w/2)-(player.x+player.w/2))/bullets[-1].s))
                sy.append(int(bullets[-1].y+bullets[-1].h/2-player.y+player.h/2)/bullets[-1].s)
        #move the backgrounds, if they go below the bottom, spawn them at the top again
        backy+=2
        backy1+=2
        if backy>=height:
            backy=-height
        if backy1>=height:
            backy1=-height
        for i in range(len(cloud)):#respwans clouds with random attributes once they go offscreen
            cloudy[i]+=2
            if cloudy[i]>=height:
                cloudw[i]=(r(100,width//2))
                cloudh[i]=(r(50, height//3))
                cloudx[i]=r(0,width-cloudw[i])
                cloudy[i]=r(-height,0-cloudh[i])
        for i in range(len(bullets)):#cycles through the bullets, if th bullet is from a jet move them in a certain way
            if bullets[i].s==40:
                bullets[i].move1(sx[i],sy[i])
            else:#move all other bullets normally
                bullets[i].move()
        for i in range(len(enemy)):#cycles through the enemy planes, moves them differently depending on their type
            if enemy[i].t==images1:
                enemy[i].down()
            elif enemy[i].t==images2:
                enemy[i].right()
            elif enemy[i].t==images3:
                if enemy[i].x>275:
                    enemy[i].x-=5
                    
            for j in range(len(bullets)):#cycles through the bullets, if the player's bullets collide with an enemy reduce the enemy's hp
                if enemy[i].bcollides(bullets[j]) and bullets[j].s==10:
                    enemy[i].hp-=bullets[j].hp
                    if enemy[i].hp<0:
                        boom.play()#explosion sound effect
                        bullets[j].hp=-(enemy[i].hp)
                    else:
                        if enemy[i].hp==0:
                            boom.play()#explosion sound effect
                        bullets[j].hp=0
                if player.bcollides(bullets[j]):#if the player collides with a bullet, reduce the players hp
                    player.hp-=bullets[j].hp
                    if player.hp<=0:#end the game when the hp runs out, stop all music, start ending song
                        boom.play()
                        game=3
                        if playerone:
                            pygame.mixer.music.stop()
                            gameover.play()
                        else:
                            pygame.mixer.music.stop()
                            endsong.play()
                    else:
                        bullets[j].hp=0
            if enemy[i].pcollides(player) and enemy[i].hp>0:#if an enemy plane collides with the player, reduce hp accordingly
                player.hp-=enemy[i].hp
                enemy[i].hp-=100
                boom.play()#explosion sound effect
                if player.hp<=0:#end the game when the hp runs out, stop all music, start ending song
                    if playerone:
                        pygame.mixer.music.stop()
                        gameover.play()
                        game=3
                    else:
                        pygame.mixer.music.stop()
                        endsong.play()
                        game=3
                        
        redraw()#call the redraw function
    elif game==2:#while the game is paused show the pause image
        screen.blit(pauseimg, (0,width//2-(width//2)//2))
        pygame.display.update()#update the display
    pygame.time.delay(0)#delay
pygame.quit()#quit
