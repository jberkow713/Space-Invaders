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

        self.player_sprite = Player((WIDTH/2,HEIGHT),WIDTH,5)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
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
        self.alien_rows = 4
        self.alien_cols = 4
        self.alien_size = 40
        self.x_space = 10
        self.y_space = 10
        self.y_buffer = 100
        self.x_alien_buffer = self.calc_buffer()
        self.alien_speed = 1
        self.alien_Lasers = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.ALIEN_dict = {}
        self.alien_setup(self.alien_rows,self.alien_cols)        

        self.hit_count =0
        self.killed = None

        # Extra ship setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_timer = randint(40,80)
        # lives display
        self.lives = 3
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
        # TODO level increment, bosses, starting screen
    def level_up(self):
        # Resets level with increased speed
        self.ALIEN_dict = {}
        self.blocks.empty()
        self.alien_Lasers.empty()
        self.extra.empty()
        self.lives +=1        
        self.create_multiple_obstacles(self.buffer-30,WIDTH*.8,*self.obstacles)
        self.alien_setup(self.alien_rows,self.alien_cols)
        curr = abs(self.alien_speed)
        self.alien_speed = curr+1
        

    def calc_buffer(self):
        return (WIDTH - ((self.alien_size+self.x_space)*self.alien_cols))/2

    def alien_setup(self,rows,cols):
        colors = ['red', 'yellow', 'green']
        count = 0
        for row_idx,row in enumerate(range(rows)):
            for col_idx,col in enumerate(range(cols)):
                x = col_idx * self.alien_size + self.x_alien_buffer + col* self.x_space
                y = row_idx * self.alien_size + row*self.y_space + self.y_buffer
                alien_sprite = Alien(colors[row_idx%len(colors)],x,y,\
                    WIDTH,2)                    
                self.ALIEN_dict[count]=alien_sprite
                self.aliens.add(alien_sprite)
                count +=1
                

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
                
                if pygame.sprite.spritecollide(laser,self.aliens, False):
                    
                    for num,alien in self.ALIEN_dict.items():
                        ALIEN = alien.__dict__
                        laser_rect = laser.__dict__['rect']
                        alien_rect = ALIEN['rect']
                        health = alien.__dict__['health']
                        if pygame.Rect.colliderect(laser_rect, alien_rect)==1:
                            ALIEN['health'] = ALIEN['health']-1
                            if ALIEN['health']==0:
                                self.aliens.remove(self.ALIEN_dict[num])
                                self.killed = num

                    self.score+=abs(self.alien_speed)
                    self.explosion.play()
                    laser.kill()
                
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    self.score+=10*abs(self.alien_speed)
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
        life_surface = self.font.render(f'LIVES:{self.lives}',False,'green')
        life_rect = life_surface.get_rect(center=(725, 25))        
        screen.blit(life_surface, life_rect)
    
    def display_score(self):
        score_surface = self.font.render(f'SCORE:{self.score}',False,'green')
        score_rect_1 = score_surface.get_rect(center=(75, 25))        
        screen.blit(score_surface, score_rect_1)

        level_surface = self.font.render(f'LEVEL:{abs(self.alien_speed)}',False,'green')
        level_rect = level_surface.get_rect(center=(WIDTH/2 , 25))        
        screen.blit(level_surface, level_rect)

    def run(self):
        if not self.aliens:
            self.level_up()

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
        if self.killed in self.ALIEN_dict:
            del self.ALIEN_dict[self.killed]
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