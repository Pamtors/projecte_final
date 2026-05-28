import mysql.connector
from database.database import get_connection
from models.usuari import Usuari

def iniciar_sessio():
    """ Demana les credencials a l'usuari i comprova si existeix a la base de dades. Retorna un objecte Usuari si és correcte, o None si fallen les credencials."""
    print("\n--- Iniciar Sessió ---")
    nom_login = input("Nom d'usuari: ")
    pass_login = input("Contrasenya: ")

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True) 

        query = "SELECT * FROM usuaris WHERE nom_usuari = %s AND contrassenya = %s"
        cursor.execute(query, (nom_login, pass_login))
        row = cursor.fetchone()

        if row:
            print(f"\n¡Benvingut/da de nou, {row['nom']}!")
            usuari_autenticat = Usuari(
                id_usuari=row['id_usuari'],
                nom=row['nom'],
                nom_usuari=row['nom_usuari'],
                contrassenya=row['contrassenya'],
                email=row['email']
            )

            usuari_autenticat.num_partides = row['num_partides']
            usuari_autenticat.victories = row['victories']
            usuari_autenticat.derrotes = row['derrotes']
            usuari_autenticat.empats = row['empats']
            usuari_autenticat.puntuacio_total = float(row['puntuacio_total'])
            
            return usuari_autenticat
        
        else:
            print("\nCredencials incorrectes.")
            return None

    except mysql.connector.Error as err:
        print(f"Error de base de dades: {err}")
        return None
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def registrar_usuari():
    """ Demana totes les dades obligatòries per a la taula 'usuaris' de la BD, les valida lleugerament i realitza la inserció a MySQL."""
    print("\n--- Registre de Nou Usuari ---")
    nom = input("Introdueix el teu nom complet: ")
    nom_usuari = input("Introdueix el teu nom d'usuari: ")

    while True:
        contrassenya = input("Introdueix la contrassenya (mínim 8 caràcters): ")
        if len(contrassenya) >= 8:
            break
        print("La contrassenya ha de tenir com a mínim 8 caràcters.")

    email = input("Introdueix el teu email: ")

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """INSERT INTO usuaris (nom, nom_usuari, contrassenya, email) VALUES (%s, %s, %s, %s)"""
        valors = (nom, nom_usuari, contrassenya, email)
        
        cursor.execute(query, valors)
        conn.commit() 

        id_generat = cursor.lastrowid
        print(f"\n¡Usuari registrat correctament amb l'ID {id_generat}!")
        
        return Usuari(id_generat, nom, nom_usuari, contrassenya, email)

    except mysql.connector.IntegrityError as err:
        print(f"\nError de registre: El nom d'usuari o l'email ja estan en ús. ({err})")
        return None
    
    except mysql.connector.Error as err:
        print(f"\nError inesperat amb la base de dades: {err}")
        return None
    
    finally:
        if cursor: 
            cursor.close()
            
        if conn: 
            conn.close()