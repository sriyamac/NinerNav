DROP DATABASE IF EXISTS ninernav;
CREATE DATABASE ninernav;

USE ninernav;

CREATE TABLE user (
	id			MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
    username	VARCHAR(100) UNIQUE NOT NULL,
    email		VARCHAR(100) UNIQUE NOT NULL,
    password	CHAR(97) NOT NULL,		-- Argon2id default hash length
    PRIMARY KEY (ID)
);

CREATE TABLE map (
	id			SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name		VARCHAR(100) UNIQUE NOT NULL,
    latitude	DOUBLE NOT NULL,
    longitude	DOUBLE NOT NULL,
    imgpath		VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE score (
	id		    INT UNSIGNED NOT NULL AUTO_INCREMENT,
	userid		MEDIUMINT UNSIGNED NOT NULL,
    mapid		SMALLINT UNSIGNED NOT NULL,
    score		SMALLINT NOT NULL,
    time		TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (userid) REFERENCES user(id),
    FOREIGN KEY (mapid) REFERENCES map(id)
);

-- Generate some dummy data for the tables
INSERT INTO user (username, email, password)
VALUES
	('a', 'a@example.com', '$argon2id$v=19$m=65536,t=3,p=4$CKADhmoj5NhfVoe+wfbFvw$h6PX2TSy9/t1QZaQ1BIpffSX6NSuAmpLA9c9ShxOAqA'),
	('b', 'b@example.com', '$argon2id$v=19$m=65536,t=3,p=4$raLdPgfD+krGBUoXoSFaVA$r26NkGLYAjDI4Bc9TEN6Usqz3RJ3P9LheAgv+VpUtHc'),
    ('c', 'c@example.com', '$argon2id$v=19$m=65536,t=3,p=4$EuVxKIUDNsmY/ENHfiARzQ$TM8+SXlbdsL50wZ4hXcQzVwgguVq9GAXm0p7bQwHw2M');

INSERT INTO map (name, latitude, longitude, imgpath)
VALUES
    ("Image 0", 35.306330, -80.733399, "/static/gallery/scene_0.png"),
    ("Image 1", 35.305407, -80.731238, "/static/gallery/scene_1.png"),
    ("Image 2", 35.305578, -80.730922, "/static/gallery/scene_2.png"),
    ("Image 3", 35.306295, -80.729552, "/static/gallery/scene_3.png"),
    ("Image 4", 35.306756, -80.731305, "/static/gallery/scene_4.png"),
    ("Image 5", 35.30579736934577, -80.73230173858936, "/static/gallery/scene_5.png"),
    ("Image 6", 35.302603, -80.732805, "/static/gallery/scene_6.png"),
    ("Image 7", 35.301666, -80.735723, "/static/gallery/scene_7.png"),
    ("Image 8", 35.30286732802698,-80.73509417677259, "/static/gallery/scene_8.png"),
    ("Image 10", 35.305415, -80.729257, "/static/gallery/scene_10.png"),
    ("Image 11", 35.307246, -80.733724, "/static/gallery/scene_11.png"),
    ("Image 12", 35.307113, -80.734777, "/static/gallery/scene_12.png"),
    ("Image 13", 35.308008, -80.733728, "/static/gallery/scene_13.png"),
    ("Image 14", 35.30579213372453, -80.73231173069534, "/static/gallery/scene_14.png"),
    ("Image 15", 35.3067350, -80.7303750, "/static/gallery/scene_15.png"),
    ("Image 16", 35.3084017, -80.7291050, "/static/gallery/scene_16.png"),
    ("Image 17", 35.3082800, -80.7278133, "/static/gallery/scene_17.png");

INSERT INTO score (userid, mapid, score)
VALUES
	(1, 1, 1),
    (1, 2, 2),
    (2, 1, 3),
    (3, 2, 10);