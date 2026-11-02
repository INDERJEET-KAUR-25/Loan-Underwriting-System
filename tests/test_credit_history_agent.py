from memory.applicant_record import ApplicantRecord
from agents.credit_history_agent import CreditHistoryAgent


def test_credit_history_agent():

    applicant = ApplicantRecord(
        applicant_id="APP001",
        application={}
    )

    agent = CreditHistoryAgent()

    result = agent.process(applicant)

    assert result["status"] == "CLEAR"
    assert applicant.credit_status == "CLEAR"

    print("\nCredit-History Agent test passed!")


if __name__ == "__main__":
    test_credit_history_agent()