PRAGMA foreign_keys = ON;

-- Populate users table
INSERT INTO users(username, fullname, email, filename, password, created) VALUES
('awdeorio', 'Andrew DeOrio', 'awdeorio@umich.edu', 'e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg', 'password', '2017-06-20 15:47:02'),
('jflinn', 'Jason Flinn', 'jflinn@umich.edu', '505083b8b56c97429a728b68f31b0b2a089e5113.jpg', 'password', '2017-06-20 15:47:02'),
('michjc', 'Michael Cafarella', 'michjc@umich.edu', '5ecde7677b83304132cb2871516ea50032ff7a4f.jpg', 'password', '2017-06-20 15:47:02'),
('jag', 'H.V. Jagadish', 'jag@umich.edu', '73ab33bd357c3fd42292487b825880958c595655.jpg', 'password', '2017-06-20 15:47:02');

-- Populate posts table
INSERT INTO posts(postid, filename, owner, created) VALUES
(1, '122a7d27ca1d7420a1072f695d9290fad4501a41.jpg', 'awdeorio', '2017-06-20 15:47:02'),
(2, 'ad7790405c539894d25ab8dcf0b79eed3341e109.jpg', 'jflinn', '2017-06-20 15:47:02'),
(3, '9887e06812ef434d291e4936417d125cd594b38a.jpg', 'awdeorio', '2017-06-20 15:47:02'),
(4, '2ec7cf8ae158b3b1f40065abfb33e81143707842.jpg', 'jag', '2017-06-20 15:47:02');

-- Populate following table
INSERT INTO following(username1, username2, created) VALUES
('awdeorio', 'jflinn', '2017-06-20 15:47:02'),
('awdeorio', 'michjc', '2017-06-20 15:47:02'),
('jflinn', 'awdeorio', '2017-06-20 15:47:02'),
('jflinn', 'michjc', '2017-06-20 15:47:02'),
('michjc', 'awdeorio', '2017-06-20 15:47:02'),
('michjc', 'jag', '2017-06-20 15:47:02'),
('jag', 'michjc', '2017-06-20 15:47:02');

-- Populate comments table
INSERT INTO comments(commentid, owner, postid, text, created) VALUES
(1, 'awdeorio', 3, '#chickensofinstagram', '2017-06-20 15:47:02'),
(2, 'jflinn', 3, 'I <3 chickens', '2017-06-20 15:47:02'),
(3, 'michjc', 3, 'Cute overload!', '2017-06-20 15:47:02'),
(4, 'awdeorio', 2, 'Sick #crossword', '2017-06-20 15:47:02'),
(5, 'jflinn', 1, 'Walking the plank #chickensofinstagram', '2017-06-20 15:47:02'),
(6, 'awdeorio', 1, 'This was after trying to teach them to do a #crossword', '2017-06-20 15:47:02'),
(7, 'jag', 4, 'Saw this on the diag yesterday!', '2017-06-20 15:47:02');

-- Populate likes table
INSERT INTO likes(likeid, owner, postid, created) VALUES
(1, 'awdeorio', 1, '2017-06-20 15:47:02'),
(2, 'michjc', 1, '2017-06-20 15:47:02'),
(3, 'jflinn', 1, '2017-06-20 15:47:02'),
(4, 'awdeorio', 2, '2017-06-20 15:47:02'),
(5, 'michjc', 2, '2017-06-20 15:47:02'),
(6, 'awdeorio', 3, '2017-06-20 15:47:02');
