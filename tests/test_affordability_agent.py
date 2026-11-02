from memory.applicant_record import ApplicantRecord
from agents.document_agent import DocumentAgent
from agents.emi_agent import EMIAgent
from agents.affordability_agent import AffordabilityAgent


def test_affordability_agent():

    application = {
        "monthly_income": 50000,
        "existing_monthly_emi": 5000,
        "loan_amount": 500000,
        "tenure_months": 36,
        "annual_interest_rate": 10
    }

    applicant = ApplicantRecord(
        applicant_id="TEST003",
        application=application
    )

    document_agent = DocumentAgent()
    validation = document_agent.process(applicant)

    assert validation["valid"] is True

    emi_agent = EMIAgent()
    emi_agent.process(applicant)

    affordability_agent = AffordabilityAgent()
    result = affordability_agent.process(applicant)

    assert result["verdict"] == "NOT AFFORDABLE"
    assert applicant.emi_to_income_ratio > 40

    print("\nAffordability Agent test passed!")


if __name__ == "__main__":
    test_affordability_agent()