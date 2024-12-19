from flask import Flask, request, jsonify
from models import db, Patient
from database import initialize_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/patient_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

initialize_db(app)

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    new_patient = Patient(name=data['name'], age=data['age'], diagnosis=data['diagnosis'])
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient added successfully'}), 201

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    results = [{'id': p.id, 'name': p.name, 'age': p.age, 'diagnosis': p.diagnosis} for p in patients]
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
