------ SPECIALTY ----------------
-- Create the specialty table
CREATE TABLE specialty (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  description TEXT
);

-- Insert dummy data into specialty table
INSERT INTO specialty (name, description)
VALUES ('Cardiology',        'Cardiology is the branch of medicine that deals with the study, diagnosis, and treatment of heart disorders.'),
       ('Internal Medicine', 'Internal medicine is the medical specialty dealing with the prevention, diagnosis, and treatment of adult diseases.'),
       ('Pneumology',        'Pulmonology is a medical specialty that deals with diseases involving the respiratory tract.');


------ DOCTORS ------------------
-- Create the doctors table
CREATE TABLE doctors (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  specialty INTEGER REFERENCES specialty (id),
  profile_picture VARCHAR(255),
  personal_statement TEXT,
  date_added TIMESTAMP NOT NULL DEFAULT NOW(),
  date_modified TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Insert dummy data into doctors table
INSERT INTO doctors (first_name, last_name, specialty, profile_picture, personal_statement)
VALUES ('John',  'Smith',   1, 'gs://health-app/img/profile_pics/john_smith.jpg',   'I am a board-certified cardiologist with over 10 years of experience.'),
       ('Sara',  'Johnson', 2, 'gs://health-app/img/profile_pics/sara_johnson.jpg', 'I am an internist with a passion for preventative medicine and patient education.'),
       ('David', 'Lee',     3, 'gs://health-app/img/profile_pics/david_lee.jpg',    'I specialize in the diagnosis and treatment of lung diseases, including asthma, COPD, and lung cancer.');


------ PATIENTS -----------------
-- Create the patients table
CREATE TABLE patients (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(255),
  phone_number VARCHAR(20),
  date_of_birth DATE,
  date_added TIMESTAMP NOT NULL DEFAULT NOW(),
  date_modified TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Insert dummy data into patients table
INSERT INTO patients (first_name, last_name, email, phone_number, date_of_birth)
VALUES ('Alice',  'Johnson', 'alice.johnson@example.com', '555-1234', '1990-05-20'),
       ('Bob',     'Smith',  'bob.smith@example.com',     '555-5678', '1985-09-12'),
       ('Charlie', 'Wong',   'charlie.wong@example.com',  '555-9012', '1977-12-01');


------ SHIFT --------------------
-- Create the shift table
CREATE TABLE shift (
  id SERIAL PRIMARY KEY,
  doctor_id INTEGER REFERENCES doctors (id),
  start_time TIMESTAMP,
  end_time TIMESTAMP,
);


------ APPOINTMENTS -------------
-- Create the appointments table
CREATE TABLE appointments (
  id SERIAL PRIMARY KEY,
  doctor_id INTEGER REFERENCES doctors (id),
  patient_id INTEGER REFERENCES patients (id),
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  duration INTEGER,
  status VARCHAR(20)
);