import pygame
class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y,WIDTH):
        super().__init__()
        self.image = pygame.image.load(f'{color}.png')
        self.rect = self.image.get_rect(topleft=(x,y))
        
        self.WIDTH=WIDTH
    def move_down(self,y):
        self.y +=y     
            
    def update(self,speed):
                
        self.rect.x += speed
       