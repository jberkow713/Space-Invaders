import pygame
from sys import exit

from random import choice,randint
from player import  *
import obstacle
from Alien import Alien, Extra
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
        self.obstacle_amount = 4
        self.obstacles = [x*(WIDTH/self.obstacle_amount) for x in range(self.obstacle_amount)]
        # calculate evening spacing buffer
        self.range =self.obstacles[-1]-self.obstacles[0]
        self.buffer = (WIDTH - self.range) / 2
        self.create_multiple_obstacles(self.buffer-30,WIDTH*.8,*self.obstacles)
        # Alien setup
        self.alien_rows = 6
        self.alien_cols = 12
        self.alien_size = 40
        self.x_space = 10
        self.y_space = 10
        self.y_buffer = 100
        self.x_alien_buffer = self.calc_buffer()
        self.alien_speed = 1
        self.alien_Lasers = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_setup(self.alien_rows,self.alien_cols)
        # Extra ship setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_timer = randint(40,80)
        # lives display
        self.lives = 3
        self.lives_surface = pygame.image.load('player.png').convert_alpha()
        self.player_width = self.lives_surface.get_size()[0]        
        self.lives_starting_x = WIDTH - (self.player_width*2) -30
        # score
        self.score = 0
        # font
        self.font = pygame.font.Font('Pixeled.ttf',20)
        # Sound
        self.music = pygame.mixer.Sound('space_music.wav')
        self.music.set_volume(0.2)
        self.music.play(loops=-1)
        self.laser = pygame.mixer.Sound('audio_laser.wav')
        self.laser.set_volume(0.3)
        self.alien_laser = pygame.mixer.Sound('audio_laser.wav')
        self.alien_laser.set_volume(0.13)           
        self.explosion = pygame.mixer.Sound('explosion.wav')
        self.explosion.set_volume(0.35)


    def calc_buffer(self):
        return (WIDTH - ((self.alien_size+self.x_space)*self.alien_cols))/2

    def alien_setup(self,rows,cols):
        colors = ['red', 'yellow', 'green']
        for row_idx,row in enumerate(range(rows)):
            for col_idx,col in enumerate(range(cols)):
                x = col_idx * self.alien_size + self.x_alien_buffer + col* self.x_space
                y = row_idx * self.alien_size + row*self.y_space + self.y_buffer
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
        if randint(0,300)>295:
            if self.aliens.sprites():
                rand = choice(self.aliens.sprites())
                laser = Laser(rand.rect.center,-3,HEIGHT)
                self.alien_Lasers.add(laser)
                self.alien_laser.play()
                
    def extra_alien_timer(self):
        self.extra_timer -=1
        if self.extra_timer<=0:
            side = ['right', 'left']
            self.extra.add(Extra(choice(side),WIDTH))
            self.extra_timer = randint(400,800)


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

    def collision_checks(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser,self.aliens,True):
                    self.score+=1
                    self.explosion.play()
                    laser.kill()
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    self.score+=10
                    laser.kill()
            # for extra in self.extra:    
        if self.alien_Lasers:
            for laser in self.alien_Lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives-=1
                    if self.lives ==0:
                        print('game over')
                        exit()
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)                    
                if pygame.sprite.spritecollide(alien,self.player,True):                    
                    print('game over')
                    exit()
    def display_lives(self):
        for life in range(self.lives-1):
            x = self.lives_starting_x + life * (self.player_width+10)            
            screen.blit(self.lives_surface,(x,10))
    
    def display_score(self):
        score_surface = self.font.render(f'Score:{self.score}',False,'white')
        score_rect_1 = score_surface.get_rect(center=(75, 25))        
        screen.blit(score_surface, score_rect_1)

    def run(self):
        self.player.update()
        self.alien_Lasers.update()
        self.extra.update()
        self.aliens.update(self.alien_speed)
        
        self.player.draw(screen)
        self.blocks.draw(screen)        
        self.change_dir(16)        
        self.aliens.draw(screen)
        self.extra.draw(screen)
        self.alien_Lasers.draw(screen)
        self.player.sprite.lasers.draw(screen)
        
        self.alien_shoot()
        self.extra_alien_timer()       
        self.collision_checks()
        self.display_lives()
        self.display_score()       

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