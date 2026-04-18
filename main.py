import mysql.connector
from flask import Flask, redirect ,render_template, request, url_for         # aita case sensitive, protom Flask f then F for senond flask. 
                                                 #render_template aita html file ke render korar jonno use kora hoy.
                                                 

app = Flask(__name__,template_folder='tamplates')            # flak object . flask bujthe pare ata main program.
                                                            # tamplates folder na bole dile error dey . tample folder pay na.

Database = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12820369",
    password="nNeUhkAFRv",    #Database collected from freesqldatabase.com (Size 5 MB)
    database="sql12820369",   
    port=3306
)






print("Database connected")

cursor = Database.cursor()                    #SQL query chalanur jonno cursor object toiri kora hoy, jeta dea command pathay database a.
cursor.execute("SELECT * FROM Students") #Temporary table create kora hoiche database a.
result = cursor.fetchall()
for row in result:
    print(row)








@app.route('/')                                ##browser a kau /(homepage) a gale kaun function cholbe seta bole dey.
def home():
    return render_template('home_page.html')             






@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        student_id = request.form['student_id']
        student_password = request.form['student_password']

        cursor.execute("CALL student_login(%s, %s)", (student_id, student_password))
        data = cursor.fetchone()

        if data:
            return render_template(
                'student_Seat_Booking_page.html',
                student_name=data[0],
                student_id=data[1]
            )
        else:
            return "Invalid student ID or password."

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
        student_id = request.form['student_id']
        buss_seat = request.form['buss_seat']
        
        #akhon  Bookseats table a data insert korbo
        buss_id=1
        student_id=student_id
        cursor.execute("INSERT INTO Bookseats (buss_seat,buss_id ,student_id) VALUES (%s, %s, %s)", (buss_seat, buss_id, student_id))
        Database.commit()

        return "Seat booked successfully!" + f" Student Name: {student_name}, Student ID: {student_id}, Seat Number: {buss_seat}" #f-string হলো Python string, যার মধ্যে {} ব্যবহার করে variable বা expression সরাসরি embed করা যায়। 
    
    return render_template('student_Seat_Booking_page.html')
        






@app.route('/Admin',methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        admin_password = request.form['admin_password']
        
        cursor.execute("SELECT * FROM Admin_info WHERE admin_id = %s AND admin_password = %s", (admin_id, admin_password))
        result = cursor.fetchone()
        
        if result:
            return "Welcome, Admin"
        else:
            return "Invalid admin ID or password."
    
    return render_template('admin_login_page.html')





if __name__ == '__main__':
    app.run(debug=True, port=8000)     

cursor.close()  
Database.close()                            
