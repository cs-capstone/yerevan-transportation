CREATE TYPE transport_type AS ENUM ('bus', 'microbus', 'metro');

CREATE TABLE transport (
	  id 	SERIAL PRIMARY KEY,
 	  name VARCHAR(10) NOT NULL,
	  type transport_type NOT NULL
);

INSERT INTO transport(name, type) VALUES ('2', 'microbus'), ('50', 'microbus'), ('71', 'microbus'), ('259', 'bus');

CREATE TABLE street (
	id 	SERIAL PRIMARY KEY,
 	name VARCHAR(50) NOT NULL
);

INSERT INTO street (name) VALUES ( 1, 'baghramnyan' ), ( 2, 'komitas' ), ( 3, 'abovyan' ), ( 4, 'azatutyun highway' );

CREATE TABLE station (id SERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL, street_id INTEGER references street(id));

CREATE TABLE connected_stations(id SERIAL PRIMARY KEY, first_station_id INTEGER references station(id) not null, second_station_id INTEGER references station(id) not null);

INSERT INTO station(name, street_id) VALUES
('Opera Mashtots str. stop', 1), ('Chekhov school stop', 1), ('AUA stop', 1),
('Kamo School stop', 1), ('Metro barekamutyun stop', 1),('ARAY stop', 4), ('Babayan str stop', 4),
('Azatuyan zbosaygi stop', 4), ('Abovyan park stop', 3),('Agrarian University stop', 3),
('Metro Eritasardakan stop', 3), ('Ameria-HSBC banks stop', 2),('Vagharshyan stop', 2),
('Papazyan str stop', 2),('Vratsakan str stop', 2),('SAS supermarket stop', 2), ('Tigranyan str. stop', 2),('Yerevan City stop', 2);

CREATE TABLE transport_station (id SERIAL PRIMARY KEY, transport_id INTEGER references transport(id) not null, station_id INTEGER references station(id) not null);

INSERT INTO transport_station(transport_id, station_id) VALUES (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 12), (1, 13),
(1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 12), (4, 13), (4, 14), (4, 15),
(4, 16), (4, 17), (4, 18), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 6), (2, 6),  (2, 12), (2, 13), (2, 14),
(2, 15), (2, 16), (2, 17), (2, 18), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17), (3, 18), (3, 6), (3, 7), (3, 8);

INSERT INTO connected_stations (first_station_id, second_station_id) VALUES (1, 2),  (2, 3), (3, 4), (4, 5), (6, 7),
(7, 8), (8, 9), (9, 10), (10, 11),  (5, 12), (12, 13),(13, 14),(14, 15), (15, 16), (16, 17), (17, 18),(18, 6);

INSERT INTO street values (5, 'Mamikonyanc Street');
INSERT INTO station (name, street_id) values ('Babloyan Hospital stop', 5);
INSERT INTO transport (name, type) values ('24', 'bus');
INSERT INTO connected_stations (first_station_id, second_station_id) VALUES (18, 19);

INSERT INTO transport_station(transport_id, station_id) VALUES (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 12), (5, 13),
(5, 14), (5, 15),(5, 16), (5, 17),(5, 18), (5, 20);

INSERT INTO connected_stations (first_station_id, second_station_id) VALUES (2, 1),  (3, 2), (4, 3), (5, 4), (7, 6),
(8, 7), (9, 8), (10, 9), (11, 10),  (12, 5), (13, 12),(14, 13),(15, 14), (16, 15), (17, 16), (18, 17),(6, 18),(19, 18);

ALTER TABLE station ADD COLUMN lng NUMERIC;
ALTER TABLE station ADD COLUMN lat NUMERIC;


UPDATE station set lng = 40.2061645, lat = 44.5228028 WHERE id = 18;
UPDATE station set lng = 40.208995, lat = 44.522736 WHERE id = 19;
UPDATE station set lng = 40.2063898, lat = 44.5188224 WHERE id = 17;
UPDATE station set lng = 40.2065988, lat = 44.5148903 WHERE id = 16;
UPDATE station set lng = 40.2068425, lat = 44.5109046 WHERE id = 15;
UPDATE station set lng = 40.2042143, lat = 44.5017609 WHERE id = 14;
UPDATE station set lng = 40.2027721, lat = 44.4982097 WHERE id = 13;
UPDATE station set lng = 40.2018462, lat = 44.4959539 WHERE id = 12;
UPDATE station set lng = 40.1909672, lat = 44.5276710 WHERE id = 9;
UPDATE station set lng = 40.1899017, lat = 44.5258766 WHERE id = 10;
UPDATE station set lng = 40.187208, lat = 44.522804 WHERE id = 11;
UPDATE station set lng = 40.1962184, lat = 44.5167115 WHERE id = 8;
UPDATE station set lng = 40.1995414, lat = 44.5203245 WHERE id = 7;
UPDATE station set lng = 40.2026820, lat = 44.5229477 WHERE id = 6;
UPDATE station set lng = 40.1958681, lat = 44.4942695 WHERE id = 5;
UPDATE station set lng = 40.1928409, lat = 44.4994301 WHERE id = 4;
UPDATE station set lng = 40.192033, lat = 44.505081 WHERE id = 3;
UPDATE station set lng = 40.191091, lat = 44.511320 WHERE id = 2;
UPDATE station set lng = 40.187830, lat = 44.514659 WHERE id = 1;


