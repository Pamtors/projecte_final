class Resultat:
    def __init__(self, id_resultat, id_partida, id_usuari, puntuacio, resultat):
        self.id_resultat = id_resultat
        self.id_partida = id_partida
        self.id_usuari = id_usuari
        self.puntuacio = float(puntuacio)
        self.resultat = resultat

    def __str__(self):
        return f"Usuari {self.id_usuari} - {self.puntuacio:.2f} punts - {self.resultat}"
