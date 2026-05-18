import json

class Questionari:
    def __init__(self, id_questionari, id_propietari, titol, categoria, dificultat, descripcio):
        self.id_questionari = int(id_questionari)
        self.id_propietari = int(id_propietari)
        self.titol = str(titol)
        self.categoria = str(categoria)
        self.dificultat = int(dificultat)
        self.descripcio = str(descripcio)

    def __str__(self):
        return f"[CATEGORIA: {self.categoria}] TITOL: {self.titol} (DIFICULTAT: {self.dificultat}/5)"

def carregar_questionaris_json(ruta_arxiu="questionaris.json"):
    try:
        with open(ruta_arxiu, "r", encoding="utf-8") as f:
            dades = json.load(f)
            return [
                Questionari(q["id_questionari"], q["id_propietari"], q["titol"], q["categoria"], q["dificultat"],q["descripcio"]) for q in dades
            ]
            
    except (FileNotFoundError, json.JSONDecodeError):
        print("ERROR")
        return []