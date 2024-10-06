import pandas as pd
from datetime import datetime


class CuratedVisitTransform:
    def transform(self, df_visits):
        """Transforms the clean visit data into the curated visit model."""

        # Derive visit month and year from appointment_date
        df_visits['visit_month'] = df_visits['appointment_date'].dt.month
        df_visits['visit_year'] = df_visits['appointment_date'].dt.year

        # Standardize doctor name, department, and other fields if necessary
        df_visits['doctor_name'] = df_visits['doctor'].str.title()
        df_visits['department'] = df_visits['department'].str.title()

        # Select and reorder the necessary columns for the curated model
        df_curated = df_visits[['appointment_id', 'patient_id', 'appointment_date', 'doctor_name',
                                'department', 'purpose', 'status', 'diagnosis', 'medication',
                                'notes', 'visit_month', 'visit_year', 'record_created_at',
                                'record_updated_at']]

        # Ensure the data types are consistent with the schema (if required)
        df_curated = df_curated.astype({
            'appointment_id': 'string',
            'patient_id': 'string',
            'appointment_date': 'datetime64[ns]',
            'doctor_name': 'string',
            'department': 'string',
            'purpose': 'string',
            'status': 'string',
            'diagnosis': 'string',
            'medication': 'string',
            'notes': 'string',
            'visit_month': 'int',
            'visit_year': 'int',
            'record_created_at': 'datetime64[ns]',
            'record_updated_at': 'datetime64[ns]'
        })

        return df_curated
