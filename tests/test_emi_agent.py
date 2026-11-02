
from memory.applicant_record import ApplicantRecord
from agents.emi_agent import EMIAgent


def test_emi_agent():

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

    # First extract the application details
    from agents.document_agent import DocumentAgent

    document_agent = DocumentAgent()
    validation = document_agent.process(applicant)

    assert validation["valid"] is True

    # Run EMI Agent
    emi_agent = EMIAgent()
    repayment = emi_agent.process(applicant)

    assert applicant.computed_emi is not None
    assert applicant.computed_emi > 0
    assert repayment["total_repayment"] > 500000
    assert repayment["total_interest"] > 0

    print("\nEMI Agent test passed!")


if __name__ == "__main__":
    test_emi_agent()
