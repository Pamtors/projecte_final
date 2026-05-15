def main():
    opcio = input("Introdueix una opció (1, 2 o 3): ")
    match opcio:
        case "1":
            print("Has seleccionat l'opció 1")
        case "2":
            print("Has seleccionat l'opció 2")
        case "3":
            print("Has seleccionat l'opció 3")
        case _:
            print("Opció no vàlida")

if __name__ == "__main__":
    main()