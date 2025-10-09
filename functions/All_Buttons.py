import pygame,sys
from functions.Button import Button
from functions.FilePaths import shop_button_image_path,shop_button_hover_image_path
from functions.FilePaths import shop_back_button_image_path,shop_back_button_hover_image_path
from functions.FilePaths import quit_button_image_path,quit_button_hover_image_path
from functions.FilePaths import start_button_image_path,start_button_hover_image_path
from functions.FilePaths import settings_image_path,settings_hover_image_path
from functions.FilePaths import leaderboard_button_image_path
from functions.FilePaths import buy_image_path,buy_hover_image_path

class ShopButtonObject(Button):
    def __init__(self) -> None:
        super().__init__(shop_button_image_path,
                         shop_button_hover_image_path,
                         alpha=True,
                         dimension_normal=(150+10,62+5),
                         dimension_hover=(150,62),
                         topleft=(900,850))

class ShopBackButtonObject(Button):
    def __init__(self) -> None:
        super().__init__(shop_back_button_image_path,
                         shop_back_button_hover_image_path,
                         alpha=True,
                         dimension_normal=(150+10,62+5),
                         dimension_hover=(150,62),
                         topleft=(900,850))

class QuitButtonObject(Button):
    def __init__(self) -> None:
        super().__init__(quit_button_image_path,
                    quit_button_hover_image_path,
                    alpha=True,
                    dimension_normal=(150+15,62+10),
                    dimension_hover=(150+10,62+5),
                    topleft=(450,850))
    
    def if_clicked(self,cursor_Rect):
        if self.rect.colliderect(cursor_Rect):
            pygame.quit()
            sys.exit()

class StartButtonObject(Button):
    def __init__(self) -> None:
        super().__init__(start_button_image_path,
                         start_button_hover_image_path,
                         alpha=True,
                         dimension_normal=(150+10,62+5),
                         dimension_hover=(150,62),
                         topleft=(1350,850))

class StartBackButtonObject(Button):
    def __init__(self) -> None:
        super().__init__(shop_back_button_image_path,
                         shop_back_button_hover_image_path,
                         alpha=True,
                         dimension_normal=(150+10,62+5),
                         dimension_hover=(150,62),
                         topleft=(1350,850))

class SettingsButtonObject(Button):
    def __init__(self,desktop_width) -> None:
        super().__init__(settings_image_path,
                         settings_hover_image_path,
                         alpha=True,
                         dimension_normal=(100,100),
                         dimension_hover=(100,100),
                         topleft=(desktop_width-100,0))
        
    def if_hover(self,cursor_Rect):
        if self.rect.colliderect(cursor_Rect):
            self.current_image = self.hover_image
        else:
            self.current_image = self.image

class LeaderboardButtonObject(Button):
    def __init__(self) -> None:
        super().__init__(leaderboard_button_image_path,
                         leaderboard_button_image_path,
                         alpha=True,
                         dimension_normal=(300+10,130+5),
                         dimension_hover=(300,130),
                         topleft=(0,0))
        
# class MultiplierBuyButtonObject(Button):
#     def __init__(self) -> None:
#         super().__init__(leaderboard_button_image_path,
#                          leaderboard_button_image_path,
#                          alpha=True,
#                          dimension_normal=(300+10,130+5),
#                          dimension_hover=(300,130),
#                          topleft=(0,0))

class BuyButtonObject(Button):
    def __init__(self,dimension_normal,dimension_hover,topleft):
        super().__init__(buy_image_path, buy_hover_image_path, True, dimension_normal, dimension_hover, topleft)
        self.rect.center = topleft