from dataclasses import dataclass

@dataclass
class Connessione:
    id : int
    id_rifugio1 : int
    id_rifugio2 : int
    distanza : float
    difficolta :str
    durata : int
    anno : int


    def __str__(self):
        return f"[{self.id_rifugio1}], [{self.id_rifugio2}] '{self.distanza}, {self.difficolta}"

    def __hash__(self):
        return hash(self.id)