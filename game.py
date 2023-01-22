import pygame
from sys import exit
import copy
from player import  *
import obstacle

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
        
        self.create_multiple_obstacles(WIDTH*.15,WIDTH*.8,0,WIDTH*.33, WIDTH*.66)
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
        # update and draw sprite groups
        

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