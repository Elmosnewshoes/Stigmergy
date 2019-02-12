import sqlite3
from cythonic.plugins.queries import new_sim
cimport cython
from pandas import read_sql

cdef class db_controller():
    @cython.wraparound(True) #else cannot use listindex:-1
    def __cinit__(self, str db_path,str db_name):
        " class constructor "
        # required format for path: /path/to/file/
        if not db_path[-1] =='/':
            # add a missing forwardslash if supplied with /path/to/file
            db_path += '/'

        "connect to the database"
        self.db = sqlite3.connect(db_path+db_name)

    def get_df(self,qry):
        " return the qry result as dataframe"
        try:
            return read_sql(qry, self.db, )
        except Exception as error:
            self.db.close()
            raise error

    cdef unsigned int new_sim_id(self,):
        " start logging of sim in sqlite database, get ID of simulation "
        cdef object cursor = self.db.cursor()
        cdef str qry = new_sim()
        cdef unsigned int id
        try:
            cursor.execute(qry)
            id = cursor.lastrowid
            self.db.commit()
        except Exception as error:
            self.db.close()
            raise error
        return id

    cdef void executemany(self,str qry, list values):
        " use the executemany for bulk insert "
        cursor = self.db.cursor()
        try:
            cursor.executemany(qry,values)
            self.db.commit()
        except Exception as error:
            self.db.close()
            raise error

    cdef void execute(self, str qry ):
        " execute an INSERT INTO, CREATE or UPDATE query "
        cdef object cursor = self.db.cursor()
        try:
            cursor.execute(qry)
            self.db.commit()
        except Exception as error:
            print(qry)
            self.db.close()
            raise error

    def close(self):
        " manually close the connection (useful when errors occur halfway a simulation)"
        self.db.close()

    def return_all(self, str qry):
        " return all rows from a select query "
        cdef object cursor = self.db.cursor()
        try:
            cursor.execute(qry)
            headers = [hdr[0] for hdr in cursor.description ]
            rows = cursor.fetchall()
            if len(rows) ==0:
                raise ValueError('No rows returned')
        except Exception as error:
            print(qry)
            self.db.close()
            raise error
        return rows, headers

    def print_all(self,str qry):
        " Print all results from a select qry "
        rows, headers = self.return_all(qry)
        print(headers)
        for row in rows:
            print(row)
