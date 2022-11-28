CREATE TABLE user_guesses (
    GUESS_ID varchar(255) NOT NULL,
    USER_ID uniqueidentifier NOT NULL PRIMARY KEY,
    DATE_OF_GUESS DATETIME,
    GUESS_STR int[]
);