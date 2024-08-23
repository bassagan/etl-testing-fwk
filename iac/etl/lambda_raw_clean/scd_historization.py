import pandas as pd
from datetime import datetime

class SCDHistorization:
    def __init__(self, keys):
        self.keys = keys

    def apply_scd_type_2(self, df_new, df_existing):
        """Apply SCD Type 2 historization."""
        if df_existing is None:
            df_new['start_date'] = datetime.now()
            df_new['end_date'] = None
            df_new['is_current'] = True
            return df_new

        df_existing = df_existing.copy()

        # Mark the existing records as not current
        df_existing.loc[:, 'is_current'] = False
        df_existing.loc[:, 'end_date'] = datetime.now()

        # Identify new records and unchanged records
        df_new = df_new.merge(df_existing[self.keys + ['is_current']], on=self.keys, how='left', indicator=True)
        df_new['start_date'] = datetime.now()
        df_new['end_date'] = None
        df_new['is_current'] = df_new['_merge'] == 'left_only'
        df_new = df_new.drop(columns=['_merge'])

        # Combine new and old records
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)

        return df_combined
