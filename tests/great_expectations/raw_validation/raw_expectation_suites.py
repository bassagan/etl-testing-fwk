import great_expectations as gx
import great_expectations.expectations as gxe

class RawExpectationSuiteManager:
    def __init__(self, context):
        self.context = context
        self.patients_suite = None
        self.visits_suite = None

    def setup_suites(self):
        self.patients_suite = self._get_or_create_suite("raw_patients_data_suite")
        self.visits_suite = self._get_or_create_suite("raw_visits_data_suite")
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
            gxe.ExpectColumnValuesToBeUnique(column="patient_id"),
            gxe.ExpectColumnValuesToMatchRegex(column="patient_id", regex=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'),
            gxe.ExpectColumnValuesToNotBeNull(column="name"),
            gxe.ExpectColumnValueLengthsToBeBetween(column="name", min_value=2, max_value=100),
            gxe.ExpectColumnValuesToNotBeNull(column="address"),
            gxe.ExpectColumnValuesToNotBeNull(column="phone_number"),
            gxe.ExpectColumnValuesToMatchRegex(column="email", regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
            gxe.ExpectColumnValuesToNotBeNull(column="insurance_provider"),
            gxe.ExpectColumnValuesToNotBeNull(column="policy_number"),
            gxe.ExpectColumnValuesToBeOfType(column="record_created_at", type_="datetime64"),
            gxe.ExpectColumnValuesToBeOfType(column="record_updated_at", type_="datetime64"),
        ]
        for expectation in patient_expectations:
            self.patients_suite.add_expectation(expectation)

    def _add_visit_expectations(self):
        visit_expectations = [
            gxe.ExpectColumnValuesToNotBeNull(column="appointment_id"),
            gxe.ExpectColumnValuesToBeUnique(column="appointment_id"),
            gxe.ExpectColumnValuesToMatchRegex(column="appointment_id", regex=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'),
            gxe.ExpectColumnValuesToNotBeNull(column="patient_id"),
            gxe.ExpectColumnValuesToMatchRegex(column="patient_id", regex=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'),
            gxe.ExpectColumnValuesToNotBeNull(column="doctor"),
            gxe.ExpectColumnValuesToNotBeNull(column="department"),
            gxe.ExpectColumnValuesToBeInSet(column="purpose", value_set=["Consultation", "Follow-up", "Routine Checkup", "Specialist Referral"]),
            gxe.ExpectColumnValuesToBeInSet(column="status", value_set=["Scheduled", "Completed", "Cancelled"]),
            gxe.ExpectColumnValuesToBeOfType(column="record_created_at", type_="datetime64"),
            gxe.ExpectColumnValuesToBeOfType(column="record_updated_at", type_="datetime64"),
        ]
        for expectation in visit_expectations:
            self.visits_suite.add_expectation(expectation)