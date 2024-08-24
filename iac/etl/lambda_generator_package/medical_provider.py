from faker import Faker
from faker.providers import BaseProvider

class MedicalProvider(BaseProvider):
    def diagnosis(self):
        diagnoses = [
            "Hypertension", "Diabetes Mellitus", "Asthma", "Chronic Obstructive Pulmonary Disease (COPD)",
            "Coronary Artery Disease", "Osteoarthritis", "Chronic Kidney Disease", "Congestive Heart Failure",
            "Anxiety Disorder", "Depressive Disorder", "Hyperlipidemia", "Gastroesophageal Reflux Disease (GERD)",
            "Thyroid Disorder", "Anemia", "Migraine", "Allergic Rhinitis"
        ]
        return self.random_element(diagnoses)

    def medical_notes(self):
        notes = [
            "Patient reports persistent cough and shortness of breath. Advised to increase dosage of inhaler.",
            "Follow-up required in 3 months for blood pressure monitoring.",
            "Prescribed Metformin 500mg twice daily for blood sugar control.",
            "Patient denies chest pain but reports occasional palpitations. ECG scheduled for next visit.",
            "Recommended lifestyle modifications and dietary changes to manage cholesterol levels.",
            "Patient advised to avoid allergens and continue antihistamine medication as needed.",
            "Blood tests indicate mild anemia. Iron supplements prescribed.",
            "Patient reports improvement in symptoms with current medication regimen."
        ]
        return self.random_element(notes)

    def medication(self):
        medications = [
            "Lisinopril", "Metformin", "Atorvastatin", "Albuterol", "Levothyroxine", "Omeprazole", "Amlodipine",
            "Losartan", "Hydrochlorothiazide", "Simvastatin", "Gabapentin", "Metoprolol", "Sertraline", "Citalopram",
            "Furosemide", "Warfarin", "Clopidogrel"
        ]
        return self.random_element(medications)


