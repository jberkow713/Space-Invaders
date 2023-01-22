import pygame
from sys import exit
import copy
from player import  *

pygame.init()
# Globals
WIDTH=800
HEIGHT=800
Health = 100
BG = (30,30,30)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space_Invaders')

class Game:
    def __init__(self):
        player_sprite = Player((WIDTH/2,HEIGHT),WIDTH,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
    def run(self):
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
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