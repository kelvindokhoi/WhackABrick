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

        self.timerfont = pygame.font.SysFont('Corbel',53)

        self.leaderboard_text = pygame.font.SysFont('Corbel',53)
        self.leaderboard_text.set_bold(True)
    
    def blit_player_point(self,playerPoints,screen):
        pointsText = self.pointsfont.render(f"Points: {playerPoints}", True, darkblue)
        screen.blit(pointsText, (90, 10))
    
    def blit_shop_text(self,screen):
        shopText = self.headerfont.render("Shop Coming Soon!", True, black, pink)
        shopRect = shopText.get_rect()
        shopRect.center = (950, 600)
        screen.blit(shopText, shopRect)
    
    def blit_timer(self,screen,current_time):
        timer_text = self.timerfont.render(f"{current_time}",True,black)
        screen.blit(timer_text,(950,850))
    
    def blit_leaderboard_text(self,screen,text,position):
        coordinate = {1:(900,300),2:(900,500),3:(900,700)}[position]
        color = {1:red,2:orange,3:yellow}[position]
        leaderboard_message = self.leaderboard_text.render(text,True,color)
        screen.blit(leaderboard_message,coordinate)
        

