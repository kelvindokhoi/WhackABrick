from enum import Enum
from functions.Resource_Reader import image_loader
from functions.FilePaths import * #type:ignore
from functions.GameState import GameState
from functions.Music import Music
from functions.CalculateScore import caclculate_score
from pygame.sprite import * #type:ignore
from pygame.locals import * #type:ignore
import random
import pygame

class brickState(Enum):
    ABSENT = 0
    CHARACTER_A = 1
    CHARACTER_B = 2
    CHARACTER_C = 3
    CHARACTER_D = 4
    CHARACTER_E = 5
    DEAD = 6

class Brick(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = image_loader(brick_absent_image_path,(90,90))
        self.rect = Rect(x+70,y-10,90,90)
        self.status = brickState.ABSENT
        self.brickabsent = image_loader(brick_absent_image_path,(90,90))
        self.absent_image = self.brickabsent
        self.alive_image = self.brickabsent
        self.fading = False
        self.fade_alpha = 255
        self.original_image = None
    
    def update(self):
        if self.fading:
            self.fade_alpha -= 10  # Adjust this value to control fade speed (higher = faster fade)
            if self.fade_alpha <= 0:
                self.status = brickState.ABSENT
                self.image = self.absent_image
                self.fading = False
            else:
                faded = self.original_image.copy() #type:ignore
                faded.set_alpha(self.fade_alpha)
                self.image = faded

class Explosion(Sprite):
    def __init__(self, pos):
        Sprite.__init__(self)
        self.pos = pos
        self.max_radius = 300
        self.radius = 0
        self.alpha = 255
        self.color = (255, 165, 0)  # Orange for explosion
        self.done = False
        self.center = (self.max_radius, self.max_radius)
        self.image_size = (self.max_radius * 2, self.max_radius * 2)
        self.image = pygame.Surface(self.image_size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
    
    def update(self):
        self.radius += 8
        self.alpha -= 15
        if self.radius > self.max_radius or self.alpha < 0:
            self.done = True
        else:
            self.image.fill((0, 0, 0, 0))
            pygame.draw.circle(self.image, (*self.color, self.alpha), self.center, self.radius)

class BrickObject:
    def __init__(self):
        self.bricks = [[None for _ in range(5)] for _ in range(5)]
        x = 274
        y = 154
        for i in range(5):
            for j in range(5):
                self.bricks[i][j] = Brick(x,y) #type: ignore
                x += 274
            x = 274
            y += 154
        self.allbricks = Group(self.bricks)
        self.explosions = []

        self.brickPossibleConfig = [brickState.CHARACTER_A,brickState.CHARACTER_B,brickState.CHARACTER_C,brickState.CHARACTER_D,brickState.CHARACTER_E]
        self.brick_alive = [(state,image_loader(brick_img,(90,90))) for state,brick_img in zip(self.brickPossibleConfig,brick_paths)]
        self.aliveodds = 10
        self.absentodds = 10

    def brick_draw(self,screen):
        self.allbricks.draw(screen)

    def random_brick(self,gameState):
        if gameState==GameState.GAME_START:
            for i in range(5):
                for j in range(5):
                    # if brick was absent, randomly makeit alive
                    if self.bricks[i][j].status not in self.brickPossibleConfig and self.bricks[i][j].fading == False:
                        r = random.randint(1,self.aliveodds)
                        if r == 1:
                            selected = random.choice(self.brick_alive)
                            self.bricks[i][j].status = selected[0]
                            self.bricks[i][j].image = selected[1]
                    # if alive, randomly make it absent
                    elif self.bricks[i][j].status not in [brickState.ABSENT,brickState.DEAD]:
                        r = random.randint(1, self.absentodds)
                        if r == 1:
                            self.bricks[i][j].status = brickState.ABSENT
                            self.bricks[i][j].image = self.bricks[i][j].absent_image
        else:
            for i in range(5):
                for j in range(5):
                    self.bricks[i][j].status = brickState.ABSENT
                    self.bricks[i][j].image = self.bricks[i][j].absent_image

    def update_brick(self):
        for i in range(5):
            for j in range(5):
                self.bricks[i][j].update()
        for exp in self.explosions[:]:
            exp.update()
            if exp.done:
                self.explosions.remove(exp)
    
    def debug_mode_brick(self,screen,debug_mode):
        if debug_mode:
            for i in range(5):
                for j in range(5):
                    pygame.draw.rect(screen, (0,0,255), self.bricks[i][j].rect, 2)
    
    def blit_brick(self,screen):
        for brick in self.allbricks:
            if brick.status in self.brickPossibleConfig or brick.status == brickState.DEAD:
                screen.blit(brick.image, brick.rect)
        for exp in self.explosions:
            screen.blit(exp.image, exp.rect)
    
    def play_brick_hit_sound(self,music):
        music.play_brick_hit_sound()
    
    def if_brick_collide(self,cursor_Rect,playerPoints,buffs,music):
        for brick in self.allbricks:
            if brick.status in self.brickPossibleConfig and brick.rect.colliderect(cursor_Rect):
                brick.status = brickState.DEAD
                brick.fading = True
                brick.fade_alpha = 255
                brick.original_image = brick.image.copy()
                self.play_brick_hit_sound(music)
                playerPoints = caclculate_score(playerPoints, buffs)
                exp_pos = brick.rect.center
                self.explosions.append(Explosion(exp_pos))
        return playerPoints