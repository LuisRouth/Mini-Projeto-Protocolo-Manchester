import datetime

class Paciente:
    def __init__(self, nome):
        self.nome = nome
        self.hora_chegada = datetime.datetime.now().strftime("%H:%M:%S")

    def __str__(self):
        return f"{self.nome} (chegou às {self.hora_chegada})"