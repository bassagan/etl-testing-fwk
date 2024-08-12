import json
import uuid
import random
from datetime import datetime, timedelta
import faker
from medical_provider import MedicalProvider

class DataGenerator:
    def __init__(self, bucket_name, s3_client, patients_file, visits_file, latest_patients_prefix, latest_visits_prefix):
        self.fake = faker.Faker()
        self.fake.add_provider(MedicalProvider)
        self.bucket_name = bucket_name
        self.s3_client = s3_client
        self.patients_file = patients_file
        self.visits_file = visits_file
        self.latest_patients_prefix = latest_patients_prefix
        self.latest_visits_prefix = latest_visits_prefix
        self.patients = []
        self.visits = []

    def save_to_s3(self, key, data):
        """Saves data to S3 bucket."""
        self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=json.dumps(data))

    def load_from_s3(self, key):
        """Loads data from S3 bucket."""
        try:
            obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            return json.loads(obj['Body'].read().decode('utf-8'))
        except self.s3_client.exceptions.NoSuchKey:
            return None

    def get_latest_file(self, prefix):
        """Gets the latest file from the specified S3 prefix."""
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        if 'Contents' in response:
            latest_file = max(response['Contents'], key=lambda x: x['LastModified'])
            return latest_file['Key']
        return None

    def generate_new_patients(self, num_patients):
        new_patients = [{
            "patient_id": str(uuid.uuid4()),
            "name": self.fake.name(),
            "date_of_birth": self.fake.date_of_birth(minimum_age=20, maximum_age=90).isoformat(),
            "address": self.fake.address().replace("\n", ", "),
            "phone_number": self.fake.phone_number(),
            "email": self.fake.email(),
            "insurance_provider": self.fake.company(),
            "policy_number": self.fake.bothify(text='???-########'),
            "policy_valid_till": (datetime.now() + timedelta(days=random.randint(30, 365))).isoformat(),
            "record_created_at": datetime.now().isoformat(),
            "record_updated_at": datetime.now().isoformat()
        } for _ in range(num_patients)]

        self.patients.extend(new_patients)

    def generate_new_visits(self, patients_to_add_visits):
        """Generates 1 to 3 visits for each patient."""
        for patient in patients_to_add_visits:
            num_visits = random.randint(1, 3)  # Each patient gets between 1 to 3 visits
            for _ in range(num_visits):
                visit = {
                    "appointment_id": str(uuid.uuid4()),
                    "patient_id": patient['patient_id'],
                    "appointment_date": self.fake.date_time_this_year().isoformat(),
                    "doctor": self.fake.name(),
                    "department": random.choice(['Cardiology', 'Neurology', 'Oncology', 'Pediatrics', 'General Medicine']),
                    "purpose": random.choice(['Routine Checkup', 'Follow-up', 'Consultation', 'Specialist Referral']),
                    "status": random.choice(['Scheduled', 'Completed', 'Cancelled']),
                    "diagnosis": None,
                    "medication": None,
                    "notes": None,
                    "record_created_at": datetime.now().isoformat(),
                    "record_updated_at": datetime.now().isoformat()
                }
                self.visits.append(visit)

    def load_existing_data(self):
        """Loads the most recent patient and visit data from S3."""
        latest_patients_file = self.get_latest_file(self.latest_patients_prefix)
        latest_visits_file = self.get_latest_file(self.latest_visits_prefix)

        if latest_patients_file:
            self.patients = self.load_from_s3(latest_patients_file) or []
        if latest_visits_file:
            self.visits = self.load_from_s3(latest_visits_file) or []

    def update_patient_record(self, patient):
        if random.random() < 0.2:  # 20% chance to update the patient's address
            patient["address"] = self.fake.address().replace("\n", ", ")
            patient["record_updated_at"] = datetime.now().isoformat()

    def update_visit_record(self, visit):
        if visit["status"] == "Scheduled" and random.random() < 0.5:
            visit["status"] = "Completed"
            if random.random() < 0.8:  # 80% chance to add diagnosis/medication on completion
                visit["diagnosis"] = self.fake.diagnosis()
                visit["medication"] = self.fake.medication()
            visit["record_updated_at"] = datetime.now().isoformat()

    def remove_old_visits(self):
        one_day_ago = datetime.now() - timedelta(days=1)
        self.visits = [visit for visit in self.visits if datetime.fromisoformat(visit["appointment_date"]) > one_day_ago]

    def remove_patients_with_no_visits(self):
        if random.random() < 0.1:
            patient_ids_with_visits = {visit['patient_id'] for visit in self.visits}
            self.patients = [patient for patient in self.patients if patient['patient_id'] in patient_ids_with_visits]

    def update_existing_data(self, initial_patients_range, new_patients_range):
        for patient in self.patients:
            self.update_patient_record(patient)

        for visit in self.visits:
            self.update_visit_record(visit)

        # Remove visits older than 1 day
        self.remove_old_visits()

        # Remove patients with no visits
        self.remove_patients_with_no_visits()

        # Generate a random number of new patients within the specified range
        num_new_patients = random.randint(*new_patients_range)
        self.generate_new_patients(num_new_patients)

        # Generate visits for the newly added patients
        self.generate_new_visits(self.patients[-num_new_patients:])

    def save_data_to_s3(self):
        self.save_to_s3(self.patients_file, self.patients)
        self.save_to_s3(self.visits_file, self.visits)
