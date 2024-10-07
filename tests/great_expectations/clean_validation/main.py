from gx_utils.data_context import DataContextManager
from gx_utils.asset_manager import AssetManager
from clean_expectation_suites import CleanExpectationSuiteManager
from validation_manager import ValidationManager
import os
from dotenv import load_dotenv

def main():

    #Load environment variables in .env file:
    load_dotenv()
    
    # Add data sources:
    print("Starting Great Expectations validation...")
    data_source_name = "clean_hospital_data_source"
    config =  {
    "bucket_name": os.getenv("CLEAN_BUCKET"),
                "type": "parquet",
                "assets": [
                    {
                        "name": "clean_patients_data",
                        "s3_prefix": "cleaned/patients/latest/",
                        "batches": [
                            {"name": "clean_batch_patients", "file_prefix": "cleaned/patients/latest/"}
                        ]
                    },
                    {
                        "name": "clean_visits_data",
                        "s3_prefix": "cleaned/visits/latest/",
                        "batches": [
                            {"name": "clean_batch_visits", "file_prefix": "cleaned/visits/latest/"}
                        ]
                    }
                ]
            }
    context_manager = DataContextManager(context_directory="gx_"+data_source_name)
    
    # Loop over each data source and add it
    context_manager.add_data_source(data_source_name, config["bucket_name"])  

    # Setup assets and batch definitions
    asset_manager = AssetManager(context_manager.context, context_manager.data_sources) 
    asset_manager.setup_assets_by_type(data_source_name, config)

    # Setup expectation suites
    clean_suite_manager = CleanExpectationSuiteManager(context_manager.context)
    clean_suite_manager.setup_suites()

    # Setup validation definitions and checkpoint
    validation_manager = ValidationManager(context_manager.context)
    validation_manager.setup_validations(config, clean_suite_manager, data_source_name)

    # Run the checkpoint

    validation_manager.run_checkpoint()
    
    # Build data docs
    context_manager.context.build_data_docs()
    print("Check DataDocs Site at: ", "https://" + os.getenv(
        "GX_REPORT_BUCKET") + ".s3.eu-west-1.amazonaws.com/gx_" + data_source_name + "/index.html")

    print("Validation complete. Check the data docs for detailed results.")

if __name__ == "__main__":
    main()