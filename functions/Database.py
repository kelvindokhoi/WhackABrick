from peewee import * #type: ignore
import tkinter as tk
from tkinter import messagebox

class Database:
    def __init__(self,IsDatabaseUsed) -> None:
        self.IsDatabaseUsed = IsDatabaseUsed
        if self.IsDatabaseUsed == True:

            #DATABASE TESTING
            #1. Define the database connection
            # Replace with your actual MySQL credentials
            self.db = MySQLDatabase(
                'whackabrick',
                host='localhost',
                port=3306,
                user='root',
                password='root'
            )

            #2. Define a base model for your database
            class BaseModel(Model):
                class Meta:
                    database = self.db

            #3. Define your model(s) that map to your database tables
            class Scores(BaseModel):
                #ScoreID = AutoField() # Peewee automatically handles primary keys
                ScoreName = CharField()
                ScoreVal = IntegerField()

            #4. Connect to the database
            try:
                self.db.connect()
            except Exception as e:
                print(e)
                root = tk.Tk()
                root.withdraw()  # Hide the main root window
                root.wm_attributes('-topmost', True)
                messagebox.showwarning("Warning","No database connection. Quitting now.")
                root.destroy()
                quit()

            #5. Read data from the database
            #Select high scores
            scores = [None for _ in range(3)]
            scoreVals = [None for _ in range(3)]

            db_cursor = self.db.execute_sql("select scores.scorename, scores.scoreval from scores order by scores.scoreval desc limit 3")

            i=0
            for row in db_cursor.fetchall():
                scores[i] = row[0] + "  " + str(row[1])  
                scoreVals[i] = row[1]
                i+=1

            self.db.close()

    def insert_data(self,name,score):
        self.db.connect()

        # Prevent SQL injection by allowing only alphanumeric names (and spaces)
        if not isinstance(name, str) or not name.replace(" ", "").isalnum():
            raise ValueError("Name contains invalid characters.")
        if not isinstance(score, int):
            raise ValueError("Score must be an integer.")

        self.db.execute_sql(
            "INSERT INTO `scores` (`ScoreID`, `ScoreName`, `ScoreVal`) VALUES (NULL, %s, %s);",
            (name, score)
        )
        self.db.close()
    
    def read_top_3(self):
        self.db.connect()
        scores = ["Bob 0" for _ in range(3)]
        scoreVals = [0 for _ in range(3)]

        db_cursor = self.db.execute_sql("select scores.scorename, scores.scoreval from scores order by scores.scoreval desc limit 3")

        i=0
        for row in db_cursor.fetchall():
            scores[i] = row[0] + "  " + str(row[1])  
            scoreVals[i] = row[1]
            # print(scores[i])
            i+=1

        self.db.close()
        return scores,scoreVals