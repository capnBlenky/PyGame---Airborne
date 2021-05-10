import pygame
import random
import os
from math import atan2, degrees, pi, cos, sin

#define window dimensions
WIDTH = 1200
HEIGHT = 800

#define some colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class helicopter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.imgNum = 0
        self.image = pygame.image.load("images/heli_{}.png".format(str(self.imgNum)))
        self.rect = self.image.get_rect()
        self.x, self.y = x,y
        if self.x > WIDTH:
            self.direction = -1
        else:
            self.direction = 1
        self.speed = 10
        super().__init__()
    def draw(self):
        if self.direction == 1:
            screen.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))

    def fly(self):
        self.x += self.speed*self.direction
        self.imgNum = (self.imgNum+1)%3
        self.image = pygame.image.load("images/heli_{}.png".format(self.imgNum))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))

class cannon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load('images/cannon.png')
        self.rect = self.image.get_rect()
        self.direction = 0
        self.x, self.y = x, y
        super().__init__()

    def draw(self):
        mpos = pygame.mouse.get_pos()
        dx = mpos[0] - self.x
        dy = mpos[1] - self.y
        rads = atan2(-dy,dx)
        rads %= 2*pi
        degs = degrees(rads)
        if degs > 300: 
            degs = 0
        elif degs > 90:
            degs = 90
        self.direction = degs
        newImage = pygame.transform.rotate(self.image,degs)
        newRect = newImage.get_rect()
        screen.blit(newImage, (self.x, self.y-newRect.bottom))
    
    def fire(self):
        mpos = pygame.mouse.get_pos()
        dx = mpos[0]-self.x
        dy = mpos[1]-self.y
        angle = atan2(dy,dx)
        bullets.add(bullet(self.x, self.y, angle))

class bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        self.rect = pygame.draw.rect(screen, BLACK, (x,y,5,5))
        self.x, self.y = x, y
        self.mx = cos(angle)
        self.my = sin(angle)
        self.speed = 20
        super().__init__()

    def draw(self):
        self.x += self.speed * self.mx
        self.y += self.speed * self.my
        self.rect = pygame.Rect(self.x,self.y, 5, 5)
        pygame.draw.rect(screen, BLACK, self.rect)

class shooter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load('images/shooter.png')
        self.rect = self.image.get_rect()
        self.x,self.y=x,y
        self.can = cannon(x+22, y+22)
        super().__init__()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        self.can.draw()

class parachuter(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()


def addHeli():
    xpos = random.choice(startxPositions)
    ypos = random.randint(50,200)
    helicopters.add(helicopter(xpos,ypos))

#Setup helicopters list to track all helicopters
helicopters = pygame.sprite.Group()
startxPositions = [-50,WIDTH+50]

#Create shooter with his cannon
player = shooter(20,HEIGHT-50)

#create bullets list
bullets = pygame.sprite.Group()

#track frame of game used for creating helicopters at specific period interval
frame = 0

while True:
    screen.fill(WHITE)
    for heli in helicopters:
        heli.fly()
        heli.draw()
    for heli in helicopters:
        if pygame.sprite.spritecollideany(heli,bullets):
            pygame.sprite.spritecollideany(heli,bullets).kill()
            heli.kill()
        elif heli.x > WIDTH+50 or heli.x < -50:
            heli.kill()
    for b in bullets:
        b.draw()
    for b in bullets:
        if b.x > WIDTH or b.y < 0:
            b.kill()
    frame += 1
    if frame % 75 == 0:
        addHeli()
    player.draw()
    
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.can.fire()
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    pygame.display.update()
    clock.tick(30)
pygame.quit()
quit()