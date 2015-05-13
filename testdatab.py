
import psycopg2
import sys

from readdata import *

def main():
    # initialize table metadata
    if len(sys.argv) == 2 and sys.argv[1] == '-i':

        con = None
        try:

            con = psycopg2.connect(database='testdb', user='klwnos')
            cur = con.cursor()

            cur.execute('''CREATE TABLE metadata
                    (id INT PRIMARY KEY, filesize INT, duration FLOAT,
                    samplerate INT, tags VARCHAR(20) ARRAY, type VARCHAR(7),
                    saliance VARCHAR(5), startime FLOAT, endtime FLOAT,
                    class VARCHAR(20));''')
            directory = "/home/klwnos/Documents/children_playing"

            print("scanning directory", directory)
            # scanning directory and inserting values to db
            for file in os.listdir(directory):
                name , extension = file.rsplit('.',1);

                # parse meta-data
                if extension == "csv":
                    meta = parseCSV(directory, file)

                    query = 'INSERT INTO metadata (id, startime, endtime, saliance, class) VALUES (%s, %s, %s, %s, %s);'
                    data = (name, meta[0], meta[1], meta[2], meta[3])
                    cur.execute(query, data)

                elif extension == "json":
                    meta = parseJSON(directory, file)
                else:

                    pass    # do something

        except psycopg2.DatabaseError as err:
            print( 'Error %s' % err)
            sys.exit(1)

        finally:

            if con:
                con.commit()
                con.close()

    # drop table metadata
    elif len(sys.argv) == 2 and sys.argv[1] == '-d':

        con = None
        try:

            con = psycopg2.connect(database='testdb', user='klwnos')
            cur = con.cursor()

            cur.execute("DROP TABLE metadata")
            con.commit()

        except psycopg2.DatabaseError as err:
            print( 'Error %s' % err)
            sys.exit(1)

        finally:

            if con:
                con.close()

if __name__ == "__main__":
    main()
