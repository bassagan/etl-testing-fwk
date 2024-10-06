import great_expectations as gx
from great_expectations import RunIdentifier
import uuid
from datetime import datetime

class ValidationManager:
    def __init__(self, context):
        self.context = context
        self.checkpoint = None
        self.checkpoint_name = "raw_patients_and_visits_checkpoint"

    def setup_validations(self, config, suite_manager, data_source_name):
        validation_definition_list = []
        for asset in config["assets"]: 
            for batch in asset["batches"]: 
                if "patient" in asset["name"]:
                    suite = suite_manager.patients_suite
                else: 
                    suite = suite_manager.visits_suite
                    
                validation_definition_list.append(
                    self._create_validation_definition(
                        asset["name"] + "_validation",
                        asset["name"],
                        batch["name"],
                        suite,
                        data_source_name
                    )
                )
        self._create_checkpoint(validation_definition_list)

    def _create_validation_definition(self, vd_name, asset_name, batch_name, suite, data_source_name):
        try:
            validation_definition = self.context.validation_definitions.get(vd_name)
            print(f"Using existing validation definition: {vd_name}")
        except gx.exceptions.DataContextError:
            print(f"Creating new validation definition: {vd_name}")
            validation_definition = gx.ValidationDefinition(
                data=self.context.get_datasource(data_source_name).get_asset(asset_name).get_batch_definition(batch_name),
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
                result_format={"result_format": "BASIC"},
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

    

