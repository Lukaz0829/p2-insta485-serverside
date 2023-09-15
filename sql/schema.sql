PRAGMA foreign_keys = ON;

CREATE TABLE users(
    username VARCHAR(20) PRIMARY KEY,
    fullname VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    filename VARCHAR(64),
    password VARCHAR(256) NOT NULL,
    created TIMESTAMP
);

CREATE TABLE posts(
    postid INTEGER PRIMARY KEY AUTOINCREMENT,
    filename VARCHAR(64) NOT NULL,
    owner VARCHAR(20) NOT NULL,
    created TIMESTAMP
);

CREATE TABLE following(
    username1 VARCHAR(20) NOT NULL,
    username2 VARCHAR(20) NOT NULL,
    created TIMESTAMP,
    PRIMARY KEY(username1, username2)
);

CREATE TABLE comments(
    commentid INTEGER PRIMARY KEY AUTOINCREMENT,
    owner VARCHAR(20) NOT NULL,
    postid INTEGER NOT NULL,
    text VARCHAR(1024) NOT NULL,
    created TIMESTAMP
);

CREATE TABLE likes(
    likeid INTEGER PRIMARY KEY AUTOINCREMENT,
    owner VARCHAR(20) NOT NULL,
    postid INTEGER NOT NULL,
    created TIMESTAMP
);