import pygame
from sys import exit
import random
from random import choice
from player import  *
import obstacle
from Alien import Alien
from laser import Laser

pygame.init()
# Globals
WIDTH=800
HEIGHT=800
Health = 100
BG = (30,30,30)
Block_Color = (241,79,80)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space_Invaders')

class Game:
    def __init__(self):
        player_sprite = Player((WIDTH/2,HEIGHT),WIDTH,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 8
        self.obstacles = [x*(WIDTH/self.obstacle_amount) for x in range(self.obstacle_amount)]
        # calculate evening spacing buffer
        self.range =self.obstacles[-1]-self.obstacles[0]
        self.buffer = (WIDTH - self.range) / 2
        self.create_multiple_obstacles(self.buffer-30,WIDTH*.8,*self.obstacles)
        self.alien_rows = 6
        self.alien_cols = 12
        self.alien_size = 40
        self.x_space = 10
        self.y_space = 10
        self.x_alien_buffer = self.calc_buffer()
        self.alien_speed = 1
        self.alien_Lasers = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_setup(self.alien_rows,self.alien_cols)
    
    def calc_buffer(self):
        return (WIDTH - ((self.alien_size+self.x_space)*self.alien_cols))/2

    def alien_setup(self,rows,cols):
        colors = ['red', 'yellow', 'green']
        for row_idx,row in enumerate(range(rows)):
            for col_idx,col in enumerate(range(cols)):
                x = col_idx * self.alien_size + self.x_alien_buffer + col* self.x_space
                y = row_idx * self.alien_size + row*self.y_space
                alien_sprite = Alien(colors[row_idx%len(colors)],x,y,\
                    WIDTH)
                self.aliens.add(alien_sprite)
    def change_dir(self,distance):
        for alien in self.aliens:
            if alien.rect.right>=WIDTH or alien.rect.left <= 0:
                self.alien_speed *=-1
                # if aliens remain
                if self.aliens:
                    for alien in self.aliens.sprites():
                        alien.rect.y +=distance
                return

    def alien_shoot(self):
        if random.randint(0,100)>97:

            if self.aliens.sprites():
                rand = choice(self.aliens.sprites())
                laser = Laser(rand.rect.center,-3,HEIGHT)
                self.alien_Lasers.add(laser)

    def create_obstacle(self,x_start,y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, val in enumerate(row):
                if val =='x':
                    x = col_index *self.block_size + x_start + offset_x
                    y = row_index *self.block_size + y_start
                    block = obstacle.Block(self.block_size,Block_Color,x,y)
                    self.blocks.add(block) 
    
    def create_multiple_obstacles(self, x_start,y_start, *offset):
        for offset_x in offset:
            self.create_obstacle(x_start,y_start,offset_x)

    def run(self):
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.update(self.alien_speed)
        self.change_dir(16)        
        self.aliens.draw(screen)
        self.alien_shoot()
        self.alien_Lasers.update() 
        self.alien_Lasers.draw(screen)      
        

G = Game()

while True:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(BG)
    G.run()

    pygame.display.update()
    clock.tick(60)             