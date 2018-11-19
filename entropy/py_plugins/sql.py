import sqlite3

class SqLite:
    " qry handler "
    def __init__(self, path, db_name):
        self.db = sqlite3.connect(path+db_name)

    def select(self, qry):
        cursor = self.db.cursor()
        try:
            cursor.execute(qry)
        except Exception as error:
            self.db.close()
            print(qry)
            raise error
        result = cursor.fetchall()
        if len(result) == 0:
            raise AssertionError("Zero (0) rows returned: ", qry)
        headers = cursor.description
        return result, headers

    def select_dict(self,qry):
        result,headers = self.select(qry)
        result_dict = {}
        i = 0
        for header in headers:
            result_dict[header[0]] = [rw[i] for rw in result]
            i+=1
        return result_dict

    def insert(self,qry):
        cursor = self.db.cursor()
        try:
            cursor.execute(qry)
            id = cursor.lastrowid
        except Exception as error:
            self.db.close()
            print(qry)
            raise error
        self.db.commit()
        return id




if __name__ == '__main__':
    import sys
    QRY = SqLite("/home/bram/ANTS/entropy/core/database/","stigmergy_database.db")
    r = QRY.select_dict("select * from sims")
    from pandas import DataFrame
    D = DataFrame(data=r)
    print(D.at[3,'ID'])
