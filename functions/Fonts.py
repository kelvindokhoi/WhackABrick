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
    
    def blit_level(self, screen, current_level, x_position):
        level_text = self.pointsfont.render(f"Level: {current_level}", True, darkblue)
        screen.blit(level_text, (x_position, 10))
    
    def blit_timer(self,screen,current_time):
        timer_text = self.timerfont.render(f"{current_time}",True,black)
        screen.blit(timer_text,(950,850))
    
    def blit_leaderboard_text(self,screen,text,position):
        coordinate = {1:(900,300),2:(900,500),3:(900,700)}[position]
        color = {1:red,2:orange,3:yellow}[position]
        leaderboard_message = self.leaderboard_text.render(text,True,color)
        screen.blit(leaderboard_message,coordinate)

    def blit_level_progress(self, screen, current_level, playerPoints, level_threshold, desktop_width):
        # Calculate progress
        points_in_current_level = playerPoints - ((current_level - 1) * level_threshold)
        points_needed = level_threshold
        progress = min(points_in_current_level / points_needed, 1.0)
        
        # Progress bar dimensions and position
        bar_width = 400
        bar_height = 60  # Changed from 40 to 60
        bar_x = (desktop_width - bar_width) // 2
        bar_y = 20
        
        # Draw background bar
        background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, white, background_rect, border_radius=10)
        pygame.draw.rect(screen, darkblue, background_rect, 3, border_radius=10)
        
        # Draw filled portion
        filled_width = int(bar_width * progress)
        if filled_width > 0:
            filled_rect = pygame.Rect(bar_x, bar_y, filled_width, bar_height)
            pygame.draw.rect(screen, lightblue, filled_rect, border_radius=10)
        
        # Draw numeric progress text
        progress_font = pygame.font.SysFont('Corbel', 28)
        progress_font.set_bold(True)  # Make text bold
        progress_text = progress_font.render(
            f"{points_in_current_level}/{points_needed} to Level {current_level + 1}", 
            True, 
            black
        )
        text_rect = progress_text.get_rect(center=(desktop_width // 2, bar_y + bar_height + 25))
        screen.blit(progress_text, text_rect)