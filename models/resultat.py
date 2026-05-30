from database.database import db_guardar_resultat

class Resultat:
    def __init__(self, id_partida, id_usuari, puntuacio, resultat, id_resultat=None):
        self.id_resultat = id_resultat
        self.id_partida = int(id_partida)
        self.id_usuari = int(id_usuari)
        self.puntuacio = float(puntuacio)
        
        if resultat.upper() not in ['WIN', 'LOSE', 'DRAW']:
            raise ValueError("El resultat ha de ser 'WIN', 'LOSE' o 'DRAW'.")
        self.resultat = resultat.upper()

    def guardar(self, connexio):
        id_generat = db_guardar_resultat(
            connexio, 
            self.id_partida, 
            self.id_usuari, 
            self.puntuacio, 
            self.resultat
        )
        if id_generat:
            self.id_resultat = id_generat
        return id_generat

    def __str__(self):
        return f"[RESULTAT] Partida: {self.id_partida} | Usuari: {self.id_usuari} | Puntuació: {self.puntuacio:.2f} | Resultat: {self.resultat}"