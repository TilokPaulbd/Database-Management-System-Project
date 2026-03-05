import mysql.connector
from flask import Flask, redirect ,render_template, request, url_for         # aita case sensitive, protom Flask f then F for senond flask. 
                                                 #render_template aita html file ke render korar jonno use kora hoy.
                                                 

app = Flask(__name__,template_folder='tamplates')            # flak object . flask bujthe pare ata main program.
                                                            # tamplates folder na bole dile error dey . tample folder pay na.

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
    return render_template('home_page.html')             








@app.route('/Login',methods=['GET', 'POST'])                       # same ager motho /Login a jabe bole dey .
def login():
    if request.method == 'POST':                      # jodi form a data pathano hoy tahole post method use hobe.
        
        # data collect korchi user thake
        student_id = request.form['student_id']      # form a student_id name dea input theke data neya hoy.
        student_password = request.form['student_password']         
     
        #data check korbo database er table er sathe
        cursor.execute("SELECT student_name FROM Students_info WHERE student_id = %s AND student_password = %s", (student_id, student_password))  # SQL query chalanur jonno cursor object use
        result = cursor.fetchone()                   # fetchone() method use kore query er prothom result ta neya hoy.
        print(result)
        
        #akhon compare korbo
        if result:                                  # jodi result thake tahole mane data match koreche.
            # seat booking page a niye jabo 
            return render_template('student_Seat_Booking_page.html', student_name=result[0])  # seat booking page a niye jabo and student name o pathabo.
        else:
            return "Invalid student ID or password."  # jodi data match na kore tahole invalid message deya hoy.
        
    return render_template('student_login_page.html')         








@app.route('/Register',methods=['GET', 'POST'])                       
def register():
    if request.method == 'POST':                     
        
        
        student_id = request.form['student_id']  
        student_name = request.form['student_name']    
        student_password = request.form['student_password']         
     
        cursor.execute("INSERT INTO Students_info (student_id, student_name, student_password) values (%s, %s, %s)", (student_id, student_name, student_password))  
        Database.commit()                          # database a change korar por commit korte hoy.    
        
        #akhon login page a niye jabo
        return render_template('student_login_page.html') 
     
        
    return render_template('student_registration_page.html') 









@app.route('/BookSeat', methods=['GET', 'POST'])
def book_seat():
    if request.method == 'POST':
        student_name = request.form['student_name']
        buss_seat = request.form['buss_seat']

        
        return "Seat booked successfully!" + f" Student Name: {student_name}, Seat Number: {buss_seat}" #f-string হলো Python string, যার মধ্যে {} ব্যবহার করে variable বা expression সরাসরি embed করা যায়। 
    
    return render_template('student_Seat_Booking_page.html')
        








if __name__ == '__main__':
    app.run(debug=True, port=8000)       #debug true dile code a kono change korle server auto restart hoye jabe.

cursor.close()  
Database.close()                            
