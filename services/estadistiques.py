from database.database import get_connection

def mostrar_estadistiques_usuari(usuari):
    connexio = get_connection()
    cursor = connexio.cursor()
    cursor.execute("SELECT * FROM usuaris WHERE id_usuari = %s", (usuari.id_usuari,))
    fila = cursor.fetchone()
    connexio.close()

    if fila is None:
        print("No s'han trobat estadístiques.")
        return

    num_partides = fila[6]
    puntuacio_total = float(fila[10])
    mitjana = 0
    if num_partides > 0:
        mitjana = puntuacio_total / num_partides

    print("\nEstadístiques del perfil")
    print(f"Usuari: {fila[2]}")
    print(f"Partides: {num_partides}")
    print(f"Victòries: {fila[7]}")
    print(f"Derrotes: {fila[8]}")
    print(f"Empats: {fila[9]}")
    print(f"Puntuació total: {puntuacio_total:.2f}")
    print(f"Mitjana: {mitjana:.2f}")

def mostrar_ranking_global():
    connexio = get_connection()
    cursor = connexio.cursor()
    cursor.execute(
        "SELECT nom_usuari, num_partides, victories, empats, puntuacio_total FROM usuaris ORDER BY victories DESC, puntuacio_total DESC LIMIT 10"
    )
    files = cursor.fetchall()
    connexio.close()

    print("\nRanking global")
    if len(files) == 0:
        print("Encara no hi ha usuaris al ranking.")
        return

    posicio = 1
    for fila in files:
        print(f"{posicio}. {fila[0]} - victòries: {fila[2]} - punts: {float(fila[4]):.2f} - partides: {fila[1]}")
        posicio += 1

def mostrar_classificatoria():
    connexio = get_connection()
    cursor = connexio.cursor()
    cursor.execute(
        "SELECT u.nom_usuari, r.puntuacio, r.resultat, p.tipus, p.data_partida FROM resultats r JOIN usuaris u ON r.id_usuari = u.id_usuari JOIN partides p ON r.id_partida = p.id_partida ORDER BY r.puntuacio DESC, p.data_partida DESC LIMIT 20"
    )
    files = cursor.fetchall()
    connexio.close()

    print("\nClassificatòria de resultats")
    if len(files) == 0:
        print("Encara no hi ha resultats guardats.")
        return

    for fila in files:
        print(f"{fila[0]} - {float(fila[1]):.2f} - {fila[2]} - {fila[3]} - {fila[4]}")
