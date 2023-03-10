import pygame
from laser import Laser
from random import choice


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,width,speed):
        super().__init__()
        self.image = pygame.image.load('player.png').convert_alpha()
        self.width = width
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.can_shoot = True
        self.laser_time = 0
        self.cooldown = 600
        self.LASER_dict = {}
        self.lasers = pygame.sprite.Group()
        self.laser = pygame.mixer.Sound('audio_laser.wav')
        self.laser.set_volume(0.2)
        self.laser_count = 0
        self.Laser_Power = {'white':1,'blue':2,'green':3}
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x +=self.speed
            if self.rect.right >= self.width:
                self.rect.right = self.width
        if keys[pygame.K_LEFT]:
            self.rect.x -=self.speed
            if self.rect.left <= 0:
                self.rect.left = 0
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.shoot_laser()
            self.can_shoot= False
            self.laser_time = pygame.time.get_ticks()
    
    def recharge(self):
        if not self.can_shoot:
            time = pygame.time.get_ticks()
            if time - self.laser_time >=self.cooldown:
                self.laser_time = 0
                self.can_shoot = True
                
    def shoot_laser(self):
        coords = self.rect.center
        x_coord = coords[0]
        y_coord =coords[1]-15

        colors = ['white', 'blue', 'green']        
        color = choice(colors)
        damage = self.Laser_Power[color]

        L = Laser((x_coord, y_coord),5,self.rect.bottom,color,damage)
        self.lasers.add(L)
        self.LASER_dict[self.laser_count]=L
        self.laser.play()
        
    def update(self):
        self.get_input()        
        self.recharge()               
        self.lasers.update()