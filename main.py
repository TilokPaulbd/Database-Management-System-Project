import mysql.connector # MySQL database connect korar jonno import kori
from flask import Flask, redirect ,render_template, request, url_for,jsonify

#flask holo toolbox . Flask holo toolbox er main tool
#render_template, request, url_for - ei gulo holo flask er built in functions 
#jsonify - data ke json format e convert kora. amra available seats er data ke json format e convert kore frontend e pataichi

app = Flask(__name__,template_folder='tamplates')
#aita ekta remote er motho  TV (app) start kore ar bole dey kun folder kun channels (HTML pages) dekhabe           
                                                            
Database = mysql.connector.connect( #amader full database ta aitar vitore load kora hoiche
    host="sql12.freesqldatabase.com",
    user="sql12820369",
    password="nNeUhkAFRv",    #Database collected from freesqldatabase.com (Size 5 MB)
    database="sql12820369",   
    port=3306
)

cursor = Database.cursor()     #databse a query chalnur jonno use korchi.  databse ekta library hole cursor holo librarian je query gulo database er vitore niye jabe ar result niye asbe.           












@app.route('/')                   #browser a kau /(homepage) a gale kaun function cholbe seta bole dey.
def home():                        #app er niche jai function thakbe oi link a gale oi function cholbe.
    return render_template('home_page.html')             
#render_template dea html file load kore .






@app.route('/login', methods=['GET', 'POST'])  # Get method a data url a thake ar POST method a data form er vitore thake. amra POST method ai use kori aita safe bashi.
def login():
    if request.method == 'POST':

        student_id_input = request.form['student_id'] #request.form dea html er vitor er input form er data niye aschi.
        student_password = request.form['student_password']

        cursor.callproc('student_login', (student_id_input, student_password)) #database er kaj korar jonno cursor ar callproc dea procedure call kori.
        
        result = None
        for res in cursor.stored_results():           #stored_results() holo built-in method jaita procedure thake asha data collect kore
            result = res.fetchall()                   #fetchall all row          #jodio ek set result ashbe tobuo procedure theke multiple result ashle jathe crush na hoy tai for loop dea result collect kori . standard way
                                                       
        if result and len(result) > 0:
            return redirect(url_for('student_dashboard', student_id=student_id_input )) # render taplate a sudhu oi page ta load korbe .redirect a oi url a nea jabe rote exicute korbe. 
        else:
            return redirect(url_for('login'))

    return render_template('student_login_page.html')





@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        student_id = request.form['student_id']
        student_name = request.form['student_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        cursor.callproc('student_signup', (student_id,student_name,email,phone,password))

        for result in cursor.stored_results():
            result.fetchall()

        Database.commit()       #database a parmanently save or chnage korar jonno commit korthe hoy

        return redirect(url_for('login')) 

    return render_template('student_signup_page.html')




@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':

        admin_id = request.form['admin_id']
        admin_password = request.form['admin_password']

        cursor.callproc('admin_login', (admin_id, admin_password))

        result = None

        for res in cursor.stored_results():
            result = res.fetchall()   

        if result and len(result) > 0:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('home'))

    return render_template('admin_login_page.html')























#aitay get deai data nichi karon post dea nithe gale session ad kora lage key add kora lage .tarpor output dey tai tai get deai nea nichi.


@app.route('/student_dashboard')
def student_dashboard():

    student_id_input = request.args.get('student_id') # get dea url thakei data nichi.

    if not student_id_input:
        return "Student ID missing"

    cursor = Database.cursor()

   
    cursor.callproc('show_student_details_by_id', (student_id_input,))
    student = cursor.stored_results().__next__().fetchall()[0]     #__next__() aita dea protom ta ar ektai result set ney.


    cursor.callproc('get_student_travel_logs', (student_id_input,))
    results = cursor.stored_results()   # ai procedure thake 2 set result ashe protom ta thake details ,second ta thake count aita .set set na nile procedure kothin hoia jatho

    logs = next(results).fetchall()#next dea result gulare serialy nea aschi            
    denied_count = next(results).fetchall()[0][0]     #fetchall sob somoy list return kore tai [0][0] dea first row ar first column      

    semester_id = request.args.get('semester_id', 261) #default value 261

    cursor.callproc('search_payment', (student_id_input, semester_id))
    payment_results = cursor.stored_results()

    payments = []
    result = list(payment_results)
    if len(result) > 0:
        payments = result[0].fetchall()

    return render_template('student_dashboard.html',student_id=student[0],student_name=student[1],email=student[2],phone=student[3],logs=logs,denied_count=denied_count,payments=payments,semester_id=semester_id)




