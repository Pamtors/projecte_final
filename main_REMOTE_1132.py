from models import User


def main():
    print("-------------------------")
    print("  Introdueix una opció   ")
    print("-------------------------")
    print("1. Registre Usuari")
    print("2. Iniciar Sessió")
    print("3. Sortir")
    opcio = input("Opció: ")

    match opcio:
        case "1":
            print("Has seleccionat l'opció 1")


        case "2":
            print("Has seleccionat l'opció 2")

        case "3":
            print("Sortint de l'aplicació...")

        case _:
            print("Opció no vàlida")

if __name__ == "__main__":
    main()