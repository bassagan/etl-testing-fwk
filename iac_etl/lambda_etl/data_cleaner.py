import pandas as pd

class DataCleaner:
    def __init__(self, schema):
        self.schema = schema

    def enforce_schema(self, df):
        """Apply specific data types to the DataFrame columns based on the provided schema."""
        for column, dtype in self.schema.items():
            if column in df.columns:
                df[column] = df[column].astype(dtype, errors='ignore')
        return df

    def remove_duplicates(self, df):
        """Remove duplicate records from the DataFrame."""
        return df.drop_duplicates()
