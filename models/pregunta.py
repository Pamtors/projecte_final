class Pregunta:
    def __init__(self, id_pregunta, id_questionari, tipus, enunciat, respostes, resposta_correcta, punts):
        self.id_pregunta = id_pregunta
        self.id_questionari = id_questionari
        self.tipus = tipus
        self.enunciat = enunciat
        self.respostes = respostes
        self.resposta_correcta = int(resposta_correcta)
        self.punts = int(punts)

    def mostrar_pregunta(self):
        print(f"\n{self.enunciat}")
        for numero, resposta in self.respostes.items():
            if resposta:
                print(f"{numero}. {resposta}")

    def validar_resposta(self, resposta_usuari):
        try:
            resposta = int(resposta_usuari)
        except ValueError:
            print("La resposta ha de ser un número.")
            return False

        if resposta == self.resposta_correcta:
            print("Correcte.")
            return True

        resposta_bona = self.respostes.get(self.resposta_correcta, "")
        print(f"Incorrecte. La resposta correcta era: {resposta_bona}")
        return False

class PreguntaMultiple(Pregunta):
    def __init__(self, id_pregunta, id_questionari, enunciat, r1, r2, r3, r4, resposta_correcta, punts):
        respostes = {
            1: r1,
            2: r2,
            3: r3,
            4: r4
        }
        super().__init__(id_pregunta, id_questionari, "multiple", enunciat, respostes, resposta_correcta, punts)

class PreguntaVF(Pregunta):
    def __init__(self, id_pregunta, id_questionari, enunciat, resposta_correcta, punts):
        respostes = {
            1: "Verdader",
            2: "Fals"
        }
        super().__init__(id_pregunta, id_questionari, "vf", enunciat, respostes, resposta_correcta, punts)
