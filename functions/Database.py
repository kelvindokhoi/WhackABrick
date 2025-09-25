from peewee import * #type: ignore

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
            self.db.connect()

            #5. Read data from the database
            #Select high scores
            scores = [None for _ in range(3)]
            scoreVals = [None for _ in range(3)]

            db_cursor = self.db.execute_sql("select scores.scorename, scores.scoreval from scores order by scores.scoreval desc limit 3")

            i=0
            for row in db_cursor.fetchall():
                #print(row[0],row[1])
                scores[i] = row[0] + "  " + str(row[1])  
                scoreVals[i] = row[1]
                print(scores[i])
                i+=1

            self.db.close()
            # for i in range(3):
            #     print(scores[i],scoreVals[i])