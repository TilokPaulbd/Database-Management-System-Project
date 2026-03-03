import mysql.connector

Database = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12818572",
    password="22KvcK1UbY",          #Database commected from freesqldatabase.com (Size 5 MB)
    database="sql12818572",   
    port=3306
)


print("Database connected")

cursor = Database.cursor()                    #SQL query chalanur jonno cursor object toiri kora hoy, jeta dea command pathay database a.
cursor.execute("SELECT * FROM Students_info") #Temporary table create kora hoiche database a.
result = cursor.fetchall()
for row in result:
    print(row)


cursor.close()  
Database.close()                            
