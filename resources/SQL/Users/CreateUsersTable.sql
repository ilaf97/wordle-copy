CREATE TABLE users (
    USER_ID uniqueidentifier NOT NULL PRIMARY KEY default NEWID(),
    EMAIL varchar(255),
    JOIN_DATE DATETIME
);