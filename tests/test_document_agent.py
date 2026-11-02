
from memory.applicant_record import ApplicantRecord
from agents.document_agent import DocumentAgent


def test_document_agent():
    application = {
        "monthly_income": 50000,
        "existing_monthly_emi": 5000,
        "loan_amount": 500000,
        "tenure_months": 36,
        "annual_interest_rate": 10
    }

    applicant = ApplicantRecord(
        applicant_id="APP001",
        application=application
    )

    agent = DocumentAgent()
    result = agent.process(applicant)

    assert result["valid"] is True
    assert applicant.net_monthly_income == 50000
    assert applicant.existing_monthly_emi == 5000
    assert applicant.requested_loan_amount == 500000
    assert applicant.tenure_months == 36

    print("\nDocument Agent test passed!")


if __name__ == "__main__":
    test_document_agent()

