CREATE TABLE IF NOT EXISTS usuaris (
    id_usuari INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    nom_usuari VARCHAR(50) UNIQUE NOT NULL,
    contrassenya VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_registre DATETIME DEFAULT CURRENT_TIMESTAMP,
    num_partides INT DEFAULT 0,
    victories INT DEFAULT 0,
    derrotes INT DEFAULT 0,
    empats INT DEFAULT 0,
    puntuacio_total DECIMAL(10,2) DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS questionaris (
    id_questionari INT AUTO_INCREMENT PRIMARY KEY,
    id_propietari INT,
    titol VARCHAR(255) NOT NULL,
    categoria VARCHAR(100),
    dificultat INT,
    descripcio TEXT,
    FOREIGN KEY (id_propietari) REFERENCES usuaris(id_usuari) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS preguntes (
    id_pregunta INT AUTO_INCREMENT PRIMARY KEY,
    id_questionari INT,
    tipus VARCHAR(20) NOT NULL,
    enunciat TEXT NOT NULL,
    resposta1 TEXT,
    resposta2 TEXT,
    resposta3 TEXT,
    resposta4 TEXT,
    resposta_correcta INT NOT NULL,
    punts INT DEFAULT 1,
    FOREIGN KEY (id_questionari) REFERENCES questionaris(id_questionari) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS partides (
    id_partida INT AUTO_INCREMENT PRIMARY KEY,
    id_questionari INT,
    tipus VARCHAR(20) NOT NULL,
    data_partida DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_questionari) REFERENCES questionaris(id_questionari) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS resultats (
    id_resultat INT AUTO_INCREMENT PRIMARY KEY,
    id_partida INT,
    id_usuari INT,
    puntuacio DECIMAL(5,2),
    resultat VARCHAR(10),
    FOREIGN KEY (id_partida) REFERENCES partides(id_partida) ON DELETE CASCADE,
    FOREIGN KEY (id_usuari) REFERENCES usuaris(id_usuari) ON DELETE CASCADE
);
