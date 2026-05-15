from datetime import date

class Usuari:
    def __init__(self, id_usuari, nom, nom_usuari, contrassenya, email):
        self.id_usuari = id_usuari
        self.nom = nom
        self.nom_usuari = nom_usuari
        self.contrassenya = contrassenya
        self.email = email
        self.data_registre = date.today()

        self.num_partides = 0
        self.victories = 0
        self.derrotes = 0
        self.empats = 0
        self.puntuacio_total = 0.0

    def crear_usuari(self):
        self.nom = input("Introdueix el teu nom: ")
        self.nom_usuari = input("Introdueix el teu nom d'usuari: ")

        while True:
            self.contrassenya = input(
                "Introdueix la contrasenya (mínim 8 caràcters): "
            )
            
            if len(self.contrassenya) >= 8:
                break
            print("La contrasenya ha de tenir com a mínim 8 caràcters.")

        self.email = input("Introdueix el teu email: ")
        self.data_registre = date.today()
        usuari = Usuari(id, )
        insertar_usuari(usuari)
    def afegir_victoria(self):
        self.num_partides += 1
        self.victories += 1

    def afegir_derrota(self):
        self.num_partides += 1
        self.derrotes += 1

    def afegir_empat(self):
        self.num_partides += 1
        self.empats += 1

    def afegir_puntuacio(self, puntuacio):
        self.puntuacio_total += puntuacio

    def mitjana_puntuacio(self):
        if self.num_partides == 0:
            return 0
        return self.puntuacio_total / self.num_partides

    def __str__(self):
        return (
            f"ID: {self.id_usuari}\n"
            f"Nom: {self.nom}\n"
            f"Nom d'usuari: {self.nom_usuari}\n"
            f"Email: {self.email}\n"
            f"Data de registre: {self.data_registre}\n"
            f"Partides jugades: {self.num_partides}\n"
            f"Victòries: {self.victories}\n"
            f"Derrotes: {self.derrotes}\n"
            f"Empats: {self.empats}\n"
            f"Puntuació total: {self.puntuacio_total}\n"
            f"Mitjana puntuació: {self.mitjana_puntuacio():.2f}\n"
        )