import pygame
class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y,WIDTH):
        super().__init__()
        self.image = pygame.image.load(f'{color}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.WIDTH=WIDTH                
    def update(self,speed):
        self.rect.x += speed
class Extra(pygame.sprite.Sprite):
    def __init__(self,side,screen_width):
        super().__init__()
        self.image = pygame.image.load('extra.png').convert_alpha()
        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3   
        self.rect = self.image.get_rect(topleft=(x,80))
    def update(self):
        self.rect.x +=self.speed

