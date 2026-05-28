class Pregunta:
    def __init__(self, id_pregunta, id_questionari, tipus, enunciat, resposta_correcta, punts=1):
        self.id_pregunta = id_pregunta
        self.id_questionari = id_questionari
        self.tipus = tipus
        self.enunciat = enunciat
        self.resposta_correcta = resposta_correcta
        self.punts = punts

    def mostrar_pregunta(self):
        raise NotImplementedError("Aquest mètode s'ha d'implementar a la subclasse")

    def validar_resposta(self, opcio_usuari):
        raise NotImplementedError("Aquest mètode s'ha d'implementar a la subclasse")


class PreguntaMultiple(Pregunta):
    def __init__(self, id_pregunta, id_questionari, enunciat, r1, r2, r3, r4, resposta_correcta, punts=1):
        Pregunta.__init__(self, id_pregunta, id_questionari, "MULTIPLE", enunciat, resposta_correcta, punts)
        self.respostes = {
            1: r1,
            2: r2,
            3: r3,
            4: r4
        }

    def mostrar_pregunta(self):
        print(f"\n[Pregunta - {self.punts} Punts] {self.enunciat}")
        for opcio, text in self.respostes.items():
            if text:
                print(f"  {opcio}. {text}")

    def validar_resposta(self, opcio_usuari):
        try:
            opcio_int = int(opcio_usuari)
            if opcio_int == self.resposta_correcta:
                print("¡Correcte! Resposta encertada.")
                return True
            else:
                resposta_text = self.respostes.get(self.resposta_correcta)
                print(f"Incorrecte. La resposta correcta era la {self.resposta_correcta}: {resposta_text}")
                return False
        except (ValueError, KeyError):
            print("Error: Has d'introduir un número d'opció vàlid.")
            return False


class PreguntaVF(Pregunta):
    def __init__(self, id_pregunta, id_questionari, enunciat, resposta_correcta, punts=1):
        Pregunta.__init__(self, id_pregunta, id_questionari, "VF", enunciat, resposta_correcta, punts)
        self.respostes = {
            1: "Verdader",
            2: "Fals"
        }

    def mostrar_pregunta(self):
        print(f"\n[Pregunta V/F - {self.punts} Punts] {self.enunciat}")
        print("  1. Verdader")
        print("  2. Fals")

    def validar_resposta(self, opcio_usuari):
        try:
            opcio_int = int(opcio_usuari)
            if opcio_int == self.resposta_correcta:
                print("¡Correcte! Resposta encertada.")
                return True
            else:
                resposta_text = self.respostes.get(self.resposta_correcta)
                print(f"Incorrecte. La resposta correcta era: {resposta_text}")
                return False
            
        except ValueError:
            print("Error: Introdueix 1 per Verdader o 2 per Fals.")
            return False