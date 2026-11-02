
from semantic_kernel.functions import kernel_function

from tools.document_tools import (
    extract_application_details,
    validate_application_details
)


class DocumentAgent:

    def __init__(self):
        self.name = "Document Agent"

    @kernel_function(
        name="extract_details",
        description="Extract financial details from a loan application."
    )
    def extract_details(self, application: dict) -> dict:
        return extract_application_details(application)

    @kernel_function(
        name="validate_details",
        description="Validate extracted financial information."
    )
    def validate_details(self, extracted_data: dict) -> dict:
        return validate_application_details(extracted_data)

    def process(self, applicant):
        print("\n[Document Agent] Processing application...")

        # Tool 1: Extract application details
        extracted_data = self.extract_details(applicant.application)

        # Update shared memory
        applicant.net_monthly_income = extracted_data["net_monthly_income"]
        applicant.existing_monthly_emi = extracted_data["existing_monthly_emi"]
        applicant.requested_loan_amount = extracted_data["requested_loan_amount"]
        applicant.tenure_months = extracted_data["tenure_months"]
        applicant.annual_interest_rate = extracted_data["annual_interest_rate"]

        applicant.add_trace("Document Agent: Extracted application details.")

        # Tool 2: Validate extracted information
        validation_result = self.validate_details(extracted_data)

        applicant.add_trace("Document Agent: Validated application details.")

        print("Extracted details:", extracted_data)
        print("Validation result:", validation_result)

        return validation_result
