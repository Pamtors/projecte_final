from datetime import datetime

class Partida:
    def __init__(self, id_partida, id_questionari, tipus, data_partida=None):
        self.id_partida = id_partida
        self.id_questionari = id_questionari
        self.tipus = tipus
        self.data_partida = data_partida or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f"Partida {self.id_partida} - Qüestionari {self.id_questionari} - {self.tipus} - {self.data_partida}"
