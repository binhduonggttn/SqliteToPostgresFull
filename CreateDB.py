import sqlite3
from numpy import random
conn = sqlite3.connect('testmydb6.db')
cur = conn.cursor()


#Only need to do this once
listOfColumns = ("column0",)
bindMarkers = ",?" #ADDED to allow values to be bound will be ?,?,?,?, ........ 49 ?
for column_number in range(1, 49):
    newColumn = ("column" + str(column_number),)
    listOfColumns = listOfColumns + newColumn
    bindMarkers = bindMarkers + ",?"

for table_number in range(1,11):
    cur.execute("DROP TABLE IF EXISTS table" + str(table_number)) #make it rerunnable
    cur.execute('''CREATE TABLE IF NOT EXISTS table''' + str(table_number) + '''(id INTEGER NOT NULL PRIMARY KEY)''')

    for column_number in listOfColumns:
        cur.execute('''ALTER TABLE table''' + str(table_number) + ''' ADD COLUMN %s TEXT''' % column_number)

    # The INSERT statement note null means that the id will be automatically generated
    insertsql = "INSERT INTO table" + str(table_number) + " VALUES(null" + bindMarkers + ")"
    #print the INSERT SQL (just the once)
    if table_number == 1:
        print(insertsql)

    for row_number in range(1,1001):
        # Generate a list of 49 random values
        listOfRandomValues =[random.randint(1, 999999) for i in range(49)]
        cur.execute(insertsql,listOfRandomValues) # insert the row

    # extract the first 5 rows an print each row
    cursor = cur.execute("SELECT * FROM table" + str(table_number) + " LIMIT 5")
    result = "row in table table" +  str(table_number) + " Data is "
    for row in cursor:
        print(row)

conn.commit()
cur.close()
conn.close()