ALTER TABLE station RENAME COLUMN lng TO lat_tmp;
ALTER TABLE station RENAME COLUMN lat TO lng;
ALTER TABLE station RENAME COLUMN lat_tmp TO lat;


INSERT INTO street VALUES ( 6, 'Mashtots Avenue' );

INSERT INTO station(name, street_id, lat, lng) VALUES
('Komitas Park stop', 6, 40.187716, 44.516096),
('Shahumyan School stop', 6, 40.184752, 44.512452),
('Amiryan Mashtots stop', 6, 40.181300, 44.508360),
('Pak Shuka stop', 6, 40.178471, 44.505086);

INSERT INTO connected_stations (first_station_id, second_station_id) VALUES (20, 21), (21, 20), (21, 22), (22, 21),
(22, 23), (23, 22), (1, 21), (21, 1), (1, 20), (20, 1);

INSERT INTO street VALUES ( 7, 'Koryun Street' );

INSERT INTO station(name, street_id, lat, lng) VALUES ('Citadel stop', 7, 40.189794, 44.521030);

INSERT INTO connected_stations (first_station_id, second_station_id) VALUES (24, 20), (20, 24), (24, 10), (10, 24),
(24, 11), (11, 24);

INSERT INTO street VALUES ( 8, 'Teryan Street' );

INSERT INTO station(name, street_id, lat, lng) VALUES ('Citadel stop', 7, 40.189794, 44.521030);

UPDATE connected_stations set distance = 870 where first_station_id = 18 AND second_station_id = 19;
UPDATE connected_stations set distance = 870 where first_station_id = 19 AND second_station_id = 18;

UPDATE connected_stations set distance = 350 where first_station_id = 16 AND second_station_id = 17;
UPDATE connected_stations set distance = 350 where first_station_id = 17 AND second_station_id = 16;

UPDATE connected_stations set distance = 800 where first_station_id = 15 AND second_station_id = 14;
UPDATE connected_stations set distance = 800 where first_station_id = 14 AND second_station_id = 15;

UPDATE connected_stations set distance = 350 where first_station_id = 14 AND second_station_id = 13;
UPDATE connected_stations set distance = 350 where first_station_id = 13 AND second_station_id = 14;

UPDATE connected_stations set distance = 300 where first_station_id = 12 AND second_station_id = 13;
UPDATE connected_stations set distance = 300 where first_station_id = 13 AND second_station_id = 12;

UPDATE connected_stations set distance = 900 where first_station_id = 12 AND second_station_id = 5;
UPDATE connected_stations set distance = 900 where first_station_id = 5 AND second_station_id = 12;

UPDATE connected_stations set distance = 550 where first_station_id = 4 AND second_station_id = 5;
UPDATE connected_stations set distance = 550 where first_station_id = 5 AND second_station_id = 4;

UPDATE connected_stations set distance = 500 where first_station_id = 4 AND second_station_id = 3;
UPDATE connected_stations set distance = 500 where first_station_id = 3 AND second_station_id = 4;

UPDATE connected_stations set distance = 500 where first_station_id = 2 AND second_station_id = 3;
UPDATE connected_stations set distance = 500 where first_station_id = 3 AND second_station_id = 2;

UPDATE connected_stations set distance = 450 where first_station_id = 2 AND second_station_id = 1;
UPDATE connected_stations set distance = 450 where first_station_id = 1 AND second_station_id = 2;

UPDATE connected_stations set distance = 400 where first_station_id = 23 AND second_station_id = 22;
UPDATE connected_stations set distance = 400 where first_station_id = 22 AND second_station_id = 23;

