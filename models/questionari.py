class Questionari:
    def __init__(self, id_questionari, id_propietari, titol, categoria, dificultat, descripcio):
        self.id_questionari = int(id_questionari)
        self.id_propietari = int(id_propietari)
        self.titol = str(titol)
        self.categoria = str(categoria)
        self.dificultat = int(dificultat)
        self.descripcio = str(descripcio)
        self.preguntes = []

    def afegir_pregunta(self, pregunta):
        self.preguntes.append(pregunta)

    def obtenir_punts_totals(self):
        totals = 0
        for p in self.preguntes:
            totals += p.punts
        return totals

    def __str__(self):
        return f"[CATEGORIA: {self.categoria}] TITOL: {self.titol} (DIFICULTAT: {self.dificultat}/5)"