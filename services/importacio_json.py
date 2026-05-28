import json
from models.questionari import Questionari
from models.pregunta import PreguntaMultiple, PreguntaVF

class ImportadorJSON:
    def __init__(self, connexio):
        self.conn = connexio
        self.cursor = self.conn.cursor()

    def importar_questionaris(self, ruta_json, id_usuari):
        creats = 0
        actualitzats = 0

        try:
            with open(ruta_json, "r", encoding="utf-8") as fitxer:
                dades = json.load(fitxer)
        except FileNotFoundError:
            print("Fitxer no trobat")
            return []
        except json.JSONDecodeError:
            print("Error llegint el JSON")
            return []

        questionaris_carregats = []
        questionaris = dades["questionaris"]

        for q in questionaris:
            info = q["informacio"]
            titol = info["titol"]
            categoria = info["categoria"]
            dificultat = info["dificultat"]
            descripcio = info["descripcio"]

            print("\n======================")
            print(f"TÍTOL: {titol}")
            print(f"CATEGORIA: {categoria}")
            print(f"DIFICULTAT: {dificultat}")
            print(f"PREGUNTES: {len(q['preguntes'])}")
            print("======================")

            self.cursor.execute("""
                SELECT id_questionari
                FROM questionaris
                WHERE titol = ? AND id_propietari = ?
            """, (titol, id_usuari))

            existent = self.cursor.fetchone()

            if existent:
                opcio = input(
                    "Aquest qüestionari ja existeix.\n"
                    "1. Actualitzar\n"
                    "2. Guardar amb nou títol\n"
                    "Opció: "
                )

                if opcio == "1":
                    id_questionari = existent[0]
                    self.cursor.execute("""
                        DELETE FROM preguntes
                        WHERE id_questionari = ?
                    """, (id_questionari,))

                    self.cursor.execute("""
                        UPDATE questionaris
                        SET categoria = ?,
                            dificultat = ?,
                            descripcio = ?
                        WHERE id_questionari = ?
                    """, (categoria, dificultat, descripcio, id_questionari))
                    actualitzats += 1
                else:
                    titol = input("Nou títol: ")
                    self.cursor.execute("""
                        INSERT INTO questionaris
                        (id_propietari, titol, categoria, dificultat, descripcio)
                        VALUES (?, ?, ?, ?, ?)
                    """, (id_usuari, titol, categoria, dificultat, descripcio))
                    id_questionari = self.cursor.lastrowid
                    creats += 1
            else:
                self.cursor.execute("""
                    INSERT INTO questionaris
                    (id_propietari, titol, categoria, dificultat, descripcio)
                    VALUES (?, ?, ?, ?, ?)
                """, (id_usuari, titol, categoria, dificultat, descripcio))
                id_questionari = self.cursor.lastrowid
                creats += 1

            obj_questionari = Questionari(id_questionari, id_usuari, titol, categoria, dificultat, descripcio)

            for p in q["preguntes"]:
                self.cursor.execute("""
                    INSERT INTO preguntes
                    (id_questionari, tipus, enunciat, resposta1, resposta2, resposta3, resposta4, resposta_correcta, punts)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    id_questionari,
                    p["tipus"],
                    p["enunciat"],
                    p["respostes"]["resposta1"],
                    p["respostes"]["resposta2"],
                    p["respostes"]["resposta3"],
                    p["respostes"]["resposta4"],
                    p["resposta_correcta"],
                    p["punts"]
                ))
                id_pregunta = self.cursor.lastrowid

                if p["tipus"] == "VF":
                    obj_pregunta = PreguntaVF(id_pregunta, id_questionari, p["enunciat"], p["resposta_correcta"], p["punts"])
                else:
                    obj_pregunta = PreguntaMultiple(
                        id_pregunta, id_questionari, p["enunciat"],
                        p["respostes"]["resposta1"], p["respostes"]["resposta2"],
                        p["respostes"]["resposta3"], p["respostes"]["resposta4"],
                        p["resposta_correcta"], p["punts"]
                    )
                obj_questionari.afegir_pregunta(obj_pregunta)

            questionaris_carregats.append(obj_questionari)

        self.conn.commit()
        print("\nIMPORTACIÓ FINALITZADA")
        print(f"Qüestionaris creats: {creats}")
        print(f"Qüestionaris actualitzats: {actualitzats}")
        
        return questionaris_carregats