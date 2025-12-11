from database.DB_connect import DBConnect
from database.connessione import Connessione
from database.rifugio import Rifugio


class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    # TODO
    @staticmethod
    def get_all_connessioni():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query= "SELECT * FROM connessione"
        result= []
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
            return None
        for row in cursor:
            connessione= Connessione(
                row["id"],
                row["id_rifugio1"],
                row["id_rifugio2"],
                row["distanza"],
                row["difficolta"],
                row["durata"],
                row["anno"])
            result.append(connessione)
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_all_rifugi():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM rifugio"
        result = {}
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
            return None
        for row in cursor:
            rifugio = Rifugio(
                row['id'],
                row['nome'],
                row["localita"],
                row["altitudine"],
                row["capienza"],
                row["aperto"])
            result[rifugio.id] = rifugio
        cursor.close()
        cnx.close()
        return result







