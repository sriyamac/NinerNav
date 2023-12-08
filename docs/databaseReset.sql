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
    description	VARCHAR(500) NOT NULL,
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

INSERT INTO map (name, latitude, longitude, imgpath, description)
VALUES
    ("Image 0", 35.306330, -80.733399, "/static/gallery/scene_0.png", "As you walk up, you can see all the way to the Union and if you look down there is a star design on the ground. This area was designed by engineers to produce the BEST echo. Don’t believe me? Make your way to star quad and whisper 'Go Niners' to experience it yourself!"),
    ("Image 1", 35.305407, -80.731238, "/static/gallery/scene_1.png", "A time capsule was installed at the plaza’s location and will be opened in 2046, UNC Charlotte’s centennial year."),
    ("Image 2", 35.305578, -80.730922, "/static/gallery/scene_2.png", "The UNC Charlotte Remembrance Memorial features a constellation garden that follows the orientation of the stars above the Kennedy Building on April 30, 2019, the day of the campus shooting."),
    ("Image 3", 35.306295, -80.729552, "/static/gallery/scene_3.png", "The sculpture was created by Jim Sanborn, the same artist who made the famous Kryptos sculpture at the CIA headquarters, which also has an unsolved code"),
    ("Image 4", 35.306756, -80.731305, "/static/gallery/scene_4.png", "The Smith building is one of the five buildings that make up the original quad of UNC Charlotte. Today, Smith is home to the College of Engineering’s Office of Student Development and Success and Department of Engineering Technology and Construction Management."),
    ("Image 5", 35.30579736934577, -80.73230173858936, "/static/gallery/scene_5.png", "Atkins Library, the third building to be constructed on the UNC Charlotte campus, is named for J. Murrey Atkins, the son of a prominent Gastonia family, successful Charlotte businessman and one of the University’s founding members."),
    ("Image 6", 35.302603, -80.732805, "/static/gallery/scene_6.png", "Levine Hall, named in honor of Sandra and Leon Levine, opened in 2016. Levine is home to both honors and non-honors students."),
    ("Image 7", 35.301666, -80.735723, "/static/gallery/scene_7.png", "A new five-story, 147,000 SF residence hall is under construction in South Village near SoVi dining hall. The residence hall features nearly 700 beds in traditional double rooms supported by shared bathrooms, study lounges, laundry rooms, and multi-purpose rooms."),
    ("Image 8", 35.30286732802698,-80.73509417677259, "/static/gallery/scene_8.png", "SoVi is based on a design concept similar to Crown Commons in which cooking areas are exposed so students can see the work that takes place behind the stove. SoVi also resembles Crown in that there are multiple food stations and there is an open dining layout."),
    ("Image 10", 35.305415, -80.729257, "/static/gallery/scene_10.png", "The Self-Made Man Statue is a 14-foot statue located in the plaza outside of Fretwell and Cato Hall. Bobbie Carlyle designed the statue with the vision of a man carving himself out of stone, carving his character and carving his future."),
    ("Image 11", 35.307246, -80.733724, "/static/gallery/scene_11.png", "Conceived as the Humanities Office Wing, Cato Hall originally housed Undergraduate Admissions and the Graduate School, along with the Development Office and the departments of Communication Studies and Social Work"),
    ("Image 12", 35.307113, -80.734777, "/static/gallery/scene_12.png", "The James H. and Martha H. Woodward Hall is a direct result of their vision to help elevate UNC Charlotte to a research institution. The Woodwards worked together to raise awareness of the University’s vital role as an economic engine and build many new partnerships and friendships for the institution."),
    ("Image 13", 35.308008, -80.733728, "/static/gallery/scene_13.png", "UNC Charlotte’s Popp Martin Student Union serves as the hub for student life and campus activities. The imposing building houses a wealth of opportunity for students including several dining options, Barnes and Noble at UNC Charlotte, Union Theater, the Campus Salon and the nerve center for student organizations; not to mention, Starbucks!"),
    ("Image 14", 35.30579213372453, -80.73231173069534, "/static/gallery/scene_14.png", "Originally opened in 2009, the UNC Charlotte Student Union is a community center for student affairs to thrive. It was renamed after prolific alumni Karen Popp (1980) and Demond Martin (1997) in 2016 to commemorate their dedication and extraordinary service to the university."),
    ("Image 15", 35.3067350, -80.7303750, "/static/gallery/scene_15.png", "Built to house the University’s earth and life sciences programs, the McEniry Building is named for UNC Charlotte’s first vice chancellor for academic affairs, William Hugh McEniry."),
    ("Image 16", 35.3084017, -80.7291050, "/static/gallery/scene_16.png", "The Botanical Gardens began in 1966 to serve as a living classroom and resource for the campus and greater Charlotte community. The co-founders were Bonnie Cone and Dr. Herbert Hechenbleikner."),
    ("Image 17", 35.3082800, -80.7278133, "/static/gallery/scene_17.png", "The Botanical Gardens began in 1966 to serve as a living classroom and resource for the campus and greater Charlotte community. The co-founders were Bonnie Cone and Dr. Herbert Hechenbleikner.");

INSERT INTO score (userid, mapid, score)
VALUES
	(1, 1, 1),
    (1, 2, 2),
    (2, 1, 3),
    (3, 2, 10);