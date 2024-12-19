# Step-by-Step Guide for Developing Doctor Appointment Management System

## Step 1: Setting Up the Project Structure
Create the following directory structure:
```bash
mkdir doctor_appointment_system
cd doctor_appointment_system
mkdir app
```
Inside the `app` folder, create the following files:
- `app.py` (Main Flask application)
- `models.py` (Database models)
- `requirements.txt` (Python dependencies)
- `Dockerfile` (Docker configuration for Flask app)

In the root folder, create:
- `docker-compose.yml` (Docker Compose configuration)
- `README.md` (Project documentation and static HTML description)

---

## Step 2: Writing the Flask Application
### app.py
```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/appointments')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models
from models import Doctor, Appointment

@app.route('/doctors', methods=['POST'])
def create_doctor():
    data = request.json
    doctor = Doctor(name=data['name'], specialization=data['specialization'], availability=data['availability'])
    db.session.add(doctor)
    db.session.commit()
    return jsonify({"message": "Doctor profile created successfully."}), 201

@app.route('/appointments', methods=['POST'])
def book_appointment():
    data = request.json
    appointment = Appointment(patient_name=data['patient_name'], doctor_id=data['doctor_id'], appointment_time=data['appointment_time'])
    db.session.add(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment booked successfully."}), 201

@app.route('/appointments/<int:doctor_id>', methods=['GET'])
def view_appointments(doctor_id):
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    return jsonify([{
        "patient_name": a.patient_name,
        "appointment_time": a.appointment_time.strftime('%Y-%m-%d %H:%M')
    } for a in appointments])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## Step 3: Writing Database Models
### models.py
```python
from app import db
from datetime import datetime

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(200), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy=True))
```

---

## Step 4: Configuring Docker
### Dockerfile
```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### requirements.txt
```
Flask==2.2.5
Flask-SQLAlchemy==3.0.5
psycopg2-binary==2.9.8
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: ./app
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/appointments
    depends_on:
      - db

  db:
    image: postgres:14
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: appointments
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

---

## Step 5: Adding Documentation and Static HTML File
### README.md
```markdown
# Doctor Appointment Management System

This project is a Flask-based application for managing doctor appointments. It uses Docker for containerization and PostgreSQL as the database backend.

## Features
- **Create Doctor Profiles**
- **Book Appointments**
- **View Booked Appointments**

## Getting Started
### Prerequisites
- Docker and Docker Compose

### Installation
1. Clone the repository.
2. Run `docker-compose up` to start the system.

### Endpoints
- `POST /doctors`: Add doctor profiles.
- `POST /appointments`: Book appointments.
- `GET /appointments/<doctor_id>`: View appointments for a doctor.
