import copy

import networkx as nx

from database.dao import DAO
from database.rifugio import Rifugio


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self._percorso_ottimale = []
        self._difficolta_ottimale = 1000
        self.G = nx.Graph()
        self._connessioni = []
        self._id_map_rifugi = {}


    def load_connessioni(self):
        self._connessioni= DAO.get_all_connessioni()
        return self._connessioni

    def load_rifugi(self):
        self._id_map_rifugi= DAO.get_all_rifugi()
        return self._id_map_rifugi



    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.G.clear()
        self.load_connessioni()
        self.load_rifugi()


        dizionario_difficolta= {"facile": 1.0, "media": 1.5, "difficile": 2.0}
        for c in self._connessioni:
            r1= c.id_rifugio1
            r2= c.id_rifugio2

            rif1= self._id_map_rifugi[r1]
            rif2= self._id_map_rifugi[r2]
            difficolta= c.difficolta
            peso= float(c.distanza) * float(dizionario_difficolta[difficolta])

            if c.anno <= year:
                self.G.add_edge(rif1, rif2, weight=peso)




    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        lista_pesi=[]
        for e in self.G.edges():
            p= self.G[e[0]][e[1]]['weight']
            lista_pesi.append(p)
        return min(lista_pesi), max(lista_pesi)



    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        lista_minori=[]
        lista_maggiori=[]
        for e in self.G.edges():
            if self.G[e[0]][e[1]]['weight'] < soglia:
                lista_minori.append(e)
            elif self.G[e[0]][e[1]]['weight'] > soglia:
                lista_maggiori.append(e)
        return len(lista_minori), len(lista_maggiori)


    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    def get_percorso_ottimo(self, soglia):
        self._percorso_ottimale = []
        self._difficolta_ottimale = 1000

        for n in self.G.nodes():
            self._ricorsione(n, [n], 0, soglia )
        return self._percorso_ottimale, self._difficolta_ottimale

    def _ricorsione (self, node : Rifugio , percorso_corrente, difficolta_corrente, soglia):
        if len(percorso_corrente) >= 3 and difficolta_corrente < self._difficolta_ottimale:
            self._difficolta_ottimale = difficolta_corrente
            self._percorso_ottimale= percorso_corrente

        if len(self._percorso_ottimale)!=0 and difficolta_corrente > self._difficolta_ottimale:
            return

        for vicino in self.G.neighbors(node):
            if vicino not in percorso_corrente:
                peso= self.G[node][vicino]['weight']

                if peso> soglia:
                    nuova_difficolta= difficolta_corrente+ peso
                    nuovo_percorso= copy.deepcopy(percorso_corrente)
                    nuovo_percorso.append(vicino)
                    self._ricorsione(vicino,nuovo_percorso,nuova_difficolta, soglia)








