CREATE DATABASE IF NOT EXISTS sistema_cuestionaris;
USE sistema_cuestionaris;

CREATE TABLE usuaris (
    id_usuari INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    nom_usuari VARCHAR(50) NOT NULL UNIQUE,
    contrassenya VARCHAR(255) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    data_registre DATE NOT NULL DEFAULT (CURRENT_DATE),
    num_partides INT NOT NULL DEFAULT 0,
    victories INT NOT NULL DEFAULT 0,
    derrotes INT NOT NULL DEFAULT 0,
    empats INT NOT NULL DEFAULT 0,
    puntuacio_total DECIMAL(10,2) NOT NULL DEFAULT 0.00
);

CREATE TABLE questionaris (
    id_questionari INT AUTO_INCREMENT PRIMARY KEY,
    id_propietari INT NOT NULL,
    titol VARCHAR(200) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    dificultat INT NOT NULL,
    descripcio TEXT,

    CONSTRAINT chk_dificultat
        CHECK (dificultat BETWEEN 1 AND 5),

    CONSTRAINT fk_questionari_usuari
        FOREIGN KEY (id_propietari)
        REFERENCES usuaris(id_usuari)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE preguntes (
    id_pregunta INT AUTO_INCREMENT PRIMARY KEY,
    id_questionari INT NOT NULL,
    tipus VARCHAR(50) NOT NULL,
    enunciat TEXT NOT NULL,

    resposta1 VARCHAR(255),
    resposta2 VARCHAR(255),
    resposta3 VARCHAR(255),
    resposta4 VARCHAR(255),

    resposta_correcta INT NOT NULL,
    punts INT NOT NULL DEFAULT 1,

    CONSTRAINT chk_resposta_correcta
        CHECK (resposta_correcta BETWEEN 1 AND 4),

    CONSTRAINT chk_punts
        CHECK (punts > 0),

    CONSTRAINT fk_pregunta_questionari
        FOREIGN KEY (id_questionari)
        REFERENCES questionaris(id_questionari)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE partides (
    id_partida INT AUTO_INCREMENT PRIMARY KEY,
    id_questionari INT NOT NULL,
    tipus ENUM('INDIVIDUAL', 'VS') NOT NULL,
    data_partida DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_partida_questionari
        FOREIGN KEY (id_questionari)
        REFERENCES questionaris(id_questionari)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE resultats (
    id_resultat INT AUTO_INCREMENT PRIMARY KEY,
    id_partida INT NOT NULL,
    id_usuari INT NOT NULL,
    puntuacio DECIMAL(5,2) NOT NULL,
    resultat ENUM('WIN', 'LOSE', 'DRAW') NOT NULL,

    CONSTRAINT fk_resultat_partida
        FOREIGN KEY (id_partida)
        REFERENCES partides(id_partida)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_resultat_usuari
        FOREIGN KEY (id_usuari)
        REFERENCES usuaris(id_usuari)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_questionaris_categoria
    ON questionaris(categoria);

CREATE INDEX idx_questionaris_dificultat
    ON questionaris(dificultat);

CREATE INDEX idx_preguntes_tipus
    ON preguntes(tipus);

CREATE INDEX idx_resultats_puntuacio
    ON resultats(puntuacio);

CREATE INDEX idx_usuaris_victories
    ON usuaris(victories);
