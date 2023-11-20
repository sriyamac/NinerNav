DROP DATABASE IF EXISTS ninernav;
CREATE DATABASE ninernav;

USE ninernav;

CREATE TABLE User (
	id			MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
    username	VARCHAR(100) UNIQUE NOT NULL,
    email		VARCHAR(100) UNIQUE NOT NULL,
    password	CHAR(77) NOT NULL,		-- Argon2id default hash length
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
	id		    INT UNSIGNED NOT NULL,
	userid		MEDIUMINT UNSIGNED NOT NULL,
    mapid		SMALLINT UNSIGNED NOT NULL,
    score		SMALLINT NOT NULL,
    time		TIMESTAMP NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (userid) REFERENCES User(id),
    FOREIGN KEY (mapid) REFERENCES Map(id)
);