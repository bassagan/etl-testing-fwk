import pandas as pd

class VisitsSummary:
    def __init__(self, df_visits):
        self.df_visits = df_visits

    def calculate_total_visits(self):
        """Calculates total visits for each patient."""
        return self.df_visits.groupby('patient_id')['appointment_id'].count().reset_index(name='total_visits')

    def calculate_last_visit_date(self):
        """Calculates the last visit date for each patient."""
        return self.df_visits.groupby('patient_id')['appointment_date'].max().reset_index(name='last_visit_date')

    def get_summary(self):
        """Generates a summary DataFrame with total visits and last visit date."""
        total_visits = self.calculate_total_visits()
        last_visit_date = self.calculate_last_visit_date()
        return pd.merge(total_visits, last_visit_date, on='patient_id')
