-- CREATING TABLES

CREATE SCHEMA assets;

CREATE TABLE assets.sectors(
	id SERIAL PRIMARY KEY,
	descripton VARCHAR(64)
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
