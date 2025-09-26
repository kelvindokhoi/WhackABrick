from functions.FilePaths import leaderboard_image_path
from functions.Resource_Reader import image_loader
from functions.Fonts import GameFonts
import tkinter as tk
from tkinter import simpledialog, messagebox

class LeaderboardObject:
    def __init__(self,desktop_width,desktop_height):
        self.background = image_loader(leaderboard_image_path,(1400,112*6),alpha=True)
        self.rect = self.background.get_rect()
        self.rect.center = (desktop_width//2,desktop_height//2)
    
    def blit_leaderboard(self,screen,scores,gameFont):
        screen.blit(self.background,self.rect)
        for i in range(3):
            message = scores[i]
            gameFont.blit_leaderboard_text(screen,message,i+1)
    
    def ask_name(self,MyDB,score):
        user_response = simpledialog.askstring("Input", f"Your score is {score}!\nPlease enter your name to be on the leaderboard.\nThe limit is 50 characters.")
        # root.destroy()
        if user_response is not None and user_response != '':
            if len(user_response) <= 50:
                MyDB.insert_data(user_response, score)

    
