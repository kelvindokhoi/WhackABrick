from functions.FilePaths import braxton_image_path
from functions.Resource_Reader import resource_path

import pygame
from pygame.locals import * #type:ignore
from pygame.sprite import * #type:ignore


class BraxtonObject:
    def __init__(self,desktop_height) -> None:
        braxton_x = 612//4
        braxton_y = 408//4
        self.braxton_image = pygame.transform.scale(pygame.image.load(resource_path(braxton_image_path)).convert_alpha(),(braxton_x,braxton_y))
        self.braxton_Rect = self.braxton_image.get_rect()
        self.braxton_Rect.topleft = (0, desktop_height-braxton_y)
    
    def blit_braxton(self,screen):
        screen.blit(self.braxton_image, self.braxton_Rect)
    
    def if_collide_braxton(self,cursor_Rect,music):
        if self.braxton_Rect.colliderect(cursor_Rect):
            music.play_braxton_sound()
