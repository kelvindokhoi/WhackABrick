-- Drop the existing database if it exists
DROP DATABASE IF EXISTS whackabrick;

-- Create the new database
CREATE DATABASE whackabrick;

-- Use the new database
USE whackabrick;

-- Create the scores table with the required columns
CREATE TABLE scores (
    ScoreID INT AUTO_INCREMENT PRIMARY KEY,
    ScoreName VARCHAR(255) NOT NULL,
    ScoreVal INT NOT NULL,
    MaxLevel INT DEFAULT 1
);

-- Insert 3 default/null entries to populate the leaderboard
INSERT INTO scores (ScoreName, ScoreVal, MaxLevel) VALUES ('Bob', 3, 1);
INSERT INTO scores (ScoreName, ScoreVal, MaxLevel) VALUES ('Alice', 2, 1);
INSERT INTO scores (ScoreName, ScoreVal, MaxLevel) VALUES ('Charlie', 1, 1);