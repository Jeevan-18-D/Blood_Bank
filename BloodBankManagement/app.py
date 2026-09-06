from flask import Flask, render_template, request, jsonify
from flask_mysql_connector import MySQL

app = Flask(__name__)

# DATABASE CONNECTION
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DATABASE'] = 'bloodbank'

mysql = MySQL(app)


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# DASHBOARD
@app.route('/dashboard')
def dashboard():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM donor")
    donors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM receiver")
    receivers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM hospital")
    hospitals = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(available_units), 0)
        FROM blood_stock
    """)
    blood_units = cursor.fetchone()[0]

    cursor.close()

    return jsonify({
        "donors": donors,
        "receivers": receivers,
        "hospitals": hospitals,
        "blood_units": blood_units
    })


# GET DONORS
@app.route('/donors', methods=['GET'])
def get_donors():
    cursor = mysql.connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM donor
        ORDER BY donor_id DESC
    """)

    donors = cursor.fetchall()
    cursor.close()

    return jsonify(donors)


# ADD DONOR
@app.route('/donors', methods=['POST'])
def add_donor():
    data = request.get_json()

    cursor = mysql.connection.cursor()

    query = """
        INSERT INTO donor
        (name, age, gender, blood_group, phone, email, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data['name'],
        data['age'],
        data['gender'],
        data['blood_group'],
        data['phone'],
        data['email'],
        data['address']
    )

    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Donor added successfully"})


# DELETE DONOR
@app.route('/donors/<int:id>', methods=['DELETE'])
def delete_donor(id):
    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM donor WHERE donor_id = %s",
        (id,)
    )

    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Donor deleted successfully"})


# GET RECEIVERS
@app.route('/receivers')
def get_receivers():
    cursor = mysql.connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.receiver_id,
               r.name,
               r.age,
               r.gender,
               r.blood_group_required,
               r.phone,
               r.address,
               h.hospital_name
        FROM receiver r
        LEFT JOIN hospital h
        ON r.hospital_id = h.hospital_id
        ORDER BY r.receiver_id DESC
    """)

    receivers = cursor.fetchall()
    cursor.close()

    return jsonify(receivers)


# GET BLOOD STOCK
@app.route('/bloodstock')
def get_blood_stock():
    cursor = mysql.connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM blood_stock
        ORDER BY blood_group
    """)

    stock = cursor.fetchall()
    cursor.close()

    return jsonify(stock)


# GET HOSPITALS
@app.route('/hospitals')
def get_hospitals():
    cursor = mysql.connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM hospital
        ORDER BY hospital_id DESC
    """)

    hospitals = cursor.fetchall()
    cursor.close()

    return jsonify(hospitals)


# GET EMPLOYEES
@app.route('/employees')
def get_employees():
    cursor = mysql.connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT e.employee_id,
               e.name,
               e.role,
               e.phone,
               e.email,
               e.shift,
               h.hospital_name
        FROM employee e
        LEFT JOIN hospital h
        ON e.hospital_id = h.hospital_id
        ORDER BY e.employee_id DESC
    """)

    employees = cursor.fetchall()
    cursor.close()

    return jsonify(employees)


# GET BLOOD REQUESTS
@app.route('/requests')
def get_requests():
    cursor = mysql.connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT br.request_id,
               r.name AS receiver_name,
               h.hospital_name,
               br.blood_group,
               br.units_required,
               br.status,
               br.request_date
        FROM blood_request br
        LEFT JOIN receiver r
        ON br.receiver_id = r.receiver_id
        LEFT JOIN hospital h
        ON br.hospital_id = h.hospital_id
        ORDER BY br.request_id DESC
    """)

    requests_data = cursor.fetchall()
    cursor.close()

    return jsonify(requests_data)


# APPROVE BLOOD REQUEST
@app.route('/requests/<int:id>/approve', methods=['PUT'])
def approve_request(id):

    cursor = mysql.connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT blood_group, units_required, status
        FROM blood_request
        WHERE request_id = %s
    """, (id,))

    request_data = cursor.fetchone()

    if request_data is None:
        cursor.close()
        return jsonify({"message": "Request not found"}), 404

    if request_data['status'] == 'Approved':
        cursor.close()
        return jsonify({"message": "Request already approved"})

    cursor.execute("""
        SELECT available_units
        FROM blood_stock
        WHERE blood_group = %s
    """, (request_data['blood_group'],))

    stock = cursor.fetchone()

    if stock is None:
        cursor.close()
        return jsonify({"message": "Blood group not found"})

    if stock['available_units'] < request_data['units_required']:
        cursor.close()
        return jsonify({"message": "Not enough blood available"})

    cursor.execute("""
        UPDATE blood_stock
        SET available_units = available_units - %s
        WHERE blood_group = %s
    """, (
        request_data['units_required'],
        request_data['blood_group']
    ))

    cursor.execute("""
        UPDATE blood_request
        SET status = 'Approved'
        WHERE request_id = %s
    """, (id,))

    mysql.connection.commit()
    cursor.close()

    return jsonify({
        "message": "Blood request approved successfully"
    })


if __name__ == '__main__':
    app.run(debug=True)
