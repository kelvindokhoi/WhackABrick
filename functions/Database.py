from peewee import * #type: ignore
import tkinter as tk
from tkinter import messagebox

class Database:
    def __init__(self,IsDatabaseUsed) -> None:
        self.IsDatabaseUsed = IsDatabaseUsed
        if self.IsDatabaseUsed == True:
            self.db = MySQLDatabase(
                'whackabrick',
                host='localhost',
                port=3306,
                user='root',
                password='root'
            )

            class BaseModel(Model):
                class Meta:
                    database = self.db

            class Scores(BaseModel):
                ScoreName = CharField()
                ScoreVal = IntegerField()
                MaxLevel = IntegerField(default=1)  # New field

            try:
                self.db.connect()
                # Check if table exists
                cursor = self.db.execute_sql("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = 'scores'
                """)
                if cursor.fetchone() is None:
                    # Create table if not exists
                    self.db.create_tables([Scores])
                else:
                    # Check if column exists
                    cursor = self.db.execute_sql("""
                        SELECT COLUMN_NAME 
                        FROM INFORMATION_SCHEMA.COLUMNS 
                        WHERE TABLE_NAME = 'scores' 
                        AND COLUMN_NAME = 'MaxLevel'
                    """)
                    if cursor.fetchone() is None:
                        # Add the column if it doesn't exist
                        self.db.execute_sql("ALTER TABLE scores ADD COLUMN MaxLevel INT DEFAULT 1")
            except Exception as e:
                print(e)
                root = tk.Tk()
                root.withdraw()
                root.wm_attributes('-topmost', True)
                messagebox.showwarning("Warning","No database connection or setup failed. Quitting now.")
                root.destroy()
                quit()

            self.db.close()

    def insert_data(self,name,score, max_level):  # Modified
        if self.db.is_closed():
            self.db.connect()
        if not isinstance(name, str) or not name.replace(" ", "").isalnum():
            raise ValueError("Name contains invalid characters.")
        if not isinstance(score, int):
            raise ValueError("Score must be an integer.")

        self.db.execute_sql(
            "INSERT INTO `scores` (`ScoreID`, `ScoreName`, `ScoreVal`, `MaxLevel`) VALUES (NULL, %s, %s, %s);",
            (name, score, max_level)
        )
        self.db.close()
    
    def read_top_3(self):  # Modified: Return max_levels too
        if self.db.is_closed():
            self.db.connect()
        scores = ["Bob 0 L1" for _ in range(3)]  # Format: Name Score Level
        scoreVals = [0 for _ in range(3)]
        max_levels = [1 for _ in range(3)]

        db_cursor = self.db.execute_sql("SELECT scorename, scoreval, MaxLevel FROM scores ORDER BY scoreval DESC LIMIT 3")

        i=0
        for row in db_cursor.fetchall():
            scores[i] = f"{row[0]}  {row[1]} L{row[2]}"  
            scoreVals[i] = row[1]
            max_levels[i] = row[2]
            i+=1

        self.db.close()
        return scores,scoreVals, max_levels