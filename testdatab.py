
import psycopg2
import sys


con = None

try:
     
    con = psycopg2.connect(database='vash', user='tabrianos') 
    cur = con.cursor()
    cur.execute('SELECT version()')          
    ver = cur.fetchone()
    print(ver)    
    

except psycopg2.DatabaseError as err:
    print( 'Error %s' % err)    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
