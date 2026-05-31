from database.database import inicialitzar_base_dades
from services.autenticacio import registrar_usuari, iniciar_sessio
from services.importacio_json import ImportadorJSON
from services.joc import mostrar_questionaris, jugar_individual, jugar_vs, carregar_questionari
from services.estadistiques import mostrar_estadistiques_usuari, mostrar_ranking_global, mostrar_classificatoria


def pausar():
    input("\nPrem Enter per continuar...")


def mostrar_info_questionari():
    mostrar_questionaris()
    try:
        id_questionari = int(input("Número de qüestionari: "))
    except ValueError:
        print("Has d'escriure un número.")
        return

    questionari = carregar_questionari(id_questionari)
    if questionari is None:
        print("No s'ha trobat aquest qüestionari.")
        return

    print("\nInformació del qüestionari")
    print(questionari)


def menu_usuari(usuari):
    while True:
        print(f"\nMenú de {usuari.nom_usuari}")
        print("1. Importar qüestionaris des d'un JSON")
        print("2. Veure qüestionaris disponibles")
        print("3. Mostrar informació d'un qüestionari")
        print("4. Jugar partida individual")
        print("5. Jugar partida 1 contra 1")
        print("6. Veure les meves estadístiques")
        print("7. Veure ranking global")
        print("8. Veure classificatòria de resultats")
        print("9. Tancar sessió")

        opcio = input("Opció: ").strip()

        if opcio == "1":
            ruta = input("Ruta del JSON o Enter per usar data/quiz_test1.json: ").strip()
            if ruta == "":
                ruta = "data/quiz_test1.json"
            importador = ImportadorJSON()
            importador.importar_questionaris(ruta, usuari.id_usuari)
            pausar()
        elif opcio == "2":
            mostrar_questionaris()
            pausar()
        elif opcio == "3":
            mostrar_info_questionari()
            pausar()
        elif opcio == "4":
            jugar_individual(usuari)
            pausar()
        elif opcio == "5":
            jugar_vs(usuari)
            pausar()
        elif opcio == "6":
            mostrar_estadistiques_usuari(usuari)
            pausar()
        elif opcio == "7":
            mostrar_ranking_global()
            pausar()
        elif opcio == "8":
            mostrar_classificatoria()
            pausar()
        elif opcio == "9":
            print("Sessió tancada.")
            break
        else:
            print("Opció no vàlida.")


def main():
    inicialitzar_base_dades()

    while True:
        print("\nQuizzBattle")
        print("1. Registrar usuari")
        print("2. Iniciar sessió")
        print("3. Veure ranking global")
        print("4. Sortir")

        opcio = input("Opció: ").strip()

        if opcio == "1":
            usuari = registrar_usuari()
            if usuari is not None:
                menu_usuari(usuari)
        elif opcio == "2":
            usuari = iniciar_sessio()
            if usuari is not None:
                menu_usuari(usuari)
        elif opcio == "3":
            mostrar_ranking_global()
            pausar()
        elif opcio == "4":
            print("Fins aviat.")
            break
        else:
            print("Opció no vàlida.")


if __name__ == "__main__":
    main()
