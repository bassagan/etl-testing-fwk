from visits_summary import VisitsSummary
import pandas as pd
import datetime

class CuratedPatientTransform:
    def transform(self, df_patients, df_visits):
        """Transforms the clean patient data into the curated patient model."""

        # Derive age from date_of_birth
        today = datetime.datetime.today()
        df_patients['age'] = df_patients['date_of_birth'].apply(
            lambda dob: today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)))

        # Generalize address (e.g., extract city or region)
        df_patients['address'] = df_patients['address'].apply(lambda x: x.split(',')[-1].strip() if ',' in x else x)

        # Calculate total visits and last visit date
        visits_summary = VisitsSummary(df_visits)
        summary = visits_summary.get_summary()

        # Merge summary into patient data
        df_curated = pd.merge(df_patients, summary, on='patient_id', how='left').fillna(
            {'total_visits': 0, 'last_visit_date': pd.NaT})

        # Return the curated DataFrame
        return df_curated[['patient_id', 'name', 'date_of_birth', 'age', 'address', 'phone_number',
                           'email', 'insurance_provider', 'policy_number', 'policy_valid_till',
                           'total_visits', 'last_visit_date', 'record_created_at']]
