#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
#-------------------------------------------------------------------------------
Project		: Health API
Module		: main
Purpose   	: API for medical app
Source		: https://github.com/buraktokman/Health-API
Version		: 0.1.0 beta
Status 		: Development

Modified	: 2023 Apr 1
Created   	: 2023 Mar 29
Author		: Burak Tokman
Email 		: buraktokman@hotmail.com
#-------------------------------------------------------------------------------
'''
import logging
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, extract, func
from datetime import datetime, date, time, timedelta

import src.settings as settings


# ------ LOGGER -----------------
logger = logging.getLogger('API')
# logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s [%(name)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


# ------ SETUP ------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%s:%s@%s/%s' % (
    settings.SQL_USERNAME, settings.SQL_PASSWORD, settings.SQL_HOSTNAME, settings.SQL_DATABASE)
db = SQLAlchemy(app)


# ------ ORM --------------------
class Doctor(db.Model):
    __tablename__   = settings.SQL_DOCTORS_TABLE
    id              = db.Column(db.Integer, primary_key=True)
    first_name      = db.Column(db.String(50), nullable=False)
    last_name       = db.Column(db.String(50), nullable=False)
    specialty       = db.Column(db.Integer, db.ForeignKey('specialty.id'), nullable=False)
    # specialty_name  = db.relationship('Specialty', backref=db.backref('doctors', lazy=True))
    profile_picture = db.Column(db.String(200), nullable=True)
    personal_statement = db.Column(db.Text(), nullable=True)
    date_added      = db.Column(db.DateTime(), default=datetime.utcnow)
    date_modified   = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, first_name, last_name, specialty, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.specialty = specialty
        # Optional fields
        if 'profile_picture' in kwargs:     self.profile_picture = kwargs['profile_picture']
        if 'personal_statement' in kwargs:  self.personal_statement = kwargs['personal_statement']
    
    def serialize(self):
        return {
            'id':               self.id,
            'first_name':       self.first_name,
            'last_name':        self.last_name,
            'specialty_id':     self.specialty,
            # 'specialty_name':   self.specialty_name if self.specialty else None,
            'profile_picture':  self.profile_picture,
            'personal_statement': self.personal_statement,
            'date_added':       self.date_added.isoformat(),
            'date_modified':    self.date_modified.isoformat()
        }

class Specialty(db.Model):
    __tablename__   = settings.SQL_SPECIALTY_TABLE
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(50), nullable=False)
    description     = db.Column(db.Text(), nullable=True)

    def serialize(self):
        return {
            'id':           self.id,
            'name':         self.name,
            'description':  self.description
        }

class Shift(db.Model):
    __tablename__   = settings.SQL_SHIFTS_TABLE
    id              = db.Column(db.Integer, primary_key=True)
    doctor_id       = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    start_time      = db.Column(db.DateTime, nullable=False)
    end_time        = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        return {
            'id':           self.id,
            'doctor_id':    self.doctor_id,
            # Note: Convert date objects to strings since they are not JSON serializable.
            #       e.g. datetime.datetime(2020, 1, 1, 0, 0) -> '2020-01-01T00:00:00'
            'start_time':   self.start_time.isoformat(),
            'end_time':     self.end_time.isoformat(),
        }

class Appointment(db.Model):
    __tablename__   = settings.SQL_APPOINTMENTS_TABLE
    id              = db.Column(db.Integer, primary_key=True)
    doctor_id       = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id      = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    start_time      = db.Column(db.DateTime(), nullable=False)
    end_time        = db.Column(db.DateTime(), nullable=False)

    def serialize(self):
        return {
            'id':           self.id,
            'doctor_id':    self.doctor_id,
            'patient_id':   self.patient_id,
            'start_time':   self.start_time.isoformat(),
            'end_time':     self.end_time.isoformat(),
        }

class Patient(db.Model):
    __tablename__   = settings.SQL_PATIENTS_TABLE
    id              = db.Column(db.Integer, primary_key=True)
    first_name      = db.Column(db.String(50), nullable=False)
    last_name       = db.Column(db.String(50), nullable=False)
    email           = db.Column(db.String(120), unique=True, nullable=False)
    phone_number    = db.Column(db.String(20), nullable=False)
    date_of_birth   = db.Column(db.Date, nullable=False)
    date_added      = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # def serialize(self):
    #     """ TODO: Test this method!
    #     """
    #     return {
    #         'id':               self.id,
    #         'first_name':       self.first_name,
    #         'last_name':        self.last_name,
    #         'email':            self.email,
    #         'phone_number':     self.phone_number,
    #         'date_of_birth':    self.date_of_birth.isoformat(),
    #         'date_added':       self.date_added.isoformat(),
    #         'date_modified':    self.date_modified.isoformat()
    #     }


# ------ DOCTORS ----------------
@app.route('/doctors', methods=['GET'])
@app.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctors(doctor_id=None):
    """ Endpoint to find doctors

        Route:
            - /doctors
            - /doctors/<int:doctor_id>
        Method:
            - GET
        Params:
            - limit (int): number of doctors to return
                - Required: Optional
            - specialty (str): specialty of the doctor
                - Required: Optional
                - Exammple: "/doctors?specialty=Cardiology"
            - first_name (str): first name of the doctor
                - Required: Optional
            - last_name (str): last name of the doctor
                - Required: Optional
        Returns:
            (json): list of doctors
                e.g. [{
                        "id": 1,
                        "first_name": "John",
                        "last_name": "Smith",
                        "specialty_id": 1,
                        "specialty_name": "Cardiology",
                        "profile_picture": "gs://health-app/img/profile_pics/john.jpg",
                        "personal_statement": "I am a cardiologist with 10 years of experience",
                        "date_added": "2021-03-29 12:00:00",
                        "date_modified": "2021-03-29 12:00:00"
                    }, ...]
    """
    # Get the parameters
    specialty   = request.args.get('specialty')
    first_name  = request.args.get('first_name')
    last_name   = request.args.get('last_name')
    limit       = request.args.get('limit')

    # TODO: add 'specialty_name' to the 'doctors' table to avoid joins
    # Join the tables to get the specialty name
    # doctors.specialty <-> specialty.id
    query = Doctor.query.join(Specialty, Doctor.specialty == Specialty.id)
    # Add specialty name to the query
    query = query.add_columns(Specialty.name.label('specialty_name'))

    # Order by random to be able to schedule an appointment
    # with a random doctor of the selected specialty.
    query = query.order_by(func.random())

    # Filter
    if doctor_id:   query = query.filter(Doctor.id == doctor_id)
    if first_name:  query = query.filter(Doctor.first_name.ilike(f'%{first_name}%'))
    if last_name:   query = query.filter(Doctor.last_name.ilike(f'%{last_name}%'))
    if specialty:   query = query.filter(Specialty.name.ilike(f'%{specialty}%'))
    # Limit
    if limit:       query = query.limit(limit)

    # Execute query
    doctors = query.all()
    results = []
    for doctor, specialty_name in doctors:
        r = {
            **doctor.serialize(),
            # Add the specialty name
            'specialty_name': specialty_name
        }
        results.append(r)
    # Return results
    return jsonify(results), 200


@app.route('/doctors', methods=['POST'])
def add_doctor():
    """ Endpoint to add a doctor

        Route:
            - /doctors
        Method:
            - POST
        Params:
            - first_name (str): first name of the doctor
                - Required: Yes
            - last_name (str): last name of the doctor
                - Required: Yes
            - specialty (str): specialty of the doctor
                - Required: Yes
            - profile_picture (str): profile picture of the doctor
                - Required: No
            - personal_statement (str): personal statement of the doctor
                - Required: No
        Returns:
            (json): message
                e.g. {'message': 'Doctor added successfully.'}
    """
    # Get the parameters
    first_name          = request.args.get('first_name')
    last_name           = request.args.get('last_name')
    specialty_name      = request.args.get('specialty')
    profile_picture     = request.args.get('profile_picture')
    personal_statement  = request.args.get('personal_statement')

    # Validate the data
    if not first_name or not last_name or not specialty_name:
        msg = {'message': 'Missing required fields.'}
        return jsonify(msg), 400

    #! DELTHIS
    logger.info('>> parameters >> first_name: %s, last_name: %s, specialty_name: %s, profile_picture: %s, personal_statement: %s',
        first_name, last_name, specialty_name, profile_picture, personal_statement)
    #! -----

    # Find the specialty id by the name from the 'Specialty' table
    specialty = Specialty.query.filter_by(name=specialty_name).first()
    if not specialty:
        msg = {'message': 'Specialty not found.'}
        return jsonify(), 400
    s = specialty.serialize()

    #! DELTHIS
    logger.info('>> specialty id >> %s', s['id'])
    #! -----

    # Create new Doctor
    doctor = Doctor(
        first_name=first_name,
        last_name=last_name,
        specialty=s['id'],
    )
    # Add optional fields
    if profile_picture:     doctor.profile_picture = profile_picture
    if personal_statement:  doctor.personal_statement = personal_statement

    # Insert into the table
    db.session.add(doctor)
    db.session.commit()

    # Return message
    msg = {'message': 'Doctor added successfully.', 'doctor_id': doctor.id}
    return jsonify(msg), 201


@app.route('/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    """ Endpoint to update a doctor

        Route:
            - /doctors/<doctor_id>
        Method:
            - PUT
        Params:
            - first_name (str): first name of the doctor
                - Required: No
            - last_name (str): last name of the doctor
                - Required: No
            - specialty (str): specialty of the doctor
                - Required: No
            - profile_picture (str): profile picture of the doctor
                - Required: No
            - personal_statement (str): personal statement of the doctor
        Returns:
            (json): message
                e.g. {'message': 'Doctor updated successfully.'}
    """
    # Get the doctor from the database
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        msg = {'message': 'Doctor not found.'}
        return jsonify(msg), 404

    # Get the parameters
    first_name          = request.args.get('first_name', doctor.first_name)
    last_name           = request.args.get('last_name', doctor.last_name)
    profile_picture     = request.args.get('profile_picture', doctor.profile_picture)
    personal_statement  = request.args.get('personal_statement', doctor.personal_statement)
    
    # Find the specility id by the name from the 'Specialty' table
    specialty           = request.args.get('specilty')
    if specialty:
        specialty = Specialty.query.filter_by(name=specialty).first()
        if not specialty:
            msg = {'message': 'Specialty not found.'}
            return jsonify(msg), 400
        specialty = specialty.id
    else:
        specialty = doctor.specialty

    # Update the doctor's details
    doctor.first_name         = first_name
    doctor.last_name          = last_name
    doctor.specialty          = specialty
    doctor.profile_picture    = profile_picture
    doctor.personal_statement = personal_statement

    # Save the changes to the database
    db.session.commit()

    # Return message
    msg = {'message': 'Doctor updated successfully.'}
    return jsonify(msg), 200


@app.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    """ Endpoint to delete a doctor

        Route:
            - /doctors/<doctor_id>
        Method:
            - DELETE
        Params:
            - doctor_id (int): id of the doctor
                - Required: True
        Returns:
            (json): message
                e.g. {'message': 'Doctor deleted successfully.'}
    """
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        # Delete from the database
        db.session.delete(doctor)
        db.session.commit()
        msg = {'message': 'Doctor deleted successfully'}
        return jsonify(msg), 200
    else:
        # Doctor not found!
        msg = {'error': 'Doctor not found'}
        return jsonify(msg), 404


@app.route('/doctors/<int:doctor_id>/availability', methods=['GET'])
def get_available_times(doctor_id):
    """ Endpoint to get available time ranges from a doctor to book an appointment.
        
        Route:
            - /doctors/<int:doctor_id>/available_times
        Method:
            - GET: returns a list of available time ranges
        Params:
            - start_date (date): start date to search for available time ranges
                - Required: GET
                - Example: 2023-04-01
            - end_date (date): end date to search for available time ranges
                - Required: GET
        Returns:
            (json): list of available time ranges for the doctor
                e.g. [["2023-04-01 09:00", "2023-04-01 10:30"],
                      ["2023-04-01 11:00", "2023-04-01 14:30"], ...] 
    """
    start_date = request.args.get('start_date')
    end_date   = request.args.get('end_date')

    # Check if the required fields are provided
    if not start_date or not end_date:
        msg = {'message': 'start_date and end_date are required'}
        return jsonify(msg), 400

    # Convert str to datetime
    #   e.g. 2023-04-01 00:00
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        # Add 1 day to the end date to include the end date
        #   e.g. 2023-04-01 00:00 to 2023-04-02 00:00
        end_date   = datetime.strptime(end_date, '%Y-%m-%d').date() + timedelta(days=1)
    except ValueError:
        msg = {'message': 'start_date and end_date should be in the format YYYY-MM-DD'}
        return jsonify(msg), 400

    # Check if the end date is after the start date
    if end_date < start_date:
        msg = {'message': 'end_date must be after start_date'}
        return jsonify(msg), 400

    # Check if the doctor exists
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        msg = {"error": "Doctor not found"}
        return jsonify(msg), 404

    # Get all shifts for the doctor within the date range
    shifts = Shift.query.filter(
            Shift.doctor_id == doctor_id,
            Shift.start_time >= start_date,
            Shift.end_time <= end_date
        ).all()
    #! DELTHIS
    logging.info('>> shifts: %s', len(shifts))
    #! ---

    # Get all appointments for the doctor within the date range
    appointments = Appointment.query.filter(
            Appointment.doctor_id  == doctor_id,
            Appointment.start_time >= start_date,
            Appointment.start_time <= end_date
        ).all()
    #! DELTHIS
    logging.info('>> appointments: %s', len(appointments))
    #! ---

    # Generate appointment ranges
    #   e.g. [(start_time, end_time), (2023-04-01 16:30, 2023-04-01 17:00), ...]
    appointment_ranges = [(appointment.start_time, appointment.end_time) for appointment in appointments]

    # Create a list of all possible time slots within the doctor's shifts
    possible_slots = []
    for shift in shifts:
        start_time = shift.start_time
        end_time = shift.end_time
        slot_start = start_time
        while slot_start < end_time:
            slot_end = slot_start + timedelta(minutes=15)
            if slot_end <= end_time:
                possible_slots.append((slot_start, slot_end))
            slot_start = slot_end

    # Remove the appointments from the possible time slots
    for appointment_range in appointment_ranges:
        possible_slots = [(start, end) for (start, end) in possible_slots if start >= appointment_range[1] or end <= appointment_range[0]]
    
    # TODO: Eliminate this stage if possible
    # Merge the time ranges that are next to each other
    #   e.g. before: [["2023-04-01 09:00", "2023-04-01 09:30"],
    #                 ["2023-04-01 09:30", "2023-04-01 10:00"]]
    #        after:  [["2023-04-01 09:00", "2023-04-01 10:00"]]
    merged_slots = []
    for slot in possible_slots:
        if not merged_slots:
            merged_slots.append(slot)
        else:
            if slot[0] == merged_slots[-1][1]:
                merged_slots[-1] = (merged_slots[-1][0], slot[1])
            else:
                merged_slots.append(slot)

    # Find time ranges greater than 15 minutes
    MIN_APPOINTMENT_TIME = 15
    available_times = []
    start_time = None
    for slot in merged_slots:
        if not start_time:
            start_time = slot[0]
        if slot[1] - start_time >= timedelta(minutes=MIN_APPOINTMENT_TIME):
            # available_times.append((start_time, slot[1]))
            available_times.append((
                start_time.strftime("%Y-%m-%dT%H:%M"), # Start time e.g. "2023-04-01T09:00"
                slot[1].strftime("%Y-%m-%dT%H:%M")))   # End time   e.g. "2023-04-01T10:30"
            start_time = None

    return jsonify(available_times), 200


# ------ SHIFTS -----------------
@app.route('/doctors/<int:doctor_id>/shifts', methods=['GET'])
def get_shifts(doctor_id):
    """ Endpoint to get doctor shifts

        Route:
            - /doctors/<int:doctor_id>/shifts
        Method:
            - GET: returns a list of all shifts for the given doctor
        Header:
            - Content-Type: application/json
        Query Params:
            - start_date (str): Start date of the range in YYYY-MM-DD format
                - Required: Optional
                - Example: "2023-04-01"
            - end_date (str): End date of the range in YYYY-MM-DD format
                - Required: Optional
                - Example: "2023-04-30"
        Returns:
            (json): list of shifts
                e.g. [{
                        "id": 1,
                        "doctor_id": 1,
                        "start_time": "2023-04-01 09:00",
                        "end_time":   "2023-04-01 17:00"
                    }, ...] 
    """
    # Get params
    start_date = request.args.get('start_date')
    end_date   = request.args.get('end_date')
    # Filter by date range
    if start_date and end_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            # Set to 23:59:59 to include the shifts on the end date.
            end_date_obj   = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
            # Caution: End date cannot be before the start date
            if end_date_obj < start_date_obj:
                msg = {"error": "End date cannot be before start date."}
                return jsonify(msg), 400
            # Query
            shifts = Shift.query.filter(
                    Shift.doctor_id == doctor_id,
                    Shift.start_time >= start_date_obj,
                    Shift.start_time <= end_date_obj
                ).all()
        except ValueError:
            return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400
    else:
        # All shifts
        shifts = Shift.query.filter_by(doctor_id=doctor_id).all()
    results = [shift.serialize() for shift in shifts]
    return jsonify(results), 200


@app.route('/doctors/<int:doctor_id>/shifts', methods=['POST'])
def add_shift(doctor_id):
    """ Endpoint to add doctor shifts

        TODO: Merge with the get_shifts endpoint?
        Route:
            - /doctors/<int:doctor_id>/shifts
        Method:
            - GET: returns a list of all shifts for the given doctor
            - POST: creates a new shift for the given doctor
        Header:
            - Content-Type: application/json
        Params:
            - start_time (timestamp): start time of the shift
                - Required: True
                - Example: "2023-04-01 09:00"
            - end_time (timestamp): end time of the shift
                - Required: True
                - Example: "2023-04-01 09:00"
        Returns:
            (json): the newly created shift
                e.g. {
                        "id": 1,
                        "doctor_id": 1,
                        "start_time": "2023-04-01 09:00",
                        "end_time":   "2023-04-01 17:00"
                    }
    """
    start_time = request.args.get('start_time')
    end_time   = request.args.get('end_time')
    
    # Check if the star/end times are provided
    if not start_time or not end_time:
        msg = {'message': 'start_time and end_time are required'}
        return jsonify(msg), 400
    
    # Check if doctor has another shift on that range
    overlapping_shifts = Shift.query.filter_by(doctor_id=doctor_id).filter(
        (Shift.start_time <= start_time) & (Shift.end_time >= start_time) | 
        (Shift.start_time <= end_time) & (Shift.end_time >= end_time)).all()
    if overlapping_shifts:
        msg = {'message': 'A shift already exists during the given time range'}
        return jsonify(msg), 400

    # Add the shift to the database
    shift = Shift(doctor_id=doctor_id, 
                    start_time=start_time, 
                    end_time=end_time)
    db.session.add(shift)
    db.session.commit()

    return jsonify(shift.serialize()), 201
    

@app.route('/doctors/<int:doctor_id>/shifts/<int:shift_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_shift(doctor_id, shift_id):
    """ Endpoint to manage a doctor's shift

        Route:
            - /doctors/<int:doctor_id>/shifts/<int:shift_id>
        Method:
            - GET: returns a shift for the given doctor
            - PUT: updates an existing shift for the given doctor
            - DELETE: deletes an existing shift for the given doctor
        Params:
            - start_time (timestamp): start time of the shift
                - Required: PUT
            - end_time (timestamp): end time of the shift
                - Required: PUT
        Returns:
            (json): updated shift or delete confirmation
                e.g. {
                        "id": 1,
                        "doctor_id": 1,
                        "start_time": "2023-04-01T09:00:00",
                        "end_time": "2023-04-01T17:00:00"
                    }
    """
    # Get the shift for the given doctor
    shift = Shift.query.filter_by(id=shift_id, doctor_id=doctor_id).first()
    # Check if the shift exists
    if not shift:
        msg = {'message': 'Shift not found'}
        return jsonify(msg), 404

    # GET the shift details
    if request.method == 'GET':
        return jsonify(shift.serialize()), 200

    # UPDATE the shift
    elif request.method == 'PUT':
        start_time = request.args.get('start_time')
        end_time   = request.args.get('end_time')

        # Check if the start/end times are provided
        if not start_time or not end_time:
            msg = {'message': 'start_time and end_time are required'}
            return jsonify(), 400
        # Caution: End date cannot be before the start date
        if end_time < start_time:
            msg = {"error": "End date cannot be before start date."}
            return jsonify(msg), 400

        shift.start_time = start_time
        shift.end_time   = end_time
        db.session.commit()
        return jsonify(shift.serialize()), 200

    # DELETE the shift
    elif request.method == 'DELETE':
        db.session.delete(shift)
        db.session.commit()
        msg = {'message': 'Shift deleted successfully'}
        return jsonify(msg), 200


# ------ APPOINTMENTS -----------
def is_doctor_available(doctor_id, start_time, end_time):
    """ Check if the doctor is available at the requested time

        Args:
            - doctor_id (int): id of the doctor
            - start_time (datetime): start time of the appointment
            - end_time (datetime): end time of the appointment
        Returns:
            (bool): True if the doctor is available, False otherwise
    """   
    # Check if doctor has shifts for the day
    shifts = Shift.query.filter(
        Shift.doctor_id == doctor_id,
        Shift.start_time <= start_time,
        Shift.end_time >= end_time
        ).all()
    if not shifts:
        return False

    # Check if appointment is within the shift
    start_time_hour     = start_time.time().hour
    start_time_minute   = start_time.time().minute
    end_time_hour       = end_time.time().hour
    end_time_minute     = end_time.time().minute
    for shift in shifts:
        if (start_time_hour < shift.start_time.hour or 
            (start_time_hour == shift.start_time.hour and start_time_minute < shift.start_time.minute) or
            end_time_hour > shift.end_time.hour or 
            (end_time_hour == shift.end_time.hour and end_time_minute > shift.end_time.minute)):
            return False
   
    # Check if there are any conflicting appointments
    conflicting_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.start_time < end_time,
            Appointment.end_time > start_time,
        ).all()
    #! DELTHIS
    logger.info('>> conflicting_appointments: %s', conflicting_appointments)
    #! -----
    if conflicting_appointments:
        return False
        
    return True
        

@app.route('/appointments', methods=['GET', 'POST'])
def manage_appointments():
    """ Endpoint to manage appointments

        TODO:
            - Add 'note' field to appointments
        Note:
             - Can't use the `/doctors/<int:doctor_id>/appointments` route because
               what if we want to get all the appointments for all doctors?
        Route:
            - /appointments
        Method:
            - GET: returns a list of all appointments
            - POST: creates a new appointment
        Params:
            - patient_id (int): ID of the patient making the appointment
                - Required: POST
            - doctor_id (int): ID of the doctor for the appointment
                - Required: POST
            - start_time (timestamp): start time of the appointment
                - Required: POST
            - end_time (timestamp): end time of the appointment
                - Required: POST
        Returns:
            (json): list of appointments or the newly created appointment
                e.g. [{
                        "id": 1,
                        "patient_id": 1,
                        "doctor_id": 1,
                        "start_time": "2023-04-01 10:00:00",
                        "end_time": "2023-04-01 11:00:00",
                        "status": "Scheduled"
                    }, ...] 
    """
    # GET: all appointments
    if request.method == 'GET':
        appointments = Appointment.query.all()
        results = [appointment.serialize() for appointment in appointments]
        return jsonify(results), 200

    # POST: Create new appointment
    elif request.method == 'POST':
        patient_id = request.args.get('patient_id')
        doctor_id  = request.args.get('doctor_id')
        start_time = request.args.get('start_time')
        end_time   = request.args.get('end_time')

        # Check if the required fields are provided
        if not patient_id or not doctor_id or not start_time or not end_time:
            msg = {'message': 'patient_id, doctor_id, start_time, and end_time are required'}
            return jsonify(msg), 400
        
        # Convert the start_time and end_time to datetime objects
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        end_time   = datetime.strptime(end_time, '%Y-%m-%d %H:%M')

        #! DELTHIS
        # logger.info('>> start_time: %s', start_time)
        # logger.info('>> end_time: %s', end_time)
        #! -----
    
        # Check if the duration of the appointment is at least 15 minutes
        duration = (end_time - start_time).total_seconds() / 60
        if duration < 15:
            msg = {'message': 'appointment duration should be at least 15 minutes'}
            return jsonify(msg), 400
        
        # Check if patient exists
        patient = Patient.query.get(patient_id)
        if not patient:
            msg = {"error": "Patient not found"}
            return jsonify(msg), 404
        
        # Check if the doctor exists
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            msg = {"error": "Doctor not found"}
            return jsonify(msg), 404

        # Check if the doctor is available
        if not is_doctor_available(doctor_id, start_time, end_time):
            msg = {'message': 'doctor is not available at the requested time'}
            return jsonify(msg), 400

        # Add the appointment to the database
        appointment = Appointment(patient_id=patient_id, 
                                  doctor_id=doctor_id, 
                                  start_time=start_time, 
                                  end_time=end_time)
        db.session.add(appointment)
        db.session.commit()

        return jsonify(appointment.serialize()), 201


@app.route('/appointments/<int:appointment_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_appointment(appointment_id):
    """ Endpoint to manage a specific appointment
    
        Route:
            - /appointments/<int:appointment_id>
        Methods:
            - GET: returns the appointment with the given ID
            - PUT: updates the appointment with the given ID
            - DELETE: deletes the appointment with the given ID
        Params:
            - appointment_id (int): ID of the appointment to manage
                - Required: Yes
        Returns:
            - GET: returns the appointment with the given ID
                e.g. {
                        "id": 1,
                        "patient_id": 1,
                        "doctor_id": 1,
                        "start_time": "2023-04-01T10:00:00",
                        "end_time":   "2023-04-01T11:00:00",
                        "note": "Annual checkup"
                    }
            - PUT: returns the updated appointment
                e.g. {
                        "id": 1,
                        "patient_id": 1,
                        "doctor_id": 1,
                        "start_time": "2023-04-01T10:30:00",
                        "end_time":   "2023-04-01T11:30:00",
                        "note": "Annual checkup"
                    }
            - DELETE: returns a success message
                e.g. {"message": "Appointment deleted successfully"}
    """
    # Get the appointment
    appointment = Appointment.query.get(appointment_id)
    # Check if the appointment exists
    if not appointment:
        msg = {"error": "Appointment not found"}
        return jsonify(msg), 404

    # GET: return the appointment
    if request.method == 'GET':
        return jsonify(appointment.serialize()), 200

    # PUT: update the appointment
    elif request.method == 'PUT':
        appointment.start_time  = request.args.get('start_time', appointment.start_time)
        appointment.end_time    = request.args.get('end_time', appointment.end_time)
        if not is_doctor_available(appointment.doctor_id, appointment.start_time, appointment.end_time):
            msg = {'message': 'doctor is not available at the requested time'}
            return jsonify(msg), 400
        # Save the changes
        db.session.commit()
        return jsonify(appointment.serialize()), 200

    # DELETE: cancel the appointment
    elif request.method == 'DELETE':
        db.session.delete(appointment)
        db.session.commit()
        msg = {"message": "Appointment deleted successfully"}
        return jsonify(msg), 200
    

# ------ PATIENTS ---------------
@app.route('/patients', methods=['GET', 'POST'])
def manage_patients():
    """ Endpoint to manage patients

        TODO:
            - Complete the endpoint!
        Route:
            - /patients
        Methods:
            - GET: returns a list of patients
            - POST: creates a new patient
        Params:
            - first_name (str): first name of the patient
                - Required: Yes
            - last_name (str): last name of the patient
                - Required: Yes
            - email (str): email of the patient
                - Required: Yes
            - phone (str): phone number of the patient
                - Required: Yes
            - date_of_birth (str): date of birth of the patient
                - Required: Yes
        Returns:
            - GET: returns all patients in a list
                e.g. [{
                        "id": 1,
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john@doe.com",
                        "phone": "1234567890",
                        "date_of_birth": "1990-01-01"
                        }, ...]
            - POST: returns a success message
                e.g. {"message": "Patient created successfully"}
    """
    pass


@app.route('/patients/<int:patient_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_patient(patient_id):
    """ Endpoint to manage a specific patient

        TODO:
            - Complete the endpoint!
        Route:
            - /patients/<int:patient_id>
        Methods:
            - GET: returns the patient with the given ID
            - PUT: updates the patient with the given ID
            - DELETE: deletes the patient with the given ID
        Params:
            - patient_id (int): ID of the patient to manage
                - Required: Yes
            - first_name (str): first name of the patient
                - Required: No
            - last_name (str): last name of the patient
                - Required: No
            - email (str): email of the patient
                - Required: No
            - phone (str): phone number of the patient
                - Required: No
            - date_of_birth (str): date of birth of the patient
                - Required: No
        Returns:
            - GET: returns the patient with the given ID
                e.g. {
                        "id": 1,
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "
            - PUT: returns a success message
                e.g. {"message": "Patient updated successfully"}
            - DELETE: returns a success message
                e.g. {"message": "Patient deleted successfully"}
    """
    pass


# ------ TEST -------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)