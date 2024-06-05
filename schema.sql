DROP TABLE IF EXISTS tb_marca;
DROP TABLE IF EXISTS tb_modelo;
DROP TABLE IF EXISTS tb_veiculo;

CREATE TABLE IF NOT EXISTS tb_marca (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

INSERT INTO tb_marca (nome)
VALUES
('Chevrolet'),
('Fiat'),
('Ford'),
('Honda'),
('Toyota'),
('Renault'),
('Volkswagen');

CREATE TABLE IF NOT EXISTS tb_modelo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    id_marca INTEGER NOT NULL
);

INSERT INTO tb_modelo (nome, id_marca)
VALUES
('Onix', 1),
('Cruze', 1),
('Argo', 2),
('Mobi', 2),
('Fusion', 3),
('Fiesta', 3),
('Civic', 4),
('Fit', 4),
('Etios', 5),
('Hilux', 5),
('Kwid', 6),
('Sandero', 6),
('Gol', 7),
('Polo', 7);

CREATE TABLE IF NOT EXISTS tb_veiculo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT NOT NULL UNIQUE,
    cor TEXT NOT NULL,
    ano INTEGER NOT NULL,
    status INTEGER NOT NULL,
    id_modelo INTEGER NOT NULL
);

INSERT INTO tb_veiculo (placa, cor, ano, status, id_modelo)
VALUES
('ABC-1234', 'Preto', 2011, 1, 1),
('DEF-5678', 'Vermelho', 2021, 2, 3),
('HIJ-1638', 'Cinza', 2001, 3, 5),
('KLM-5274', 'Vermelho', 2020, 2, 7);