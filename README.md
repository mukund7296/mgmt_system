# Flask-based Medical API with Docker and Database

## Step-by-Step Instructions

This project will set up a Flask-based API to manage patient data, use SQLite as the database, and deploy it using Docker.

### 1. Prerequisites
- Python installed on your system.
- Docker installed.
- A code editor (VS Code or any other).

### 2. Create the Project Structure

```plaintext
medical_api_project/
|-- app/
|   |-- __init__.py
|   |-- models.py
|   |-- routes.py
|   |-- database.db
|-- Dockerfile
|-- requirements.txt
|-- app.py
|-- README.md
```

### 3. Flask App Code

#### **app/__init__.py**
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes
```

#### **app/models.py**
```python
from app import db

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    treatment = db.Column(db.String(200), nullable=True)
```

#### **app/routes.py**
```python
from flask import request, jsonify
from app import app, db
from app.models import Patient

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    new_patient = Patient(
        name=data['name'],
        age=data['age'],
        diagnosis=data['diagnosis'],
        treatment=data.get('treatment', None)
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient added successfully', 'patient': data}), 201

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    results = [
        {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "diagnosis": patient.diagnosis,
            "treatment": patient.treatment
        } for patient in patients
    ]
    return jsonify(results), 200
```

#### **app.py**
```python
from app import app, db
from app.models import Patient

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 4. Install Dependencies

#### **requirements.txt**
```plaintext
Flask==2.2.3
Flask-SQLAlchemy==3.0.4
```

Install them locally (optional for testing):

```bash
pip install -r requirements.txt
```

### 5. Create the Dockerfile

#### **Dockerfile**
```Dockerfile
# Use the official Python image as a base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /usr/src/app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
```

### 6. Build and Run the Docker Container

1. Open the terminal in the project root directory (`medical_api_project`).

2. Build the Docker image:
   ```bash
   docker build -t medical-api .
   ```

3. Run the Docker container:
   ```bash
   docker run -p 5000:5000 medical-api
   ```

### 7. Test the API

1. Use tools like Postman or `curl` to test the endpoints.

2. Add a patient:
   ```bash
   curl -X POST http://127.0.0.1:5000/patients -H "Content-Type: application/json" \
   -d '{"name": "John Doe", "age": 45, "diagnosis": "Hypertension", "treatment": "Medication"}'
   ```

3. Retrieve all patients:
   ```bash
   curl -X GET http://127.0.0.1:5000/patients
   ```

### 8. README File

#### **README.md**
```markdown
# Medical API Project

This project is a Flask-based API for managing patient records. It uses SQLite as a database and is containerized with Docker for easy deployment.

## Features
- Add a new patient record.
- Retrieve all patient records.

## Prerequisites
- Python 3.x
- Docker

## How to Run

### Without Docker:
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```

### With Docker:
1. Build the image:
   ```bash
   docker build -t medical-api .
   ```
2. Run the container:
   ```bash
   docker run -p 5000:5000 medical-api
   ```

## API Endpoints

### Add a Patient
**POST /patients**

Request Body:
```json
{
  "name": "John Doe",
  "age": 45,
  "diagnosis": "Hypertension",
  "treatment": "Medication"
}
```

### Get All Patients
**GET /patients**

Response:
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "age": 45,
    "diagnosis": "Hypertension",
    "treatment": "Medication"
  }
]
```

## Technologies Used
- Python (Flask)
- SQLite
- Docker
