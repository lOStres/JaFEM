import psycopg2
import sys


con = None

try:
     
    con = psycopg2.connect(database='testdb', user='jafem')
    cur = con.cursor()
    cur.execute('''CREATE TABLE metadata
            (Id INT PRIMARY KEY, Filesize INT, Duration FLOAT, Samplerate INT,
            Tags VARCHAR(20) ARRAY, Type VARCHAR(7), Saliance VARCHAR(5),
            StartTime FLOAT, EndTime FLOAT, Class VARCHAR(20));''')
    cur.execute('SELECT version()')
    ver = cur.fetchone()
    print(ver)    
    

except psycopg2.DatabaseError as err:
    print( 'Error %s' % err)    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
