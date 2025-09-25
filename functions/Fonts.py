import pygame
from pygame.font import Font
from functions.Colors import * #type:ignore

class GameFonts:
    def __init__(self) -> None:
        self.headerfont = Font('freesansbold.ttf', 48)

        self.buttonfont = pygame.font.SysFont('Corbel',32)
        self.buttonfont.set_bold(True)

        self.pointsfont = pygame.font.SysFont('Corbel', 69)
        self.pointsfont.set_bold(True)

        self.remaintimefont = pygame.font.SysFont('Corbel',53)
    
    def blit_player_point(self,playerPoints,screen):
        pointsText = self.pointsfont.render(f"Points: {playerPoints}", True, darkblue)
        screen.blit(pointsText, (90, 10))
    
    def blit_shop_text(self,screen):
        shopText = self.headerfont.render("Shop Coming Soon!", True, black, pink)
        shopRect = shopText.get_rect()
        shopRect.center = (350, 300)
        screen.blit(shopText, shopRect)

