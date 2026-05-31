import mysql.connector
from database.database import get_connection
from models.usuari import Usuari

def crear_usuari_des_de_fila(fila):
    return Usuari(
        fila[0], # id_usuari
        fila[1], # nom
        fila[2], # nom_usuari
        fila[3], # contrassenya
        fila[4], # email
        fila[5], # data_registre
        fila[6], # num_partides
        fila[7], # victories
        fila[8], # derrotes
        fila[9], # empats
        fila[10] # puntuacio_total
    )

def registrar_usuari():
    print("\nRegistre d'usuari")
    nom = input("Nom complet: ").strip()
    nom_usuari = input("Nom d'usuari: ").strip()
    contrassenya = input("Contrasenya: ").strip()
    email = input("Email: ").strip()

    if nom == "" or nom_usuari == "" or contrassenya == "" or email == "":
        print("Tots els camps són obligatoris.")
        return None

    if len(contrassenya) < 4:
        print("La contrasenya ha de tenir com a mínim 4 caràcters.")
        return None

    connexio = get_connection()
    try:
        cursor = connexio.cursor()
        cursor.execute(
            "INSERT INTO usuaris (nom, nom_usuari, contrassenya, email) VALUES (%s, %s, %s, %s)",
            (nom, nom_usuari, contrassenya, email)
        )
        connexio.commit()
        id_usuari = cursor.lastrowid
        print("Usuari registrat correctament.")
        return Usuari(id_usuari, nom, nom_usuari, contrassenya, email)
    except mysql.connector.Error:
        print("Aquest nom d'usuari o email ja existeix o hi ha un error amb la base de dades.")
        return None
    finally:
        connexio.close()

def iniciar_sessio():
    print("\nInici de sessió")
    nom_usuari = input("Nom d'usuari: ").strip()
    contrassenya = input("Contrasenya: ").strip()

    connexio = get_connection()
    cursor = connexio.cursor()
    cursor.execute(
        "SELECT * FROM usuaris WHERE nom_usuari = %s AND contrassenya = %s",
        (nom_usuari, contrassenya)
    )
    fila = cursor.fetchone()
    connexio.close()

    if fila is None:
        print("Credencials incorrectes.")
        return None

    usuari = crear_usuari_des_de_fila(fila)
    print(f"Benvingut/da, {usuari.nom}.")
    return usuari

def buscar_usuari_per_nom(nom_usuari):
    connexio = get_connection()
    cursor = connexio.cursor()
    cursor.execute("SELECT * FROM usuaris WHERE nom_usuari = %s", (nom_usuari,))
    fila = cursor.fetchone()
    connexio.close()

    if fila is None:
        return None
    return crear_usuari_des_de_fila(fila)
