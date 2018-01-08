'''Matthew Paulin
January 25, 2017
classes for 1943'''
import pygame #pygame module
import math as m #math module
#strings to load the plane images
string= 'frame'
string1= 'frame1'
string2= 'frame2'
string3= 'frame3'

#dimensions of the surface
width=800
height=600
middle = 400#middle of the surface

pexplosion=[]#list for plane explosion images
for i in range(1,9):#loading the gif into a list
    pexplosion.append(pygame.image.load('explosion'+str(i)+'.png'))

bexplosion=[]#list for bullet explosion images
for i in range(6):#loading the gif into a list
    bexplosion.append(pygame.image.load('bframe'+str(i)+'.png'))
    
bimages=[]#list for different bullet images
#lists for different planes
images=[]
images1=[]
images2=[]
images3=[]

for i in range(4):#loading the different plane images' gifs into lists
    images.append(pygame.image.load(string+str(i)+'.png'))
    images1.append(pygame.image.load(string1+str(i)+'.png'))
    images2.append(pygame.image.load(string2+str(i)+'.png'))
    images3.append(pygame.image.load(string3+str(i)+'.png'))
    
for i in range(4):#loading the different bullets into a list
    bimages.append(pygame.image.load('bullet'+str(i)+'.png'))
    
#loading the upgrade images for health, auto-fire, and more bullets
health=pygame.image.load('health.png')
autofireimg=pygame.image.load('autofireimg.png')
morebullets=pygame.image.load('morebullets.png')

  
class Plane(object):
    """ A plane
        data:               behaviour:
            x - x-value        move left/right/up/down
            y - y-value        draw
            w - width          collisions with walls/bullets/upgrades/other planes
            h - height         explode
            t - type of plane
            hp - health points
            frame - frame of gif
            score - score
            numbullets - number of bullets"""
    def __init__(self, x=middle, y=height, w=width, h=height,t=images, hp=100, frame=1,score=0,numbullets=1):
        '''setting all of the attributes of the object to the parameters of the method'''
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.t=t
        self.hp=hp
        self.frame=frame
        self.score=score
        self.score1=self.hp
        self.numbullets=numbullets
        self.autofire=False #autofire is always false until the autofire upgrade
    def pcollides(self, other):
        '''checks if a plane colides with another plane'''
        if self.x>other.x-self.w and self.x< other.x+other.w:#if the x-values collide
            if self.y>other.y-self.h and self.y< other.y+other.h:#if the y-values collide
                return True       
    def wcollides(self):
        '''checks if a plane collides with a wall to prevent  going off screen'''
        if self.t == images:#if the plane is the player
            if self.x<0 or self.x>width-self.w or self.y<0 or self.y>height-self.h:# if the plane collides
                return True
    def bcollides(self, other):
        '''checks if a plane collides with a bullet'''
        if other.x>=self.x and other.x<=self.x+self.w:#if the x-values collide
            if other.y>=self.y and other.y<=self.y+self.h:#if the y-values collide
                return True
    def ucollides(self,other):
        '''checks if a plane collides with an upgrade'''
        if self.x>=other.x and self.x<=other.x+86:#if the x-values collide
            if self.y>=other.y and self.y<=other.y+150:#if the y-values collide
                return True
    def draw(self, surface, frame=0):
        '''draw the plane on the screen'''
        if self.hp>0:#if the plane still has health
            surface.blit(self.t[frame], (self.x,self.y))#draw on the surface
    def right(self):
        '''moves a plane right'''
        if self.t==images:#if the plane is the player
            self.x+=5#move by 5 pixels at a time
        else:
            self.x+=10#move by 10 pixels at a time
    def left(self):
        '''moves the plane right'''
        self.x-=5#move 5 pixels left
    def up(self):
        '''moves the plane up'''
        self.y-=5#move up by 5 pixels
    def down(self):
        '''moves the plane down'''
        if self.t==images:#if the plane is the player
            self.y+=5#move down by 5 pixels
        else:
            self.y+=3#move down by 3 pixels
    def explode(self, surface):
        '''plane explodes when it has no hp left'''
        if self.frame<9 and self.hp<=0:#if the explosion has not already finished
            #resizing
            pexplosion[self.frame-1]=pexplosion[self.frame-1].convert_alpha()
            pexplosion[self.frame-1]=pygame.transform.scale(pexplosion[self.frame-1], (self.w, self.h))
            surface.blit(pexplosion[self.frame-1], (self.x, self.y))#draw the frame of the gif on the screen
            self.frame+=1#move to the next frame of the explosion

            
               
class Bullet(object):
    """ A bullet
        data:               behaviour:
            x - x-value        move up/down/towards the player
            y - y-value        draw
            w - width
            h - height         explode
            t - type of bullet
            hp - health points
            s - speed
            dx - direction of the x coordinate
            dy - direction of the y coordinate
            frame - frame of explosion gif"""
    def __init__(self, other, w, h, t, dx, dy, s, hp, frame=0):
        '''setting all of the attributes of the object to the parameters of the method'''
        if other.t==images:# if the bullet is from a player
            #spawn the bullet at the top centre of the plane
            self.x=other.x+(other.w//2)-(w//2)
            self.y=other.y
        else:
            #spawn at the bottom centre of the plane
            self.x=other.x+(other.w//2)-(w//2)
            self.y=other.y+other.h
        self.w=w
        self.h=h
        self.t=bimages[t]#setting the type to the corresponding image
        self.dx=dx
        self.dy=dy
        self.s=s
        self.hp=hp
        self.frame=frame

    def move(self):
        '''move the bullet according to the direction and speed'''
        self.y+=(self.dy)*self.s
        self.x+=(self.dx)*self.s

    def bdraw(self, surface, frame=0):
        '''draw the bullets if it has hp left'''
        if self.hp>0:
            surface.blit(self.t, (self.x, self.y))
            
            

    def move1(self, sx,sy):
        '''move the jet's bullets directly toward the player diagonally'''
        self.y+=-sy
        self.x+=-sx
    def explode(self, surface):
        '''explode the bullet and draw on the surface'''
        if self.frame<6 and self.hp<=0:#if the bullet has no hp and has not exploded already
            #resizing
            bexplosion[self.frame]=bexplosion[self.frame].convert_alpha()
            bexplosion[self.frame]=pygame.transform.scale(bexplosion[self.frame], (self.w, self.h))
            #draw the frame of the bullet's explosion
            surface.blit(bexplosion[self.frame], (self.x, self.y))
            self.frame+=1#move on to the next frame of the explosion
class Upgrade(object):
    """ An upgrade "parachute"
        data:               behaviour:
            x - x-value            move up/down/left/right
            y - y-value            draw    
            t - type of upgrade
            tl - time left before the upgrade despawns       
    """
    
    def __init__(self, other, t, tl=400):
        '''sets the attributes of the object to the corresponding parameter'''
        #spawns at the middle of the destroyed plane
        self.x=other.x+other.w//2
        self.y=other.y+other.h//2
        
        self.t=t#type
        self.tl=tl#time left
    def move(self):
        '''move the pgrade away from the edges of the surface'''
        if self.x<50:
            self.x+=2
        if self.x>height-136:
            self.x-=2
        if self.y<50:
            self.y+=2
        if self.y>height-236:
            self.y-=2
    def draw(self, surface):
        '''draws the upgrade on the surface'''
        surface.blit(self.t, (self.x, self.y))
        
    
    
            

    
    
