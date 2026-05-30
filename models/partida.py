from datetime import datetime
from database.database import db_guardar_partida

class Partida:
    def __init__(self, id_questionari, tipus, id_partida=None, data_partida=None):
        self.id_partida = id_partida
        self.id_questionari = int(id_questionari)
        
        if tipus.upper() not in ['INDIVIDUAL', 'VS']:
            raise ValueError("El tipus de partida ha de ser 'INDIVIDUAL' o 'VS'.")
        self.tipus = tipus.upper()
        
        self.data_partida = data_partida if data_partida else datetime.now()

    def guardar(self, connexio):
        id_generat = db_guardar_partida(
            connexio, 
            self.id_questionari, 
            self.tipus, 
            self.data_partida
        )
        if id_generat:
            self.id_partida = id_generat
        return id_generat

    def __str__(self):
        return f"[PARTIDA {self.id_partida}] Qüestionari: {self.id_questionari} | Tipus: {self.tipus} | Data: {self.data_partida}"