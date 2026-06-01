from datetime import date

class Usuari:
    def __init__(self, id_usuari, nom, nom_usuari, contrassenya, email, data_registre=None, num_partides=0, victories=0, derrotes=0, empats=0, puntuacio_total=0.0):
        self.id_usuari = id_usuari
        self.nom = nom
        self.nom_usuari = nom_usuari
        self.contrassenya = contrassenya
        self.email = email
        
        self.data_registre = data_registre if data_registre else date.today().strftime('%Y-%m-%d')

        self.num_partides = num_partides
        self.victories = victories
        self.derrotes = derrotes
        self.empats = empats
        self.puntuacio_total = float(puntuacio_total) # Nos aseguramos de que sea float

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
            f"Puntuació total: {self.puntuacio_total:.2f}\n"
            f"Mitjana de puntuació: {self.mitjana_puntuacio():.2f}"
        )