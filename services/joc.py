from database.database import get_connection
from models.questionari import Questionari
from models.pregunta import PreguntaMultiple, PreguntaVF
from services.autenticacio import buscar_usuari_per_nom

def obtenir_questionaris():
    connexio = get_connection()
    cursor = connexio.cursor()
    cursor.execute("SELECT * FROM questionaris ORDER BY id_questionari")
    files = cursor.fetchall()
    connexio.close()
    return files

def mostrar_questionaris():
    questionaris = obtenir_questionaris()
    if len(questionaris) == 0:
        print("Encara no hi ha qüestionaris guardats.")
        return

    print("\nQüestionaris disponibles")
    for q in questionaris:
        print(f"{q[0]}. {q[2]} - {q[3]} - dificultat {q[4]}")

def carregar_questionari(id_questionari):
    connexio = get_connection()
    cursor = connexio.cursor()
    cursor.execute("SELECT * FROM questionaris WHERE id_questionari = %s", (id_questionari,))
    fila_q = cursor.fetchone()

    if fila_q is None:
        connexio.close()
        return None

    questionari = Questionari(
        fila_q[0], # id_questionari
        fila_q[1], # id_propietari
        fila_q[2], # titol
        fila_q[3], # categoria
        fila_q[4], # dificultat
        fila_q[5]  # descripcio
    )

    cursor.execute("SELECT * FROM preguntes WHERE id_questionari = %s ORDER BY id_pregunta", (id_questionari,))
    preguntes = cursor.fetchall()
    connexio.close()

    for p in preguntes:
        if p[2].lower() == "vf":
            pregunta = PreguntaVF(p[0], p[1], p[3], p[8], p[9])
        else:
            pregunta = PreguntaMultiple(p[0], p[1], p[3], p[4], p[5], p[6], p[7], p[8], p[9])
        questionari.afegir_pregunta(pregunta)

    return questionari

def demanar_questionari():
    mostrar_questionaris()
    try:
        id_questionari = int(input("Número de qüestionari: "))
    except ValueError:
        print("Has d'escriure un número.")
        return None

    questionari = carregar_questionari(id_questionari)
    if questionari is None:
        print("No s'ha trobat aquest qüestionari.")
    return questionari

def jugar_questionari(questionari, nom_jugador):
    punts = 0
    punts_totals = questionari.obtenir_punts_totals()
    print(f"\nTorn de {nom_jugador}")

    for pregunta in questionari.preguntes:
        pregunta.mostrar_pregunta()
        resposta = input("Resposta: ")
        if pregunta.validar_resposta(resposta):
            punts += pregunta.punts

    nota = 0
    if punts_totals > 0:
        nota = (punts / punts_totals) * 10

    print(f"Resultat de {nom_jugador}: {punts}/{punts_totals} punts. Nota: {nota:.2f}")
    return nota

def guardar_partida(id_questionari, tipus):
    connexio = get_connection()
    cursor = connexio.cursor()
    cursor.execute("INSERT INTO partides (id_questionari, tipus) VALUES (%s, %s)", (id_questionari, tipus))
    connexio.commit()
    id_partida = cursor.lastrowid
    connexio.close()
    return id_partida

def guardar_resultat(id_partida, id_usuari, puntuacio, resultat):
    connexio = get_connection()
    cursor = connexio.cursor()
    cursor.execute(
        "INSERT INTO resultats (id_partida, id_usuari, puntuacio, resultat) VALUES (%s, %s, %s, %s)",
        (id_partida, id_usuari, puntuacio, resultat)
    )
    connexio.commit()
    connexio.close()
    actualitzar_estadistiques_usuari(id_usuari)

def actualitzar_estadistiques_usuari(id_usuari):
    connexio = get_connection()
    cursor = connexio.cursor()
    cursor.execute("SELECT COUNT(*) FROM resultats WHERE id_usuari = %s", (id_usuari,))
    num_partides = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM resultats WHERE id_usuari = %s AND resultat = 'WIN'", (id_usuari,))
    victories = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM resultats WHERE id_usuari = %s AND resultat = 'LOSE'", (id_usuari,))
    derrotes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM resultats WHERE id_usuari = %s AND resultat = 'DRAW'", (id_usuari,))
    empats = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(puntuacio) FROM resultats WHERE id_usuari = %s", (id_usuari,))
    puntuacio_total = cursor.fetchone()[0] or 0
    cursor.execute(
        "UPDATE usuaris SET num_partides = %s, victories = %s, derrotes = %s, empats = %s, puntuacio_total = %s WHERE id_usuari = %s",
        (num_partides, victories, derrotes, empats, puntuacio_total, id_usuari)
    )
    connexio.commit()
    connexio.close()

def jugar_individual(usuari):
    questionari = demanar_questionari()
    if questionari is None:
        return

    id_partida = guardar_partida(questionari.id_questionari, "INDIVIDUAL")
    nota = jugar_questionari(questionari, usuari.nom_usuari)
    resultat = "WIN" if nota >= 5 else "LOSE"
    guardar_resultat(id_partida, usuari.id_usuari, nota, resultat)
    print("Partida individual guardada.")

def jugar_vs(usuari):
    questionari = demanar_questionari()
    if questionari is None:
        return

    nom_rival = input("Nom d'usuari del rival: ").strip()
    rival = buscar_usuari_per_nom(nom_rival)
    if rival is None:
        print("Aquest rival no existeix. Primer s'ha de registrar.")
        return

    id_partida = guardar_partida(questionari.id_questionari, "VS")
    nota_1 = jugar_questionari(questionari, usuari.nom_usuari)
    nota_2 = jugar_questionari(questionari, rival.nom_usuari)

    if nota_1 > nota_2:
        resultat_1 = "WIN"
        resultat_2 = "LOSE"
    elif nota_2 > nota_1:
        resultat_1 = "LOSE"
        resultat_2 = "WIN"
    else:
        resultat_1 = "DRAW"
        resultat_2 = "DRAW"

    guardar_resultat(id_partida, usuari.id_usuari, nota_1, resultat_1)
    guardar_resultat(id_partida, rival.id_usuari, nota_2, resultat_2)
    print("Partida 1 contra 1 guardada.")
