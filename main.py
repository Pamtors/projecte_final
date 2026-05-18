from models.usuari import Usuari
from datetime import date
from models.questionari import carregar_questionaris_json

def crear_usuari(id_usuari):
    nom = input("Introdueix el teu nom: ")
    nom_usuari = input("Introdueix el teu nom d'usuari: ")

    while True:
        contrassenya = input(
            "Introdueix la contrasenya (mínim 8 caràcters): "
        )
        
        if len(contrassenya) >= 8:
            break
        print("La contrasenya ha de tenir com a mínim 8 caràcters.")

    email = input("Introdueix el teu email: ")
    
    usuari = Usuari(id_usuari, nom, nom_usuari, contrassenya, email)
    return usuari

def main():
    proxim_id = 1
    usuaris_registrats = [] 
    questionaris_disponibles = carregar_questionaris_json("questionaris.json")

    while True:
        print("  Introdueix una opció   ")
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
                print("Has seleccionat l'opció 2")

            case "3":
                print("Sortint de l'aplicació...")
                break 

            case _:
                print("Opció no vàlida")

if __name__ == "__main__":
    main()