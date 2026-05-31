class Questionari:
    def __init__(self, id_questionari, id_propietari, titol, categoria, dificultat, descripcio):
        self.id_questionari = id_questionari
        self.id_propietari = id_propietari
        self.titol = titol
        self.categoria = categoria
        self.dificultat = dificultat
        self.descripcio = descripcio
        self.preguntes = []

    def afegir_pregunta(self, pregunta):
        self.preguntes.append(pregunta)

    def obtenir_punts_totals(self):
        total = 0
        for pregunta in self.preguntes:
            total += pregunta.punts
        return total

    def __str__(self):
        return (
            f"{self.titol}\n"
            f"Categoria: {self.categoria}\n"
            f"Dificultat: {self.dificultat}\n"
            f"Descripció: {self.descripcio}\n"
            f"Preguntes: {len(self.preguntes)}\n"
            f"Punts totals: {self.obtenir_punts_totals()}"
        )
