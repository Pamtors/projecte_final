import database.database as db
from models.usuari import Usuari
from services.importacio_json import ImportadorJSON

def crear_usuari(id_usuari):
    nom = input("Introdueix el teu nom: ")
    nom_usuari = input("Introdueix el teu nom d'usuari: ")

    while True:
        contrassenya = input("Introdueix la contrassenya (mínim 8 caràcters): ")
        if len(contrassenya) >= 8:
            break
        print("La contrassenya ha de tenir com a mínim 8 caràcters.")

    email = input("Introdueix el teu email: ")
    usuari = Usuari(id_usuari, nom, nom_usuari, contrassenya, email)
    return usuari

def main():
    # Connexió utilitzant el teu mòdul de base de dades
    connexio = db.get_connection()

    proxim_id = 1
    usuaris_registrats = []
    questionaris_disponibles = []

    while True:
        print("\n  Introdueix una opció   ")
        print("1. Registre Usuari")
        print("2. Iniciar Sessió")
        print("3. Sortir")

        opcio = input("Opció: ")

        match opcio:
            case "1":
                print("\n--- Registre de Nou Usuari ---")
                nou_usuari = crear_usuari(proxim_id)
                usuaris_registrats.append(nou_usuari)
                proxim_id += 1
                print("\n¡Usuari registrat correctament!")
                print(nou_usuari)

            case "2":
                if len(usuaris_registrats) == 0:
                    print("No hi ha usuaris registrats")
                    continue

                nom_login = input("Nom d'usuari: ")
                pass_login = input("Contrasenya: ")

                usuari_actual = None
                for usuari in usuaris_registrats:
                    if usuari.nom_usuari == nom_login and usuari.contrassenya == pass_login:
                        usuari_actual = usuari
                        break

                if usuari_actual is None:
                    print("Credencials incorrectes")
                    continue

                print(f"\nBenvingut {usuari_actual.nom}")

                while True:
                    print("\n--- MENÚ USUARI ---")
                    print("a. Importar qüestionari")
                    print("b. Veure questionaris")
                    print("c. Tancar sessió")
                    
                    opcio2 = input("Opció: ")
                    match opcio2:
                        case "a":
                            ruta = input("Nom del fitxer JSON: ")
                            importador = ImportadorJSON(connexio)
                            
                            # L'importador retorna la llista de nous objectes Questionari
                            nous_questionaris = importador.importar_questionaris(ruta, usuari_actual.id_usuari)
                            
                            # Afegim els objectes un a un sense utilitzar .extend()
                            for questionari in nous_questionaris:
                                questionaris_disponibles.append(questionari)

                        case "b":
                            print("\n--- QUESTIONARIS ---")
                            if len(questionaris_disponibles) == 0:
                                print("No hi ha qüestionaris disponibles. Importa'n un primer.")
                            else:
                                for q in questionaris_disponibles:
                                    print(f"\nTítol: {q.titol}")
                                    print(f"Categoria: {q.categoria}")
                                    print(f"Dificultat: {q.dificultat}/5")
                                    print(f"Preguntes: {len(q.preguntes)}")
                                    print(f"Punts Totals: {q.obtenir_punts_totals()}")

                        case "c":
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