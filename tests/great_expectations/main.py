from data_context import DataContextManager
from asset_manager import AssetManager
from expectation_suites import ExpectationSuiteManager
from validation_manager import ValidationManager
import uuid

def main():
    print("Starting Great Expectations validation...")
    context_manager = DataContextManager()
    print("context_manager context", context_manager.context)
    asset_manager = AssetManager(context_manager.context, context_manager.data_source)
    suite_manager = ExpectationSuiteManager(context_manager.context)
    validation_manager = ValidationManager(context_manager.context)

    # Setup assets and batch definitions
    asset_manager.setup_assets()

    # Setup expectation suites
    suite_manager.setup_suites()

    # Setup validation definitions and checkpoint
    validation_manager.setup_validations(asset_manager, suite_manager)

    # Run the checkpoint
    validation_results = validation_manager.run_checkpoint()
    
    # Build data docs
    context_manager.context.build_data_docs()

    print("Validation complete. Check the data docs for detailed results.")

if __name__ == "__main__":
    main()