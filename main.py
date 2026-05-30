import database.database as db
from services.autenticacio import iniciar_sessio, registrar_usuari
from services.importacio_json import ImportadorJSON
from models.partida import Partida
from models.resultat import Resultat

def main():
    connexio = db.get_connection()
    questionaris_disponibles = []

    while True:
        print("\n  Introdueix una opció   ")
        print("1. Registre Usuari")
        print("2. Iniciar Sessió")
        print("3. Sortir")

        opcio = input("Opció: ")

        match opcio:
            case "1":
                registrar_usuari()

            case "2":
                usuari_actual = iniciar_sessio()
                if usuari_actual:
                    while True:
                        print(f"\n--- MENÚ USUARI ({usuari_actual.nom_usuari}) ---")
                        print("a. Importar fitxer JSON amb qüestionaris")
                        print("b. Veure qüestionaris disponibles")
                        print("c. Jugar Partida Individual")
                        print("d. Veure el meu perfil estadístic")
                        print("e. Tancar sessió")

                        opcio_usuari = input("Opció: ")

                        match opcio_usuari:
                            case "a":
                                ruta = input("Introdueix la ruta del fitxer JSON: ")
                                importador = ImportadorJSON(connexio)
                                nous_questionaris = importador.importar_questionaris(ruta, usuari_actual.id_usuari)
                                for questionari in nous_questionaris:
                                    questionaris_disponibles.append(questionari)

                            case "b":
                                print("\n--- QUESTIONARIS ---")
                                if len(questionaris_disponibles) == 0:
                                    print("No hi ha qüestionaris disponibles en memòria. Importa'n un primer.")
                                else:
                                    for idx, q in enumerate(questionaris_disponibles):
                                        print(f"{idx + 1}. {q.titol} ({q.categoria}) - Punts totals: {q.obtenir_punts_totals()}")

                            case "c":
                                if len(questionaris_disponibles) == 0:
                                    print("No hi ha qüestionaris disponibles per jugar.")
                                    continue
                                
                                for idx, q in enumerate(questionaris_disponibles):
                                    print(f"{idx + 1}. {q.titol}")
                                
                                try:
                                    sel = int(input("Selecciona el número de qüestionari: ")) - 1
                                    q_escollit = questionaris_disponibles[sel]
                                except (ValueError, IndexError):
                                    print("Selecció incorrecta.")
                                    continue

                                partida = Partida(id_questionari=q_escollit.id_questionari, tipus="INDIVIDUAL")
                                partida.guardar(connexio)

                                punts_obtinguts = 0
                                punts_totals = q_escollit.obtenir_punts_totals()

                                for pregunta in q_escollit.preguntes:
                                    pregunta.mostrar_pregunta()
                                    resposta = input("La teva resposta (número d'opció): ")
                                    if pregunta.validar_resposta(resposta):
                                        punts_obtinguts += pregunta.punts

                                nota_final = (punts_obtinguts / punts_totals) * 10 if punts_totals > 0 else 0.0
                                print(f"\nPartida acabada! Punts: {punts_obtinguts}/{punts_totals}. Nota final: {nota_final:.2f}/10")

                                estat_resultat = "WIN" if nota_final >= 5 else "LOSE"
                                if estat_resultat == "WIN":
                                    usuari_actual.afegir_victoria()
                                else:
                                    usuari_actual.afegir_derrota()
                                
                                usuari_actual.afegir_puntuacio(nota_final)

                                resultat = Resultat(partida.id_partida, usuari_actual.id_usuari, nota_final, estat_resultat)
                                resultat.guardar(connexio)

                                db.db_actualitzar_estadistiques_usuari(connexio, usuari_actual)

                            case "d":
                                print("\n--- EL MEU PERFIL ---")
                                print(usuari_actual)

                            case "e":
                                print("Tancant sessió...")
                                break
                            case _:
                                print("Opció no vàlida")

            case "3":
                print("Sortint de l'aplicació...")
                if connexio.is_connected():
                    connexio.close()
                break
            case _:
                print("Opció no vàlida")

if __name__ == "__main__":
    main()