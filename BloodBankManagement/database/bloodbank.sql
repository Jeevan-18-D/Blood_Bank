CREATE DATABASE IF NOT EXISTS bloodbank;

USE bloodbank;


CREATE TABLE hospital (
    hospital_id INT AUTO_INCREMENT PRIMARY KEY,
    hospital_name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    address VARCHAR(255),
    phone VARCHAR(15)
);


CREATE TABLE donor (
    donor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(10),
    blood_group VARCHAR(5) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100),
    address VARCHAR(255)
);


CREATE TABLE receiver (
    receiver_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(10),
    blood_group_required VARCHAR(5) NOT NULL,
    phone VARCHAR(15),
    address VARCHAR(255),
    hospital_id INT,

    FOREIGN KEY (hospital_id)
    REFERENCES hospital(hospital_id)
    ON DELETE SET NULL
);


CREATE TABLE employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100),
    shift VARCHAR(30),
    hospital_id INT,

    FOREIGN KEY (hospital_id)
    REFERENCES hospital(hospital_id)
    ON DELETE SET NULL
);


CREATE TABLE blood_stock (
    stock_id INT AUTO_INCREMENT PRIMARY KEY,
    blood_group VARCHAR(5) NOT NULL UNIQUE,
    available_units INT DEFAULT 0
);


CREATE TABLE donation (
    donation_id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    units INT DEFAULT 1,
    donation_date DATE,

    FOREIGN KEY (donor_id)
    REFERENCES donor(donor_id)
    ON DELETE CASCADE
);


CREATE TABLE blood_request (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    receiver_id INT NOT NULL,
    hospital_id INT,
    blood_group VARCHAR(5) NOT NULL,
    units_required INT NOT NULL,
    request_date DATE,
    status VARCHAR(20) DEFAULT 'Pending',

    FOREIGN KEY (receiver_id)
    REFERENCES receiver(receiver_id)
    ON DELETE CASCADE,

    FOREIGN KEY (hospital_id)
    REFERENCES hospital(hospital_id)
    ON DELETE SET NULL
);


INSERT INTO hospital
(hospital_name, city, address, phone)
VALUES
('Apollo Hospital', 'Chennai', 'Greams Road', '04428293333'),
('Government Hospital', 'Chennai', 'Park Town', '04425305000'),
('MIOT International', 'Chennai', 'Manapakkam', '04442002288');


INSERT INTO donor
(name, age, gender, blood_group, phone, email, address)
VALUES
('Arun Kumar', 22, 'Male', 'O+', '9876543210', 'arun@gmail.com', 'Chennai'),
('Rahul', 24, 'Male', 'A+', '9876543211', 'rahul@gmail.com', 'Tambaram'),
('Priya', 21, 'Female', 'B+', '9876543212', 'priya@gmail.com', 'Chennai'),
('Karthik', 25, 'Male', 'AB+', '9876543213', 'karthik@gmail.com', 'Chengalpattu'),
('Divya', 23, 'Female', 'O-', '9876543214', 'divya@gmail.com', 'Chennai');


INSERT INTO receiver
(name, age, gender, blood_group_required, phone, address, hospital_id)
VALUES
('Ramesh', 45, 'Male', 'O+', '9876500001', 'Chennai', 1),
('Suresh', 38, 'Male', 'A+', '9876500002', 'Tambaram', 2),
('Lakshmi', 30, 'Female', 'B+', '9876500003', 'Chennai', 1);


INSERT INTO employee
(name, role, phone, email, shift, hospital_id)
VALUES
('Meena', 'Nurse', '9876511111', 'meena@gmail.com', 'Morning', 1),
('Anitha', 'Nurse', '9876511112', 'anitha@gmail.com', 'Evening', 2),
('Kumar', 'Staff', '9876511113', 'kumar@gmail.com', 'Morning', 1),
('Vijay', 'Staff', '9876511114', 'vijay@gmail.com', 'Night', 3);


INSERT INTO blood_stock
(blood_group, available_units)
VALUES
('A+', 20),
('A-', 8),
('B+', 15),
('B-', 5),
('AB+', 10),
('AB-', 3),
('O+', 25),
('O-', 4);


INSERT INTO donation
(donor_id, blood_group, units, donation_date)
VALUES
(1, 'O+', 1, '2026-08-20'),
(2, 'A+', 1, '2026-08-21'),
(3, 'B+', 1, '2026-08-22'),
(4, 'AB+', 1, '2026-08-23'),
(5, 'O-', 1, '2026-08-24');


INSERT INTO blood_request
(receiver_id, hospital_id, blood_group,
units_required, request_date, status)
VALUES
(1, 1, 'O+', 2, '2026-09-01', 'Pending'),
(2, 2, 'A+', 1, '2026-09-02', 'Approved'),
(3, 1, 'B+', 2, '2026-09-03', 'Pending');
