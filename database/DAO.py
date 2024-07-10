from database.DB_connect import DBConnect
from model import States


class DAO():

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(s.datetime) as anno
                from new_ufo_sightings.sighting s 
                order by anno DESC"""
        cursor.execute(query, ())
        for row in cursor:
            result.append(row["anno"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getForme():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.shape as forma
                        from new_ufo_sightings.sighting s 
                        order by forma"""
        cursor.execute(query, ())
        for row in cursor:
            result.append(row["forma"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getStati():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from new_ufo_sightings.state s
                """#sono gia tutti distinte secondo id le righe (gli stati)
        cursor.execute(query, ())
        for row in cursor:
            result.append(States.State(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(dizionarioStati):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from new_ufo_sightings.neighbor n 
                       """  # sono gia tutti distinte secondo id le righe (gli stati)
        cursor.execute(query, ())
        for row in cursor:
            ID1=row["state1"]
            ID2=row["state2"]
            result.append((dizionarioStati[ID1], dizionarioStati[ID2]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def aggiornaDizArchiPesi(anno,forma,dizionarioArchiPesiInizializzati):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query=      """  
                    SELECT n.state1 as IDstate1, n.state2 as IDstate2, count(*) as peso
                    FROM new_ufo_sightings.sighting s , new_ufo_sightings.neighbor n 
                    where   year(s.`datetime`) =%s
                            and s.shape = %s
                            and (s.state = n.state1 or s.state = n.state2 )
                            and n.state1 < n.state2
                    group by n.state1 , n.state2
                    """
        cursor.execute(query, (anno, forma))
        for row in cursor:
            print((row['IDstate1'], row['IDstate2']), row['peso'])
            print()
            dizionarioArchiPesiInizializzati[(row['IDstate1'].upper(), row['IDstate2'].upper())]= row['peso']


        cursor.close()
        conn.close()
        return dizionarioArchiPesiInizializzati