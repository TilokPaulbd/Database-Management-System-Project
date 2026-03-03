import mysql.connector
from flask import Flask          # aita case sensitive, protom Flask f then F for senond flask.

app = Flask(__name__)            # flak object . flask bujthe pare ata main program.

Database = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12818572",
    password="22KvcK1UbY",          #Database collected from freesqldatabase.com (Size 5 MB)
    database="sql12818572",   
    port=3306
)



print("Database connected")

cursor = Database.cursor()                    #SQL query chalanur jonno cursor object toiri kora hoy, jeta dea command pathay database a.
cursor.execute("SELECT * FROM Students_info") #Temporary table create kora hoiche database a.
result = cursor.fetchall()
for row in result:
    print(row)





@app.route('/')                                ##browser a kau /(homepage) a gale kaun function cholbe seta bole dey.
def home():
    return "Welcome to the Home Page"



@app.route('/Login')                       # same ager motho /Login a gale bole dey .
def login():
    return "Welcome to the Login Page"

if __name__ == '__main__':
    app.run(debug=True, port=8000)       #debug true dile code a kono change korle server auto restart hoye jabe.

cursor.close()  
Database.close()                            
