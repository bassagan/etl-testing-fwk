import great_expectations as gx
import great_expectations.expectations as gxe

class CleanExpectationSuiteManager:
    def __init__(self, context):
        self.context = context
        self.patients_suite = None
        self.visits_suite = None

    def setup_suites(self):
        self.patients_suite = self._get_or_create_suite("clean_patients_data_suite")
        self.visits_suite = self._get_or_create_suite("clean_visits_data_suite")
        self._add_patient_expectations()
        self._add_visit_expectations()

    def _get_or_create_suite(self, suite_name):
        try:
            suite = self.context.suites.get(suite_name)
            print(f"Using existing expectation suite: {suite_name}")
        except gx.exceptions.DataContextError:
            print(f"Creating new expectation suite: {suite_name}")
            suite = gx.ExpectationSuite(name=suite_name)
            suite = self.context.suites.add(suite)
        return suite

    def _add_patient_expectations(self):
        patient_expectations = [
            gxe.ExpectColumnValuesToNotBeNull(column="patient_id"),
                   ]
        for expectation in patient_expectations:
            self.patients_suite.add_expectation(expectation)

    def _add_visit_expectations(self):
        visit_expectations = [
            gxe.ExpectColumnValuesToNotBeNull(column="appointment_id"),
            ]
        for expectation in visit_expectations:
            self.visits_suite.add_expectation(expectation)