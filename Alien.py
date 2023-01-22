import pygame
class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        self.image = pygame.image.load(f'{color}.png')
        self.rect = self.image.get_rect(topleft=(x,y))
