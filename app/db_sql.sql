-- CREATING TABLES

CREATE SCHEMA assets;

CREATE TABLE assets.sectors(
	id SERIAL PRIMARY KEY,
	descripton VARCHAR(64)
);

CREATE TABLE assets.rooms (
	id SERIAL PRIMARY KEY,
	room_number VARCHAR(16),
	id_sector INTEGER,
	CONSTRAINT fk_sector FOREIGN KEY (id_sector) REFERENCES assets.sectors(id)
);

CREATE TABLE assets.xbees(
	id SERIAL PRIMARY KEY,
	address_64_bit VARCHAR(16),
	sector INTEGER,
	CONSTRAINT fk_sector FOREIGN KEY (sector) REFERENCES assets.sectors(id)
);

CREATE TABLE assets.equipments(
	id SERIAL PRIMARY KEY,
	description VARCHAR(255),
	serial_number VARCHAR(64),
	equipment_function VARCHAR(255),
	primarary_sector VARCHAR(64),
	xbee INTEGER,
	CONSTRAINT fk_xbee FOREIGN KEY (xbee) REFERENCES assets.xbees(id)
);



SELECT * FROM assets.equipments;
SELECT * FROM assets.sectors;
SELECT * FROM assets.xbees;
SELECT * FROM assets.rooms;

DELETE FROM assets.equipments;
DELETE FROM assets.xbees;
CREATE TABLE assets.rooms (
	id SERIAL PRIMARY KEY,
	room_number vARCHAR(16),
	id_sector INTEGER,
	CONSTRAINT fk_sector FOREIGN KEY (id_sector) REFERENCES assets.sectors(id)
);

ALTER TABLE assets.xbees DROP CONSTRAINT fk_sector;
ALTER TABLE assets.xbees ADD COLUMN ni VARCHAR(64);
ALTER TABLE assets.xbees ALTER COLUMN ni SET DEFAULT 'EMPTY';
ALTER TABLE assets.xbees ADD CONSTRAINT fk_room FOREIGN KEY (room) REFERENCES assets.rooms(id);
ALTER TABLE assets.xbees ADD COLUMN xbee_type VARCHAR(1) DEFAULT 'E';
ALTER TABLE assets.sectors RENAME COLUMN descripton TO description;

INSERT INTO assets.sectors (description) VALUES ('Enfermaria'),
('Pronto Socorro'), ('Lavanderia'), ('Bioengenharia'),
('Refeitorio'), ('Neurologia'), ('Mamografia')

INSERT INTO assets.rooms(room_number, id_sector) VALUES ('1A', 1), ('1B', 1),('1C', 1),('5A', 2),('9Z', 3),('8K', 4),('6F', 5),('2B', 5), ('3N', 6)

INSERT INTO assets.xbees(address_64_bit, xbee_type) VALUES ('0013A200404A4BB3', 'C'),
('0013A200404A4BC6', 'R'),('0013A200404AB737','R'),('0013A200407C48FE','E'),
('0013A200407C48FF','E'),('0013A200407C4533','E'), ('0013A200407C4927','E')
