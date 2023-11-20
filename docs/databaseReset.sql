DROP DATABASE IF EXISTS ninernav;
CREATE DATABASE ninernav;

USE ninernav;

CREATE TABLE User (
	id			MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
    username	VARCHAR(100) UNIQUE NOT NULL,
    email		VARCHAR(100) UNIQUE NOT NULL,
    password	CHAR(97) NOT NULL,		-- Argon2id default hash length
    PRIMARY KEY (ID)
);

CREATE TABLE Map (
	id			SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name		VARCHAR(100) UNIQUE NOT NULL,
    latitude	DOUBLE NOT NULL,
    longitude	DOUBLE NOT NULL,
    imgpath		VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE Score (
	id		    INT UNSIGNED NOT NULL AUTO_INCREMENT,
	userid		MEDIUMINT UNSIGNED NOT NULL,
    mapid		SMALLINT UNSIGNED NOT NULL,
    score		SMALLINT NOT NULL,
    time		TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (userid) REFERENCES User(id),
    FOREIGN KEY (mapid) REFERENCES Map(id)
);

-- Generate some dummy data for the tables
INSERT INTO User (username, email, password)
VALUES
	('a', 'a@example.com', '$argon2id$v=19$m=65536,t=3,p=4$CKADhmoj5NhfVoe+wfbFvw$h6PX2TSy9/t1QZaQ1BIpffSX6NSuAmpLA9c9ShxOAqA'),
	('b', 'b@example.com', '$argon2id$v=19$m=65536,t=3,p=4$raLdPgfD+krGBUoXoSFaVA$r26NkGLYAjDI4Bc9TEN6Usqz3RJ3P9LheAgv+VpUtHc'),
    ('c', 'c@example.com', '$argon2id$v=19$m=65536,t=3,p=4$EuVxKIUDNsmY/ENHfiARzQ$TM8+SXlbdsL50wZ4hXcQzVwgguVq9GAXm0p7bQwHw2M');

INSERT INTO Map (name, longitude, latitude, imgpath)
VALUES
	('Null Island', 0, 0, '/dev/null'),
    ('Full Island', 1, 1, '/dev/full'),
    ('Random Island', 0.4019647391215304, 0.830638956196776, '/dev/urandom');

INSERT INTO Score (userid, mapid, score)
VALUES
	(0, 0, 1),
    (0, 1, 2),
    (1, 0, 3),
    (2, 1, 10);