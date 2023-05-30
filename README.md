# Health API #

[![Repo](https://img.shields.io/badge/source-GitHub-303030.svg?maxAge=3600&style=flat-square)](https://github.com/buraktokman/Health-API) ![Python](https://img.shields.io/badge/python-3.9-blue.svg?maxAge=3600&style=flat-square) ![License](https://img.shields.io/badge/License-EULA-orange) 
<!-- https://shields.io/ -->

This is a Python application that provides RESTful endpoints to manage doctors, their profiles, and allows users to book appointments with them. Built with Python, Flask, and SQLAlchemy.

## Architecture

The following technologies and tools were used in the development of this application. Before setting up the Health-API service, you need to ensure that you have the following prerequisites installed:

- [**Flask Application:**](https://flask.palletsprojects.com/) A lightweight Python web framework for building web applications.
- **PostgreSQL:** Relational database systems used for storing and managing data.
- **Python 3.9:** The programming language used for implementing the application.
- **Google Cloud Platform (GCP):** A suite of cloud computing services provided by Google.
- **gcloud Utility:** A command-line interface for interacting with GCP services.
- [**Terraform:**](https://www.terraform.io/) Open-source infrastructure as code (IAC) tool used for building, changing, and versioning infrastructure safely and efficiently. 

## API Endpoints ##
The following endpoints are available:

### Doctors ###

| Endpoint                 | Method | Description               |
|--------------------------|--------|---------------------------|
| /doctors                 | GET    | Get a list of all doctors |
| /doctors/`<int:doctor_id>` | GET    | Get a doctor by ID        |
| /doctors                 | POST   | Add a new doctor          |
| /doctors/`<int:doctor_id>` | PUT    | Update a doctor           |
| /doctors/`<int:doctor_id>` | DELETE | Delete a doctor           |
| /doctors/`<int:doctor_id>`/availability | GET | Get available time ranges from a doctor to book an appointment |


### Shifts ###

| Endpoint                                       | Method | Description |
|------------------------------------------------|--------|-------------|
| /doctors/`<int:doctor_id>`/shifts                | GET    | Get a list of all the shifts of a doctor |
| /doctors/`<int:doctor_id>`/shifts                | POST   | Add a new shift to a doctor |
| /doctors/`<int:doctor_id>`/shifts/`<int:shift_id>` | GET    | Get a shift by ID |
| /doctors/`<int:doctor_id>`/shifts/`<int:shift_id>` | PUT    | Update a shift |
| /doctors/`<int:doctor_id>`/shifts/`<int:shift_id>` | DELETE | Delete a shift |


### Appointments ###

| Endpoint                           | Method | Description |
|------------------------------------|--------|-------------|
| /appointments                      | GET    | Get the list of all appointments |
| /appointments                      | POST   | Add a new appointment |
| /appointments/`<int:appointment_id>` | GET    | Get an appointment by ID |
| /appointments/`<int:appointment_id>` | PUT    | Update an appointment |
| /appointments/`<int:appointment_id>` | DELETE | Delete an appointment |


### Patients ###

| Endpoint                           | Method | Description |
|------------------------------------|--------|-------------|
| /patients                          | GET    | Get the list of all patients |
| /patients                          | POST   | Add a new patient |
| /patients/`<int:patient_id>`       | GET    | Get a patient by ID |
| /patients/`<int:patient_id>`       | PUT    | Update a patient |
| /patients/`<int:patient_id>`       | DELETE | Delete a patient |


### Example requests and responses

<details>
  <summary>List doctors</summary>
  <markdown>

#### Request

    GET /doctors HTTP/1.1
    Accept: application/vnd.api+json

#### Response

    HTTP/1.1 200 OK
    Content-Type: application/vnd.api+json
    
    [
      {
         "date_added": "2023-04-01T08:33:23.228331",
         "date_modified": "2023-04-01T08:33:23.228336",
         "first_name": "Richard",
         "id": 17,
         "last_name": "Branson",
         "personal_statement": "Certified practitioner",
         "profile_picture": null,
         "specialty_id": 4,
         "specialty_name": "Dermatology"
      },
      {
         "date_added": "2023-03-29T21:09:45.932443",
         "date_modified": "2023-03-29T21:09:45.932443",
         "first_name": "Sara",
         "id": 5,
         "last_name": "Johnson",
         "personal_statement": "I am an internist with a passion for preventative medicine and patient education.",
         "profile_picture": "gs://health-app/img/profile_pics/sara_johnson.jpg",
         "specialty_id": 2,
         "specialty_name": "Internal Medicine"
      }
    ]

  </markdown>
</details>


<details>
  <summary>Add doctor</summary>
  <markdown>

#### Request

    POST /doctors HTTP/1.1
    Content-Type: application/vnd.api+json
    Accept: application/vnd.api+json

    {
      "first_name": "John",
      "last_name": "Doe",
      "specialty_name": "Internal Medicine",
      "personal_statement": "Let food be thy medicine."
    }

#### Response

    HTTP/1.1 200 OK
    Content-Type: application/vnd.api+json
    
    {
      "doctor_id": 18,
      "message": "Doctor added successfully."
    }

  </markdown>
</details>


<details>
  <summary>Delete doctor</summary>
  <markdown>

#### Request

   DELETE /doctors/18 HTTP/1.1
   Accept: application/vnd.api+json

#### Response

    HTTP/1.1 200 OK
    Content-Type: application/vnd.api+json
    
    {"message": "Doctor deleted successfully"}

  </markdown>
</details>


---

## Constraints

- The doctors should be able to update their profile statement and picture (if available).
- Filtering and searching should be primarily processed on the server if possible.
- There can't be two appointments with the same doctor at the same time period.
- The minimum duration for an appointment is 15 minutes.

---

## Prerequisites

Before setting up the Health API service, you need to ensure that you have the following prerequisites installed:

- Python 3.9
- gcloud CLI
- Terraform

## Setting up the development environment ##

1. Clone the repository to your local machine:

```
git clone https://github.com/buraktokman/Health-API
cd Health-API
```


2. Create a virtual environment and activate it:

```
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Create a PostgreSQL database for the application and import the `health.sql` file in the `sql` directory.
5. Set the credentials and details of the database in the `src/settings.py` file.
6. Start the API server (2 options):
   - `python main.py`
   - `bash start_server.sh`

## Running the Tests

TODO: here

## Deploying on GCP with Terraform

TODO: here

---

## Changelog

**0.3.0 (todo)**

```
- Unit tests and integration tests.
- Terraform code for provisioning the necessary infrastructure.
- To be defined...
```

**0.2.0 (WIP)**

```
- Patients endpoint.
```

**0.1.0**

```
- All major endpoints completed.
```

