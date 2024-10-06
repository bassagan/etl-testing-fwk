from tests.great_expectations.gx_utils.data_context import DataContextManager
from tests.great_expectations.gx_utils.asset_manager import AssetManager
from tests.great_expectations.raw_validation.raw_expectation_suites import RawExpectationSuiteManager
from validation_manager import ValidationManager
import os

def main():

    # Add data sources:
    print("Starting Great Expectations validation...")
    data_source_name = "raw_hospital_data_source"
    config =  {
            "bucket_name": os.getenv("RAW_BUCKET"),
            "type": "json",
            "assets": [
                {
                    "name": "raw_patients_data",
                    "s3_prefix": "patients/",
                    "batches": [
                        {"name": "raw_batch_patients", "file_prefix": "patients"}
                    ]
                },
                {
                    "name": "raw_visits_data",
                    "s3_prefix": "visits/",
                    "batches": [
                        {"name": "raw_batch_visits", "file_prefix": "visits"}
                    ]
                }
            ]
        }
    context_manager = DataContextManager(context_directory="gx_" + data_source_name)
    
    # Loop over each data source and add it
    context_manager.add_data_source(data_source_name, config["bucket_name"])  

    # Setup assets and batch definitions
    asset_manager = AssetManager(context_manager.context, context_manager.data_sources) 
    asset_manager.setup_assets_by_type(data_source_name, config)

    # Setup expectation suites
    raw_suite_manager = RawExpectationSuiteManager(context_manager.context)
    raw_suite_manager.setup_suites()

    # Setup validation definitions and checkpoint
    validation_manager = ValidationManager(context_manager.context)
    validation_manager.setup_validations(config, raw_suite_manager, data_source_name)

    # Run the checkpoint

    validation_manager.run_checkpoint()
    
    # Build data docs
    context_manager.context.build_data_docs()

    print("Validation complete. Check the data docs for detailed results.")

if __name__ == "__main__":
    main()