UPDATE connected_stations set distance = 600 where first_station_id = 20 AND second_station_id = 24;
UPDATE connected_stations set distance = 600 where first_station_id = 24 AND second_station_id = 20;

UPDATE connected_stations set distance = 500 where first_station_id = 24 AND second_station_id = 10;
UPDATE connected_stations set distance = 500 where first_station_id = 10 AND second_station_id = 24;

UPDATE connected_stations set distance = 450 where first_station_id = 24 AND second_station_id = 11;
UPDATE connected_stations set distance = 450 where first_station_id = 11 AND second_station_id = 24;

UPDATE connected_stations set distance = 190 where first_station_id = 9 AND second_station_id = 10;
UPDATE connected_stations set distance = 190 where first_station_id = 10 AND second_station_id = 9;

UPDATE connected_stations set distance = 400 where first_station_id = 11 AND second_station_id = 10;
UPDATE connected_stations set distance = 400 where first_station_id = 10 AND second_station_id = 11;

UPDATE connected_stations set distance = 2800 where first_station_id = 9 AND second_station_id = 8;
UPDATE connected_stations set distance = 2800 where first_station_id = 8 AND second_station_id = 9;

UPDATE connected_stations set distance = 550 where first_station_id = 7 AND second_station_id = 8;
UPDATE connected_stations set distance = 550 where first_station_id = 8 AND second_station_id = 7;

UPDATE connected_stations set distance = 350 where first_station_id = 7 AND second_station_id = 6;
UPDATE connected_stations set distance = 350 where first_station_id = 6 AND second_station_id = 7;

UPDATE connected_stations set distance = 700 where first_station_id = 18 AND second_station_id = 6;
UPDATE connected_stations set distance = 700 where first_station_id = 6 AND second_station_id = 18;

UPDATE connected_stations set distance = 450 where first_station_id = 20 AND second_station_id = 21;
UPDATE connected_stations set distance = 450 where first_station_id = 21 AND second_station_id = 20;

INSERT INTO station(name, street_id, lat, lng) VALUES
 ('Architecture and Construction University stop', 8, 40.1909518, 44.5239803);

INSERT INTO connected_stations (first_station_id, second_station_id, distance) VALUES (24, 25, 300), (25, 24, 300);

INSERT INTO street (id, name) values (9, 'Amiryan Street')

INSERT INTO station(name, street_id, lat, lng) VALUES
 ('Amiryan SAS supermarket stop', 9, 40.1802791, 44.5084691),
 ('Amiryan Republic Square stop', 9, 40.178352, 44.511262);

INSERT INTO connected_stations (first_station_id, second_station_id, distance) VALUES (26, 27, 300), (27, 26, 300),
(26, 22, 160), (22, 26, 160), (26, 23, 450), (23, 26, 450);

INSERT INTO street (id, name) values (10, 'Kievyan Street')

INSERT INTO station(name, street_id, lat, lng) VALUES
 ('Kievyan Barekamutyun stop', 9, 40.1976751, 44.4924992),
 ('Kievyan Orbeli stop', 9, 40.194359, 44.486812),
 ('Kievyan HayPost stop', 9, 40.193201, 44.484911),
 ('Kievyan Hamalir stop', 9, 40.190014, 44.479477);

INSERT INTO connected_stations (first_station_id, second_station_id, distance) VALUES (28, 29, 600), (29, 28, 600),
(29, 30, 210), (30, 29, 210), (30, 31, 600), (31, 30, 600), (28, 12, 550), (12, 28, 550), (28, 5, 200), (5, 28, 200);

INSERT INTO street (id, name) values (11, 'Hrachya Qochar Street');

UPDATE station set street_id = 10 where name like 'Kievyan%' and street_id = 9;

INSERT INTO station(name, street_id, lat, lng) VALUES
 ('Qochar Barekamutyun stop', 11, 40.198119, 44.493800),
 ('Qochar Gyulbenkyan stop', 11, 40.199236, 44.496497),
 ('Qochar Vagharshyan stop', 11, 40.200734, 44.500051),
 ('Qochar Papazyan stop', 11, 40.202103, 44.503558);


INSERT INTO connected_stations (first_station_id, second_station_id, distance) VALUES (32, 33, 260), (33, 32, 260),
(33, 34, 350), (34, 33, 350), (35, 34, 350), (34, 35, 350), (32, 28, 120), (28, 32, 120), (32, 5, 150), (5, 32, 150),
(32, 28, 120), (28, 32, 120);

INSERT INTO connected_stations (first_station_id, second_station_id, distance) VALUES (17, 35, 1800), (35, 17, 1800)