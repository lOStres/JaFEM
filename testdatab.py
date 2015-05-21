
import psycopg2
import sys
import soundfile as sf

from rtree import index
from scipy.fftpack import dct
from features import *
from readdata import *

def main():
    # initialize table metadata
    if len(sys.argv) == 2 and sys.argv[1] == '-i':

        con = None
        try:
	        # TODO prepei na allaksei auto gia na mporoume na to xrhsimopoioume kai oi 2
            con = psycopg2.connect(database='testdb2', user='tabrianos')
            cur = con.cursor()

            cur.execute('''CREATE TABLE metadata
                    (id INT PRIMARY KEY, filesize INT, duration FLOAT,
                    samplerate INT, tags VARCHAR(200) ARRAY, type VARCHAR(7),
                    saliance VARCHAR(5), startime FLOAT, endtime FLOAT,
                    class VARCHAR(20), link VARCHAR(200));''')
            # TODO kai auto pepei na allaksei		
            directory = "/home/tabrianos/Desktop/vaseis/test"

            # create or open spatial index
            p = index.Property()
            p.dimension = 4
            rtree = index.Rtree(properties = p)
            mbr = (0, 0, 0, 0, 0.001, 0.001, 0.001, 0.001)
            index_id = 1

            print("scanning directory", directory)
            # scanning directory and inserting values to db
            for filename in os.listdir(directory):
                name , extension = filename.rsplit('.',1);

                if not name:
                    continue;

                # parse meta-data
                if extension == "csv":
                    meta = parseCSV(directory, filename)

                    query = """INSERT INTO metadata
                    (id, startime, endtime, saliance, class)
                    VALUES (%s, %s, %s, %s, %s);"""
                    data = (name, meta[0], meta[1], meta[2], meta[3])
                    cur.execute(query, data)

                elif extension == "json":
                    meta = parseJSON(directory, filename)

                    query = """UPDATE metadata SET filesize = %s,
                        duration = %s, samplerate = %s, tags = %s, type = %s
                        WHERE id = %s;"""
                    data = (meta[0], meta[1], meta[2], meta[3], meta[4], name)
                    cur.execute(query, data)
                else:
                    # TODO soundfile doesnt work for .mp3, for now just excluding them
                    if(not(filename.endswith('.mp3'))):
                        featureV = extractFeatures(directory,filename)
                        link = directory + '/' + name + '.' + extension
		                #insert to spatialindex
                        rtree.insert(index_id, (featureV[0][0], featureV[1][0],
                            featureV[2][0], featureV[3][0], featureV[0][0],
                            featureV[1][0], featureV[2][0], featureV[3][0]),
                            obj = link)
                        index_id+=1

                        query = """UPDATE metadata SET link = %s
                            WHERE id = %s;"""
                        data = (link, name)
                        cur.execute(query, data)

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
            #kai auto prepei na allaksei
            con = psycopg2.connect(database='testdb2', user='tabrianos')
            cur = con.cursor()

            cur.execute("DROP TABLE metadata")

        except psycopg2.DatabaseError as err:
            print( 'Error %s' % err)
            sys.exit(1)

        finally:

            if con:
                con.commit()
                con.close()

if __name__ == "__main__":
    main()
