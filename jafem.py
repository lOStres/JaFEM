import sys, os
from readdata import *
from rtree import index

# perform k-NN search for file in spatial index
def similarity(directory, filename, k):
    # first extract features from query file
    featureVector = extractFeatures(directory,filename)

    # then open and query spatial index
    p = index.Property()
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    p.dimension = 13

    rtree = index.Index('rtreez', properties=p, interleaved=True)
    similar = list(rtree.nearest((featureVector[0], featureVector[1],
        featureVector[2], featureVector[3], featureVector[4],featureVector[5],
        featureVector[6], featureVector[7], featureVector[8], featureVector[9],
        featureVector[10], featureVector[11], featureVector[12],
        featureVector[0], featureVector[1], featureVector[2], featureVector[3],
        featureVector[4], featureVector[5], featureVector[6], featureVector[7],
        featureVector[8], featureVector[9], featureVector[10],
        featureVector[11], featureVector[12]), k))
    print(similar)

# perform search on name of file and display information
def metaQuery(filename):

    con = psycopg2.connect(database='testdb', user='klwnos')
    cur = con.cursor()

    query = """SELECT * FROM metadata
            WHERE id = %s;"""
    data = (filename,)
    cur.execute(query, data)
    records = cur.fetchall()

    return records

def main():
    ex=wx.App()
    UI(None)
    ex.MainLoop()
    # initialize table metadata
    if len(sys.argv) == 2 and sys.argv[1] == '-i':

        con = None
        try:
	        # TODO prepei na allaksei auto gia na mporoume na to xrhsimopoioume kai oi 2
            con = psycopg2.connect(database='testdb', user='klwnos')
            cur = con.cursor()

            cur.execute('''CREATE TABLE metadata
                    (id INT PRIMARY KEY, filesize INT, duration FLOAT,
                    samplerate INT, tags VARCHAR(200) ARRAY, type VARCHAR(7),
                    saliance VARCHAR(5), startime FLOAT, endtime FLOAT,
                    class VARCHAR(20), link VARCHAR(200));''')
            # TODO kai auto pepei na allaksei		
            directory = "/home/klwnos/Documents/children_playing"

            # create or open spatial index
            p = index.Property()
            p.dat_extension = 'data'
            p.idx_extension = 'index'
            p.dimension = 13

            rtree = index.Index('rtreez', properties=p, interleaved=True)
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
                    featureVector = extractFeatures(directory,filename)

                    link = directory + '/' + name + '.' + extension

                    #insert to spatialindex
                    rtree.insert(int(name), (featureVector[0], featureVector[1],
                        featureVector[2], featureVector[3], featureVector[4],
                        featureVector[5], featureVector[6], featureVector[7],
                        featureVector[8], featureVector[9], featureVector[10],
                        featureVector[11], featureVector[12], featureVector[0],
                        featureVector[1], featureVector[2], featureVector[3],
                        featureVector[4], featureVector[5], featureVector[6],
                        featureVector[7], featureVector[8], featureVector[9],
                        featureVector[10], featureVector[11],
                        featureVector[12]))

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
            # TODO kai auto prepei na allaksei
            con = psycopg2.connect(database='testdb', user='klwnos')
            cur = con.cursor()

            cur.execute("DROP TABLE metadata")

        except psycopg2.DatabaseError as err:
            print( 'Error %s' % err)
            sys.exit(1)

        finally:

            if con:
                con.commit()
                con.close()

    # content-based query
    elif len(sys.argv) == 2 and sys.argv[1] == '-q':

        contentQuery("/home/klwnos/Documents/children_playing", "12.mp3", 5)

    # meta data query
    elif len(sys.argv) == 2 and sys.argv[1] == '-m':

        metaQuery("12")


if __name__ == "__main__":
    main()
