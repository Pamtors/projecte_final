CREATE DATABASE IF NOT EXISTS sistema_cuestionarios;
USE sistema_cuestionarios;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    nom_usuario VARCHAR(50) NOT NULL UNIQUE,
    contrassenya VARCHAR(255) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    data_registre DATE NOT NULL DEFAULT (CURRENT_DATE),
    num_partides INT NOT NULL DEFAULT 0,
    victories INT NOT NULL DEFAULT 0,
    derrotes INT NOT NULL DEFAULT 0,
    empats INT NOT NULL DEFAULT 0,
    puntuacio_total DECIMAL(10,2) NOT NULL DEFAULT 0.00
);

-- TABLA: questionaris

CREATE TABLE questionaris (
    id_questionari INT AUTO_INCREMENT PRIMARY KEY,
    id_propietari INT NOT NULL,
    titol VARCHAR(200) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    dificultat INT NOT NULL,
    descripcio TEXT,

    -- Restricción de dificultad entre 1 y 5
    CONSTRAINT chk_dificultat
        CHECK (dificultat BETWEEN 1 AND 5),

    -- Clave foránea al propietario del cuestionario
    CONSTRAINT fk_questionari_usuari
        FOREIGN KEY (id_propietari)
        REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- TABLA: preguntes

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

    -- La respuesta correcta debe estar entre 1 y 4
    CONSTRAINT chk_resposta_correcta
        CHECK (resposta_correcta BETWEEN 1 AND 4),

    -- Puntuación positiva (normalmente 1 o 2)
    CONSTRAINT chk_punts
        CHECK (punts > 0),

    -- Clave foránea al cuestionario
    CONSTRAINT fk_pregunta_questionari
        FOREIGN KEY (id_questionari)
        REFERENCES questionaris(id_questionari)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =====================================================
-- ÍNDICES RECOMENDADOS
-- =====================================================
CREATE INDEX idx_questionaris_categoria
    ON questionaris(categoria);

CREATE INDEX idx_questionaris_dificultat
    ON questionaris(dificultat);

CREATE INDEX idx_preguntes_tipus
    ON preguntes(tipus);