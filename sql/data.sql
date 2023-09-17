PRAGMA foreign_keys = ON;

-- Populate users table
INSERT INTO users(username, fullname, email, filename, password) VALUES
('awdeorio', 'Andrew DeOrio', 'awdeorio@umich.edu', 'e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg', 'password'),
('jflinn', 'Jason Flinn', 'jflinn@umich.edu', '505083b8b56c97429a728b68f31b0b2a089e5113.jpg', 'password'),
('michjc', 'Michael Cafarella', 'michjc@umich.edu', '5ecde7677b83304132cb2871516ea50032ff7a4f.jpg', 'password'),
('jag', 'H.V. Jagadish', 'jag@umich.edu', '73ab33bd357c3fd42292487b825880958c595655.jpg', 'password');

-- Populate posts table
INSERT INTO posts(postid, filename, owner) VALUES
(1, '122a7d27ca1d7420a1072f695d9290fad4501a41.jpg', 'awdeorio'),
(2, 'ad7790405c539894d25ab8dcf0b79eed3341e109.jpg', 'jflinn'),
(3, '9887e06812ef434d291e4936417d125cd594b38a.jpg', 'awdeorio'),
(4, '2ec7cf8ae158b3b1f40065abfb33e81143707842.jpg', 'jag');

-- Populate following table
INSERT INTO following(username1, username2) VALUES
('awdeorio', 'jflinn'),
('awdeorio', 'michjc'),
('awdeorio', 'jag'),
('jflinn', 'awdeorio'),
('jflinn', 'michjc'),
('michjc', 'awdeorio'),
('michjc', 'jag'),
('jag', 'michjc');

-- Populate comments table
INSERT INTO comments(commentid, owner, postid, text) VALUES
(1, 'awdeorio', 3, '#chickensofinstagram'),
(2, 'jflinn', 3, 'I <3 chickens'),
(3, 'michjc', 3, 'Cute overload!'),
(4, 'awdeorio', 2, 'Sick #crossword'),
(5, 'jflinn', 1, 'Walking the plank #chickensofinstagram'),
(6, 'awdeorio', 1, 'This was after trying to teach them to do a #crossword'),
(7, 'jag', 4, 'Saw this on the diag yesterday!');

-- Populate likes table
INSERT INTO likes(likeid, owner, postid) VALUES
(1, 'awdeorio', 1),
(2, 'michjc', 1),
(3, 'jflinn', 1),
(4, 'awdeorio', 2),
(5, 'michjc', 2),
(6, 'awdeorio', 3);