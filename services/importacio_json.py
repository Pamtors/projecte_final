import json
from database.database import get_connection
from models.questionari import Questionari
from models.pregunta import PreguntaMultiple, PreguntaVF

class ImportadorJSON:
    def importar_questionaris(self, ruta_json, id_usuari):
        try:
            with open(ruta_json, "r", encoding="utf-8") as fitxer:
                dades = json.load(fitxer)
        except FileNotFoundError:
            print("No s'ha trobat el fitxer.")
            return []
        except json.JSONDecodeError:
            print("El fitxer no té un format JSON correcte.")
            return []

        if "questionaris" not in dades:
            print("El JSON ha de tenir la clau questionaris.")
            return []

        connexio = get_connection()
        questionaris_carregats = []

        for element in dades["questionaris"]:
            info = element.get("informacio", {})
            titol = info.get("titol", "Sense títol")
            categoria = info.get("categoria", "General")
            dificultat = int(info.get("dificultat", 1))
            descripcio = info.get("descripcio", "")

            cursor = connexio.cursor()
            cursor.execute(
                "INSERT INTO questionaris (id_propietari, titol, categoria, dificultat, descripcio) VALUES (%s, %s, %s, %s, %s)",
                (id_usuari, titol, categoria, dificultat, descripcio)
            )
            id_questionari = cursor.lastrowid
            questionari = Questionari(id_questionari, id_usuari, titol, categoria, dificultat, descripcio)

            for pregunta_json in element.get("preguntes", []):
                tipus = str(pregunta_json.get("tipus", "multiple")).lower()
                enunciat = pregunta_json.get("enunciat", "")
                respostes = pregunta_json.get("respostes", {})
                resposta1 = respostes.get("resposta1")
                resposta2 = respostes.get("resposta2")
                resposta3 = respostes.get("resposta3")
                resposta4 = respostes.get("resposta4")
                resposta_correcta = int(pregunta_json.get("resposta_correcta", 1))
                punts = int(pregunta_json.get("punts", 1))

                cursor.execute(
                    "INSERT INTO preguntes (id_questionari, tipus, enunciat, resposta1, resposta2, resposta3, resposta4, resposta_correcta, punts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (id_questionari, tipus, enunciat, resposta1, resposta2, resposta3, resposta4, resposta_correcta, punts)
                )
                id_pregunta = cursor.lastrowid

                if tipus == "vf":
                    pregunta = PreguntaVF(id_pregunta, id_questionari, enunciat, resposta_correcta, punts)
                else:
                    pregunta = PreguntaMultiple(id_pregunta, id_questionari, enunciat, resposta1, resposta2, resposta3, resposta4, resposta_correcta, punts)

                questionari.afegir_pregunta(pregunta)

            questionaris_carregats.append(questionari)

        connexio.commit()
        connexio.close()
        print(f"S'han importat {len(questionaris_carregats)} qüestionaris.")
        return questionaris_carregats
