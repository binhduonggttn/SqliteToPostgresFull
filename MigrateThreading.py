import psycopg2, sqlite3, sys
import time
from threading import Lock
import threading


sqdb="D://Python//SqliteToPostgreFull//testmydb6.db"
sqlike="table"
pgdb="testmydb12"
pguser="postgres"
pgpswd="1234"
pghost="127.0.0.1"
pgport="5432"

 
consq=sqlite3.connect(sqdb, check_same_thread=False)
cursq=consq.cursor()
 
tabnames=[]
print() 
cursq.execute('''SELECT name FROM sqlite_master WHERE type="table" AND name LIKE "'''+sqlike+'''%";''')
tabgrab = cursq.fetchall()
for item in tabgrab:
    tabnames.append(item[0])
print(tabgrab)

lock = threading.Lock()

def copyTable(table):
    cursq.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name = ?;", (table,))
    create = cursq.fetchone()[0]
    cursq.execute("SELECT * FROM %s;" %table)
    rows=cursq.fetchall()
    colcount=len(rows[0])
    pholder='%s,'*colcount
    newholder=pholder[:-1]
 
    try:
        lock.acquire(True)
        conpg = psycopg2.connect(database=pgdb, user=pguser, password=pgpswd,
                               host=pghost, port=pgport)
        curpg = conpg.cursor()
        curpg.execute("DROP TABLE IF EXISTS %s;" %table)
        create = create.replace("AUTOINCREMENT", "")
        curpg.execute(create)
        curpg.executemany("INSERT INTO %s VALUES (%s);" % (table, newholder),rows)
        conpg.commit()
        
        if conpg:
            conpg.close()
 
    except psycopg2.DatabaseError as e:
        print ('Error %s' % e) 
        sys.exit(1)
 
    finally:
        lock.release()
        print("Complete")
        
 

if __name__ == "__main__":
    start_time = time.time()
    for table in tabnames:
        p = threading.Thread(target = copyTable, args = (table,))
        p.start()
  

    duration = time.time() - start_time
    print(f"Duration {duration} seconds")