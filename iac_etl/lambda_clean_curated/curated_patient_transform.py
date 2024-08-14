import pandas as pd
from datetime import datetime


class CuratedPatientTransform:
    def transform(self, df_patients, df_visits):
        today = datetime.today()

        # Calculate the age
        df_patients['age'] = today.year - df_patients['date_of_birth'].dt.year

        # Extract year and month from date_of_birth
        df_patients['year_of_birth'] = df_patients['date_of_birth'].dt.year
        df_patients['month_of_birth'] = df_patients['date_of_birth'].dt.month

        # Summarize total visits and last visit date
        visit_summary = df_visits.groupby('patient_id').agg(
            total_visits=('appointment_id', 'count'),
            last_visit_date=('appointment_date', 'max')
        ).reset_index()

        # Merge the summary with the patients data
        df_curated_patients = df_patients.merge(visit_summary, on='patient_id', how='left')
        df_curated_patients['total_visits'].fillna(0, inplace=True)
        df_curated_patients['last_visit_date'].fillna(pd.NaT, inplace=True)

        # Extract city from address (assuming the city is the second last element in the address string)
        df_curated_patients['city'] = df_curated_patients['address'].apply(self.extract_city)

        return df_curated_patients

    def extract_city(self, address):
        """Extracts the city from the address string."""
        # Assuming the city is located between the last and second-to-last commas
        try:
            parts = address.split(',')
            if len(parts) > 2:
                return parts[-2].strip()
            else:
                return address  # Return the full address if city extraction fails
        except Exception as e:
            return None  # Return None if the extraction fails