@app.route('/booking_page')
def booking_page():
    student_id = request.args.get('student_id')

    return render_template("booking.html", student_id=student_id)














@app.route('/get_schedules_by_date')
def get_schedules_by_date():

    date = request.args.get('date')

    cursor = Database.cursor()
    cursor.callproc('get_schedules_by_date', (date,))

    result = cursor.stored_results().__next__().fetchall()

    schedules = []
    for r in result:
        schedules.append({             #append dea data insert kori.
            "bus_schedule_id": r[0],
            "schedule_id": r[1],
            "start_destination": r[2],
            "end_destination": r[3],
            "start_time": str(r[4]),
            "end_time": str(r[5]),
            "bus_id": r[6]
        })

    return jsonify(schedules) #backend a list a data rakhle problem nai kintu frontend a json format a nithe hobe jodi sob data indevidualy kaj koraithe chai .frontend a python buje na.






@app.route('/get_available_seats_by_schedule')
def get_available_seats_by_schedule():

    bus_schedule_id = request.args.get('bus_schedule_id')

    cursor = Database.cursor()
    cursor.callproc('show_available_seats_by_schedule', (bus_schedule_id,))

    result = cursor.stored_results().__next__().fetchall()

    seats = []
    for r in result:
        seats.append({
            "seat_id": r[0],
            "seat_number": r[1]
        })

    return jsonify(seats)








@app.route('/get_available_seats')
def get_available_seats():

    bus_id = request.args.get('bus_id')

    cursor = Database.cursor()
    cursor.callproc('show_available_seats', (bus_id,))

    result = cursor.stored_results().__next__().fetchall()

    seats = []
    for r in result:
        seats.append({
            "seat_id": r[0],
            "seat_number": r[1],
            "bus_id": r[2]
        })

    return jsonify(seats)







@app.route('/booking_seat')
def booking_seat():

    date = request.args.get('date')
    bus_schedule_id = request.args.get('bus_schedule_id')
    bus_id = request.args.get('bus_id')
    student_id = request.args.get('student_id')  

    return render_template("booking_seat.html",student_id=student_id,bus_schedule_id=bus_schedule_id,bus_id=bus_id,date=date)





@app.route('/add_booking', methods=['POST'])
def add_booking():

    cursor = Database.cursor()

    student_id = request.form['student_id']
    bus_schedule_id = request.form['bus_schedule_id']
    seat_id = request.form['seat_id']

    cursor.callproc('add_booking', (student_id, bus_schedule_id, seat_id))
    Database.commit()

    cursor.callproc('get_latest_booking_id', (student_id,))

    result = cursor.stored_results().__next__().fetchall()
    booking_id = result[0][0]

    cursor.callproc('add_travel_status_with_log', (booking_id, "CONFIRMED")) #deafult status CONFIRMED
    Database.commit()

    return redirect(url_for('confirm_booking',student_id=student_id,bus_schedule_id=bus_schedule_id,seat_id=seat_id))






@app.route('/confirm_booking')
def confirm_booking():

    student_id = request.args.get('student_id')
    bus_schedule_id = request.args.get('bus_schedule_id')
    seat_id = request.args.get('seat_id')

    return render_template("confirm_booking.html",student_id=student_id,bus_schedule_id=bus_schedule_id,seat_id=seat_id)

@app.route('/logout')
def logout():
    return redirect(url_for('home'))







































@app.route('/admin_dashboard')
def admin_dashboard():

    cursor.execute("SELECT * FROM journey_view")
    journeys = cursor.fetchall()

    cursor.execute("SELECT * FROM routes_view")
    routes = cursor.fetchall()

    cursor.execute("SELECT * FROM buses_view")
    buses = cursor.fetchall()

    cursor.execute("SELECT * FROM schedules_view")
    schedules = cursor.fetchall()

    cursor.execute("SELECT * FROM bus_schedules_view")
    bus_schedules = cursor.fetchall()

    cursor.execute("SELECT * FROM semesters_view")
    semesters = cursor.fetchall()

    cursor.execute("SELECT * FROM view_all_payments")
    payments = cursor.fetchall()

    return render_template('admin_dashboard.html',journeys=journeys,routes=routes,buses=buses,schedules=schedules,bus_schedules=bus_schedules,semesters=semesters,payments=payments)
   
   
   
   
   
   
   
   
   
   
    
