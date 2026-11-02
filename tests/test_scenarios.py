
from memory.applicant_record import ApplicantRecord
from agents.underwriting_manager import UnderwritingManager


def run_application(applicant_id, application):
    applicant = ApplicantRecord(
        applicant_id=applicant_id,
        application=application
    )

    manager = UnderwritingManager()
    return manager.process_application(applicant)


def test_successful_sanction():

    application = {
        "monthly_income": 70000,
        "existing_monthly_emi": 5000,
        "loan_amount": 500000,
        "tenure_months": 36,
        "annual_interest_rate": 10
    }

    result = run_application("APP001", application)

    assert result.decision == "SANCTION"
    assert result.credit_status == "CLEAR"
    assert result.affordability_verdict == "AFFORDABLE"

    print("\nScenario 1: SANCTION test passed!")


def test_affordability_decline():

    application = {
        "monthly_income": 50000,
        "existing_monthly_emi": 5000,
        "loan_amount": 500000,
        "tenure_months": 36,
        "annual_interest_rate": 10
    }

    result = run_application("TEST003", application)

    assert result.decision == "DECLINE"
    assert result.affordability_verdict == "NOT AFFORDABLE"

    print("\nScenario 2: DECLINE test passed!")


def test_missing_income_referral():

    application = {
        "existing_monthly_emi": 5000,
        "loan_amount": 500000,
        "tenure_months": 36,
        "annual_interest_rate": 10
    }

    result = run_application("NEW001", application)

    assert result.decision == "REFER"
    assert result.computed_emi is None
    assert result.affordability_verdict is None

    print("\nScenario 3: Missing income referral test passed!")


def test_credit_risk_referral():

    application = {
        "monthly_income": 70000,
        "existing_monthly_emi": 5000,
        "loan_amount": 500000,
        "tenure_months": 36,
        "annual_interest_rate": 10
    }

    result = run_application("APP002", application)

    assert result.decision == "REFER"
    assert result.credit_status == "RISK"

    print("\nScenario 4: Credit risk referral test passed!")


if __name__ == "__main__":

    test_successful_sanction()
    test_affordability_decline()
    test_missing_income_referral()
    test_credit_risk_referral()

    print("\nAll four loan scenarios passed!")
