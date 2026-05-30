import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="onejar",
        port=3307,
        user="root",
        password="",
        database="sistema_cuestionaris",
        auth_plugin='mysql_native_password'
    )
    return conn

def db_guardar_partida(connexio, id_questionari, tipus, data_partida):
    cursor = None
    try:
        cursor = connexio.cursor()
        query = """
            INSERT INTO partides (id_questionari, tipus, data_partida) 
            VALUES (%s, %s, %s)
        """
        valors = (id_questionari, tipus, data_partida)
        cursor.execute(query, valors)
        connexio.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Error a db_guardar_partida: {err}")
        connexio.rollback()
        return None
    finally:
        if cursor:
            cursor.close()

def db_guardar_resultat(connexio, id_partida, id_usuari, puntuacio, resultat):
    cursor = None
    try:
        cursor = connexio.cursor()
        query = """
            INSERT INTO resultats (id_partida, id_usuari, puntuacio, resultat) 
            VALUES (%s, %s, %s, %s)
        """
        valors = (id_partida, id_usuari, puntuacio, resultat)
        cursor.execute(query, valors)
        connexio.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Error a db_guardar_resultat: {err}")
        connexio.rollback()
        return None
    finally:
        if cursor:
            cursor.close()

def db_actualitzar_estadistiques_usuari(connexio, usuari):
    cursor = None
    try:
        cursor = connexio.cursor()
        query = """
            UPDATE usuaris 
            SET num_partides = %s, victories = %s, derrotes = %s, empats = %s, puntuacio_total = %s 
            WHERE id_usuari = %s
        """
        valors = (usuari.num_partides, usuari.victories, usuari.derrotes, usuari.empats, usuari.puntuacio_total, usuari.id_usuari)
        cursor.execute(query, valors)
        connexio.commit()
    except mysql.connector.Error as err:
        print(f"Error a db_actualitzar_estadistiques_usuari: {err}")
        connexio.rollback()
    finally:
        if cursor:
            cursor.close()