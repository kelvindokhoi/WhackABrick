import pygame

def initialize_display():
    pygame.init()
    screen = pygame.display.set_mode((0, 0),pygame.NOFRAME)
    infoObject = pygame.display.Info()
    desktop_width = infoObject.current_w
    desktop_height = infoObject.current_h
    pygame.display.set_caption("Whack A' Brick!")

    return screen,desktop_width,desktop_height