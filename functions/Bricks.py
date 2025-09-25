from enum import Enum
from functions.Resource_Reader import image_loader
from functions.FilePaths import * #type:ignore
from functions.GameState import GameState
from functions.Music import Music
from functions.CalculateScore import caclculate_score
from pygame.sprite import * #type:ignore
from pygame.locals import * #type:ignore
import random


if pygame.get_init()==False:
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,pygame.NOFRAME)
    infoObject = pygame.display.Info()
    desktop_width = infoObject.current_w
    desktop_height = infoObject.current_h
    pygame.display.set_caption("Whack A' Brick!")

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

        self.brickPossibleConfig = [brickState.CHARACTER_A,brickState.CHARACTER_B,brickState.CHARACTER_C,brickState.CHARACTER_D,brickState.CHARACTER_E]
        self.brick_alive = [(state,image_loader(brick_img,(90,90))) for state,brick_img in zip(self.brickPossibleConfig,brick_paths)]
        self.aliveodds = 5
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
    
    def debug_mode_brick(self,screen):
        for i in range(5):
            for j in range(5):
                pygame.draw.rect(screen, (0,0,255), self.bricks[i][j].rect, 2)
    
    def blit_brick(self,screen):
        for brick in self.allbricks:
            if brick.status in self.brickPossibleConfig or brick.status == brickState.DEAD:
                screen.blit(brick.image, brick.rect)
    
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
        return playerPoints