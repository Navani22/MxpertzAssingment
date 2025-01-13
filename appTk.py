from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Nh@2218#0112',
    'database': 'work1'
}

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return redirect(url_for('employee'))

@app.route('/employee', methods=['POST','GET'])
def employee():
    pass
    return render_template("employee.html")

@app.route('/createemployee', methods=['GET','POST'])
def createemployee():
    if request.method == 'POST':
        # Get form data
        name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        salary = request.form['salary']
        gender = request.form['gender']


        # Save user data to the database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO employeetable (name, email, phone, department,salary, gender)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, phone, department,salary, gender))
            conn.commit()
            return redirect(url_for('employeedisplay'))
        # except Exception as e:
        #     return redirect(url_for('createemployee'))
        finally:
            cursor.close()
            conn.close()

    return render_template('addemployee.html')

@app.route('/employeedisplay', methods=['GET'])
def employeedisplay():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * from employeetable")
    employees=cursor.fetchall()        

    return render_template('employeedisplay.html', 
    employees=employees)

@app.route('/edit/<int:employee_id>', methods=['GET','POST'])
def edit_employee(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method=='POST':
        name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        salary = request.form['salary']
        gender = request.form['gender']
        
        cursor.execute("""UPDATE employeetable SET name=%s, email=%s, phone=%s, department=%s,salary=%s, gender=%s WHERE id=%s""",
                       (name, email, phone, department,salary, gender,employee_id))
        conn.commit()
    
    return redirect(url_for('employeedisplay'))
    
    cursor.execute("SELECT * from employeetable WHERE id=%s", (employee_id),)
    employee=cursor.fetchone()

    return render_template('edit_employee.html', 
                           employee=employee)

@app.route('/delete/<int:employee_id>', methods=['GET'])
def delete_employee(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employeetable WHERE id=%s", (employee_id,))
    conn.commit()

    return redirect(url_for('employeedisplay'))

if __name__ == '__main__':
    app.run(debug=True)
