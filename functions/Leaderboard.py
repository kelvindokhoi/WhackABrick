from functions.FilePaths import leaderboard_image_path
from functions.Resource_Reader import image_loader
from functions.Fonts import GameFonts
import tkinter as tk
from tkinter import simpledialog

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
    
    def ask_name(self,MyDB,score,earnedGold):
        # Create a custom Tkinter dialog for name input
        root = tk.Tk()
        root.withdraw()
        dialog = CustomDialog(root, score, earnedGold,title="Leaderboard Entry")
        user_response = dialog.result
        root.destroy()
        if user_response is not None and user_response != '':
            if len(user_response) <= 50:
                MyDB.insert_data(user_response, score)
        
    def show_player_score(self,playerPoints,MyDB,earnedGold):
        root = tk.Tk()
        root.withdraw()
        _,top3scores = MyDB.read_top_3()
        dialog = CustomDialogNL(root, playerPoints,earnedGold,min(top3scores)-playerPoints, title="Leaderboard Entry")
        root.destroy()

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, score, earnedGold,title=None):
        self.score = score
        self.earnedGold = earnedGold
        super().__init__(parent, title=title)

    def body(self, master):
        self.configure(bg="#1e3a5c")
        tk.Label(master, text=f"Your score is {self.score}!", font=("Segoe UI", [14*3,14][0], "bold"), fg="#ffffff", bg="#1e3a5c").grid(row=0, column=0, columnspan=2, pady=(10, 0))
        tk.Label(master, text=f"You earned {self.earnedGold} gold!", font=("Segoe UI", [14*3,14][0], "bold"), fg="#eafa0b", bg="#1e3a5c").grid(row=1, column=0, columnspan=2, pady=(0, 0))
        tk.Label(master, text=f"Congratulations!!!\nPlease enter your name to be on the leaderboard.", font=("Segoe UI", [33,11][0]), fg="#b3c6e7", bg="#1e3a5c").grid(row=2, column=0, columnspan=2, pady=(10, 10))
        tk.Label(master, text="(Limit: 50 characters)", font=("Segoe UI", [27,9][0]), fg="#7fa1d6", bg="#1e3a5c").grid(row=3, column=0, columnspan=2, pady=(0, 10))
        self.entry = tk.Entry(master, font=("Segoe UI", [36,12][0]), bg="#eaf1fb", fg="#1e3a5c", width=30, highlightbackground="#3b5998", highlightcolor="#3b5998", highlightthickness=1, relief="flat")
        self.entry.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 15))
        return self.entry

    def apply(self):
        self.result = self.entry.get()

class CustomDialogNL(simpledialog.Dialog):
    def __init__(self, parent, score, earnedGold, gap, title=None):
        self.score = score
        self.gap = gap
        self.earnedGold = earnedGold
        super().__init__(parent, title=title)

    def body(self, master):
        self.configure(bg="#1e3a5c")
        tk.Label(master, text=f"Your score is {self.score}!", font=("Segoe UI", [14*3,14][0], "bold"), fg="#ffffff", bg="#1e3a5c").grid(row=0, column=0, columnspan=2, pady=(10, 0))
        tk.Label(master, text=f"You earned {self.earnedGold} gold!", font=("Segoe UI", [14*3,14][0], "bold"), fg="#eafa0b", bg="#1e3a5c").grid(row=1, column=0, columnspan=2, pady=(0, 0))
        tk.Label(master, text=f"You need {self.gap} more point{'s' if self.gap != 1 else ''} to be on the leaderboard.", font=("Segoe UI", [33,11][0]), fg="#b3c6e7", bg="#1e3a5c").grid(row=2, column=0, columnspan=2, pady=(10, 10))
        tk.Label(master, text="Try again next time.", font=("Segoe UI", [27,9][0]), fg="#7fa1d6", bg="#1e3a5c").grid(row=3, column=0, columnspan=2, pady=(0, 10))
    
