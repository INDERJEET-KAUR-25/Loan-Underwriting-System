from memory.applicant_record import ApplicantRecord
from agents.underwriting_manager import UnderwritingManager


def test_underwriting_manager():

    application = {
        "monthly_income": 70000,
        "existing_monthly_emi": 5000,
        "loan_amount": 500000,
        "tenure_months": 36,
        "annual_interest_rate": 10
    }

    applicant = ApplicantRecord(
        applicant_id="APP001",
        application=application
    )

    manager = UnderwritingManager()

    result = manager.process_application(applicant)

    assert result.decision == "SANCTION"
    assert result.computed_emi > 0
    assert result.affordability_verdict == "AFFORDABLE"
    assert result.credit_status == "CLEAR"

    print("\nUnderwriting Manager test passed!")


if __name__ == "__main__":
    test_underwriting_manager()