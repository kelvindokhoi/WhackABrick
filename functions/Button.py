import pygame
from functions.Resource_Reader import image_loader

class Button:
    def __init__(self,image_path,hover_image_path,alpha,dimension_normal,dimension_hover,topleft):
        self.image = image_loader(image_path,dimension_normal,alpha)
        self.hover_image = image_loader(hover_image_path,dimension_hover,alpha)
        self.current_image = self.image
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        self.normal_topleft = topleft
        self.hover_topleft = (topleft[0]+3,topleft[1]+3)
    
    def blit_button(self,screen):
        screen.blit(self.current_image,self.rect)
    
    def if_hover(self,cursor_Rect):
        if self.rect.colliderect(cursor_Rect):
            self.current_image = self.hover_image
            self.rect.topleft = self.hover_topleft
            return True
        else:
            self.current_image = self.image
            self.rect.topleft = self.normal_topleft
            return False
    
    def debug_mode(self,screen,debug_mode):
        if debug_mode:
            pygame.draw.rect(screen, (0,0,255), self.rect, 2)