-- Abra o pgAdmin, crie um novo serivdor. Após, abra uma janela de scripts e
-- crie um novo database chamado `lgp`.
CREATE DATABASE lgp;
-- Agora abra uma nova janela de script e execute estes codigos abaixo
-- Obs.: Execute um comando de cada vez
CREATE SCHEMA assets;

-- Criando tabela de setores
CREATE TABLE assets.sectors(
	id SERIAL PRIMARY KEY,
	descripton VARCHAR(64)
);

-- Criando tabela de salas
CREATE TABLE assets.rooms (
	id SERIAL PRIMARY KEY,
	room_number vARCHAR(16),
	id_sector INTEGER,
	CONSTRAINT fk_sector FOREIGN KEY (id_sector) REFERENCES assets.sectors(id)
);

-- Criando tabela de xbess
CREATE TABLE assets.xbees(
	id SERIAL PRIMARY KEY,
	address_64_bit VARCHAR(16),
	sector INTEGER,
	CONSTRAINT fk_sector FOREIGN KEY (sector) REFERENCES assets.sectors(id)
);

-- Criando tabela de equipamentos
CREATE TABLE assets.equipments(
	id SERIAL PRIMARY KEY,
	description VARCHAR(255),
	serial_number VARCHAR(64),
	equipment_function VARCHAR(255),
	primarary_sector VARCHAR(64),
	xbee INTEGER,
	CONSTRAINT fk_xbee FOREIGN KEY (xbee) REFERENCES assets.xbees(id)
);

-- Codigo somente para debug
SELECT * FROM assets.equipments;
SELECT * FROM assets.sectors;
SELECT * FROM assets.xbees;
SELECT * FROM assets.rooms;
DELETE FROM assets.equipments;
DELETE FROM assets.xbees;

-- Alteracoes nas tabelas necessarias. Execute um de cada vez
ALTER TABLE assets.xbees DROP CONSTRAINT fk_sector;
ALTER TABLE assets.xbees ADD COLUMN ni VARCHAR(64);
ALTER TABLE assets.xbees ALTER COLUMN ni SET DEFAULT 'EMPTY';
ALTER TABLE assets.xbees RENAME COLUMN sector TO room;
ALTER TABLE assets.xbees ADD CONSTRAINT fk_room FOREIGN KEY (room) REFERENCES assets.rooms(id);
ALTER TABLE assets.xbees ADD COLUMN xbee_type VARCHAR(1) DEFAULT 'E';
ALTER TABLE assets.sectors RENAME COLUMN descripton TO description;
ALTER TABLE assets.equipments ADD UNIQUE (serial_number);
ALTER TABLE assets.equipments RENAME COLUMN primarary_sector TO primary_sector;

-- Inserindo valores nos setores
INSERT INTO assets.sectors (description) VALUES ('Enfermaria'),
('Pronto Socorro'), ('Lavanderia'), ('Bioengenharia'),
('Refeitorio'), ('Neurologia'), ('Mamografia')

-- Inserindo valores nas salas
INSERT INTO assets.rooms(room_number, id_sector) VALUES ('1A', 1), ('1B', 1),('1C', 1),('5A', 2),('9Z', 3),('8K', 4),('6F', 5),('2B', 5), ('3N', 6)

-- Inserindo valores de enderecos 64bit dos xbees e seu tipo
INSERT INTO assets.xbees(address_64_bit, xbee_type) VALUES ('0013A200404A4BB3', 'C'),
('0013A200404A4BC6', 'R'),('0013A200404AB737','R'),('0013A200407C48FE','E'),
('0013A200407C48FF','E'),('0013A200407C4533','E'), ('0013A200407C4927','E')

-- Codigo para debug
SELECT e.description, e.serial_number, x.address_64_bit FROM assets.equipments e
RIGHT JOIN assets.xbees x ON e.xbee = x.id
WHERE e.xbee IS NULL

-- Atualizacao nas informacoes das tabelas
UPDATE assets.xbees SET ni = 'C' WHERE id=1;
UPDATE assets.xbees SET ni = 'R1' WHERE id=2;
UPDATE assets.xbees SET ni = 'R2' WHERE id=3;
UPDATE assets.xbees SET ni = 'E1' WHERE id=4;
UPDATE assets.xbees SET ni = 'E2' WHERE id=5;
UPDATE assets.xbees SET ni = 'E3' WHERE id=6;
UPDATE assets.xbees SET ni = 'E4' WHERE id=7;
UPDATE assets.xbees SET ni = 'TESTE' WHERE id=22;

-- Alteracao na estrutura da tabela xbees
-- ALTER TABLE assets.xbees ADD COLUMN sector VARCHAR(64)
-- UPDATE assets.xbees SET sector = 1 WHERE ni = 'R2'
-- UPDATE assets.xbees SET sector = 4 WHERE ni = 'R1'
-- ALTER TABLE assets.xbees DROP COLUMN sector;
ALTER TABLE assets.xbees ADD COLUMN sector_id INT;
ALTER TABLE assets.xbees
ADD CONSTRAINT fk_sector FOREIGN KEY (sector_id) REFERENCES assets.sectors(id);
UPDATE assets.xbees SET sector_id = 1 WHERE id = 3;
UPDATE assets.xbees SET sector_id = 4 WHERE id = 2;
