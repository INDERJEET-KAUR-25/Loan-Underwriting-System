from semantic_kernel.functions import kernel_function

from tools.credit_tools import (
    lookup_credit_record,
    evaluate_credit_history
)


class CreditHistoryAgent:

    def __init__(self):
        self.name = "Credit-History Agent"

    @kernel_function(
        name="lookup_credit_record",
        description="Retrieves an applicant's previous credit history."
    )
    def lookup_record(self, applicant_id: str) -> dict:
        return lookup_credit_record(applicant_id)

    @kernel_function(
        name="evaluate_credit_history",
        description="Checks the credit record for defaults and missed payments."
    )
    def evaluate_record(self, credit_record: dict) -> dict:
        return evaluate_credit_history(credit_record)

    def process(self, applicant):

        print("\n[Credit-History Agent] Checking credit history...")

        record = self.lookup_record(applicant.applicant_id)

        result = self.evaluate_record(record)

        applicant.credit_status = result["status"]
        applicant.credit_reasons = result["reasons"]

        applicant.add_trace(
            "Credit-History Agent retrieved the applicant's credit record."
        )

        applicant.add_trace(
            f"Credit status: {applicant.credit_status}"
        )

        print(f"Credit status: {applicant.credit_status}")

        for reason in applicant.credit_reasons:
            print(f"- {reason}")

        return result