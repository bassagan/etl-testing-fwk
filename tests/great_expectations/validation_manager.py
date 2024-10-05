import great_expectations as gx
from great_expectations import RunIdentifier
import uuid
from datetime import datetime

class ValidationManager:
    def __init__(self, context):
        self.context = context
        self.checkpoint = None
        self.checkpoint_name = "patients_and_visits_checkpoint"

    def setup_validations(self, asset_manager, suite_manager):
        patients_vd = self._create_validation_definition(
            "patients_validation_definition",
            "patients_data",
            "batch_patients",
            suite_manager.patients_suite
        )
        visits_vd = self._create_validation_definition(
            "visits_validation_definition",
            "visits_data",
            "batch_visits",
            suite_manager.visits_suite
        )

        self._create_checkpoint([patients_vd, visits_vd])

    def _create_validation_definition(self, vd_name, asset_name, batch_name, suite):
        try:
            validation_definition = self.context.validation_definitions.get(vd_name)
            print(f"Using existing validation definition: {vd_name}")
        except gx.exceptions.DataContextError:
            print(f"Creating new validation definition: {vd_name}")
            validation_definition = gx.ValidationDefinition(
                data=self.context.get_datasource("s3_raw_data_source").get_asset(asset_name).get_batch_definition(batch_name),
                suite=suite,
                name=vd_name
            )
            validation_definition = self.context.validation_definitions.add(validation_definition)
        return validation_definition

    def _create_checkpoint(self, validation_definitions):
        action_list = [
            gx.checkpoint.UpdateDataDocsAction(
                name="update_all_data_docs",
            )
        ]

        try:
            self.checkpoint = self.context.checkpoints.get(self.checkpoint_name)
            print(f"Using existing checkpoint: {self.checkpoint_name}")
        except gx.exceptions.DataContextError:
            print(f"Creating new checkpoint: {self.checkpoint_name}")
            self.checkpoint = gx.Checkpoint(
                name=self.checkpoint_name,
                validation_definitions=validation_definitions,
                actions=action_list,
                result_format={"result_format": "COMPLETE"},
            )
            self.context.checkpoints.add(self.checkpoint)

    def run_checkpoint(self):
        # Generate a unique run name
        unique_id = str(uuid.uuid4())
        run_name = f"{self.checkpoint_name}_{unique_id}"

        # Get the current datetime
        run_time = datetime.now()

        # Create a RunIdentifier
        run_identifier = RunIdentifier(run_name=run_name, run_time=run_time)

        # Run the checkpoint and capture the results
        return self.checkpoint.run(run_id=run_identifier)

    