@app.route('/update_travel_status', methods=['POST'])
def update_travel_status():
    cursor = Database.cursor()

    booking_id = request.form['booking_id']
    status = request.form['status']

    cursor.callproc('update_travel_status', (booking_id, status))

    Database.commit()

    return redirect(url_for('missing_checking'))









@app.route('/search_payment', methods=['POST'])
def search_payment():

    student_id = request.form['student_id']
    semester_id = request.form['semester_id']

    cursor.callproc('search_payment', [student_id, semester_id])

    result = []
    for res in cursor.stored_results():
        result = res.fetchall()

    return render_template("admin_dashboard.html",search_payments=result)
    
    
    
    
    
    
    

@app.route('/add_semester', methods=['POST'])
def add_semester():
    sid = request.form['semester_id']
    sname = request.form['semester_name']

    cursor.execute("CALL add_semester(%s, %s)", (sid, sname))
    Database.commit()

    return redirect('/admin_dashboard')




@app.route('/add_payment', methods=['POST'])
def add_payment():
    pid = request.form['payment_id']
    student_id = request.form['student_id']
    semester_id = request.form['semester_id']
    status = request.form['payment_status']

    cursor.execute("CALL add_payment(%s, %s, %s, %s)",
                   (pid, student_id, semester_id, status))
    Database.commit()

    return redirect('/admin_dashboard')




@app.route('/add_route', methods=['POST'])
def add_route():

    r_id = request.form['r_id']
    r_start = request.form['r_start']
    r_end = request.form['r_end']

    cursor.callproc('add_route', (r_id, r_start, r_end))
    Database.commit()

    return redirect(url_for('admin_dashboard'))





@app.route('/add_bus', methods=['POST'])
def add_bus():

    b_id = request.form['b_id']
    b_name = request.form['b_name']

    cursor.callproc('add_bus_with_seats', (b_id, b_name))
    Database.commit()

    return redirect(url_for('admin_dashboard'))





@app.route('/add_schedule', methods=['POST'])
def add_schedule():

    s_id = request.form['s_id']
    r_id = request.form['r_id']
    j_date = request.form['j_date']
    s_time = request.form['s_time']
    e_time = request.form['e_time']

    cursor.callproc('add_schedule', (s_id, r_id, j_date, s_time, e_time))
    Database.commit()

    return redirect(url_for('admin_dashboard'))

@app.route('/assign_bus_schedule', methods=['POST'])
def assign_bus_schedule():

    bs_id = request.form['bs_id']
    b_id = request.form['b_id']
    s_id = request.form['s_id']

    cursor.callproc('assign_bus_schedule', (bs_id, b_id, s_id))
    Database.commit()

    return redirect(url_for('admin_dashboard'))









@app.route('/view_booking_by_bus_schedule', methods=['GET', 'POST'])
def view_booking_by_bus_schedule():

    bus_schedule_id = request.values.get('bus_schedule_id')
    result = []

    if bus_schedule_id:
        cursor.callproc('view_booking_by_bus_schedule', [bus_schedule_id])

        for res in cursor.stored_results():
            result = res.fetchall()

    return render_template("missing_checking.html",   bookings=result,bus_schedule_id=bus_schedule_id,active_section="booking_result")









@app.route('/missing_checking.html')
def missing_checking():
    cursor = Database.cursor()

    bus_schedule_id = request.args.get('bus_schedule_id')

    if bus_schedule_id is None or bus_schedule_id == "":
        bus_schedule_id = 0
    else:
        bus_schedule_id = int(bus_schedule_id)        #type cast korchi aikhane.

    cursor.callproc('view_booking_by_bus_schedule', [bus_schedule_id])

    bookings = []
    for result in cursor.stored_results():
        bookings = result.fetchall()

    return render_template("missing_checking.html",bookings=bookings,bus_schedule_id=bus_schedule_id)






if __name__ == '__main__':
    app.run(debug=True, port=8000)     

cursor.close()  
Database.close()                            
