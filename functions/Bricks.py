from enum import Enum
from functions.Resource_Reader import image_loader
from functions.FilePaths import * #type:ignore
from functions.GameState import GameState
from functions.Music import Music
from functions.CalculateScore import caclculate_score
from functions.Buffs import BUFF  # Add this line
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
    BOSS = 7  # New: Boss state
    DEAD = 6

class Brick(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = image_loader(brick_absent_image_path,(90,90))
        self.rect = Rect(x+70,y-10,90,90)
        self.status = brickState.ABSENT
        self.hits_needed = 1  # New: For bosses
        self.brickabsent = image_loader(brick_absent_image_path,(90,90))
        self.absent_image = self.brickabsent
        self.alive_image = self.brickabsent
        self.boss_image = image_loader(boss_brick_image_path, (90,90)) if 'boss_brick_image_path' in globals() else self.alive_image  # Assume path exists
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

class BonusGold(Sprite):  # New: Temporary bonus for chaining
    def __init__(self, pos):
        Sprite.__init__(self)
        self.image = image_loader(gold_icon_path, (20,20))  # Assume gold icon path
        self.rect = self.image.get_rect(center=pos)
        self.lifetime = 3000  # ms
        self.start_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.start_time > self.lifetime:
            self.kill()

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
        self.bonus_golds = Group()  # New: Group for bonus golds

        self.brickPossibleConfig = [brickState.CHARACTER_A,brickState.CHARACTER_B,brickState.CHARACTER_C,brickState.CHARACTER_D,brickState.CHARACTER_E]
        self.brick_alive = [(state,image_loader(brick_img,(90,90))) for state,brick_img in zip(self.brickPossibleConfig,brick_paths)]
        self.aliveodds = 10
        self.absentodds = 10

    def brick_draw(self,screen):
        self.allbricks.draw(screen)

    def random_brick(self,gameState, level):  # Modified: Accept level for difficulty
        if gameState==GameState.GAME_START:
            # Adjust odds based on level (harder as level increases)
            adjusted_aliveodds = max(1, self.aliveodds - (level - 1) * 2)  # Bricks appear more often
            adjusted_absentodds = max(5, self.absentodds - (level - 1))  # Less likely to disappear
            boss_chance = 0.1 if level >= 3 else 0  # Boss at level 3+
            
            for i in range(5):
                for j in range(5):
                    # if brick was absent, randomly makeit alive
                    if self.bricks[i][j].status not in self.brickPossibleConfig and self.bricks[i][j].fading == False:
                        r = random.randint(1,adjusted_aliveodds)
                        if r == 1:
                            if random.random() < boss_chance and level >= 3:
                                self.bricks[i][j].status = brickState.BOSS
                                self.bricks[i][j].image = self.bricks[i][j].boss_image
                                self.bricks[i][j].hits_needed = 3
                            else:
                                selected = random.choice(self.brick_alive)
                                self.bricks[i][j].status = selected[0]
                                self.bricks[i][j].image = selected[1]
                    # if alive, randomly make it absent
                    elif self.bricks[i][j].status not in [brickState.ABSENT,brickState.DEAD]:
                        r = random.randint(1, adjusted_absentodds)
                        if r == 1:
                            self.bricks[i][j].status = brickState.ABSENT
                            self.bricks[i][j].image = self.bricks[i][j].absent_image
        else:
            for i in range(5):
                for j in range(5):
                    self.bricks[i][j].status = brickState.ABSENT
                    self.bricks[i][j].image = self.bricks[i][j].absent_image

    def spawn_bonus_gold(self, pos):  # New: Chaining bonus
        bonus = BonusGold(pos)
        self.bonus_golds.add(bonus)

    def update_brick(self):
        for i in range(5):
            for j in range(5):
                self.bricks[i][j].update()
        for exp in self.explosions[:]:
            exp.update()
            if exp.done:
                self.explosions.remove(exp)
        self.bonus_golds.update()  # Update bonuses
    
    def debug_mode_brick(self,screen,debug_mode):
        if debug_mode:
            for i in range(5):
                for j in range(5):
                    pygame.draw.rect(screen, (0,0,255), self.bricks[i][j].rect, 2)
    
    def blit_brick(self,screen):
        for brick in self.allbricks:
            if brick.status in self.brickPossibleConfig or brick.status == brickState.DEAD or brick.status == brickState.BOSS:
                screen.blit(brick.image, brick.rect)
        for exp in self.explosions:
            screen.blit(exp.image, exp.rect)
        self.bonus_golds.draw(screen)  # Draw bonuses
    
    def play_brick_hit_sound(self,music):
        music.play_brick_hit_sound()
    
    def if_brick_collide(self, cursor_Rect, playerPoints, buffs, music, current_level, playerGold):
        for brick in self.allbricks:
            if (brick.status in self.brickPossibleConfig or brick.status == brickState.BOSS) and brick.rect.colliderect(cursor_Rect):
                brick.hits_needed -= 1
                if brick.status == brickState.BOSS:
                    if BUFF.BOSS_KILLER in buffs:  # Tie to buff
                        brick.hits_needed -= 1  # Extra damage
                self.play_brick_hit_sound(music)
                playerPoints = caclculate_score(playerPoints, buffs)
                if brick.hits_needed <= 0:  # Destroy on 0 hits
                    brick.status = brickState.DEAD
                    brick.fading = True
                    brick.fade_alpha = 255
                    brick.original_image = brick.image.copy()
                    exp_pos = brick.rect.center
                    self.explosions.append(Explosion(exp_pos))
                    # Chain bonus
                    if random.random() < (0.1 + (current_level - 1) * 0.05):
                        if BUFF.CHAIN_MASTER in buffs:
                            # Double chance or spawn two
                            self.spawn_bonus_gold(exp_pos)
                            self.spawn_bonus_gold((exp_pos[0] + 50, exp_pos[1] + 50))
                        else:
                            self.spawn_bonus_gold(exp_pos)
                # Bonus gold interaction (simple: add gold if hit)
                for bonus in self.bonus_golds:
                    if bonus.rect.colliderect(cursor_Rect):
                        playerGold += 10 * current_level
                        bonus.kill()
        return playerPoints, playerGold