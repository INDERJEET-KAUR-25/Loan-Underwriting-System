import json
from pathlib import Path


CREDIT_FILE = Path(__file__).resolve().parent.parent / "memory" / "credit_records.json"


def lookup_credit_record(applicant_id):
    with open(CREDIT_FILE, "r") as file:
        records = json.load(file)

    return records.get(applicant_id)


def evaluate_credit_history(credit_record):
    if credit_record is None:
        return {
            "status": "UNKNOWN",
            "reasons": ["No previous credit record found."]
        }

    reasons = []

    if credit_record["defaults"] > 0:
        reasons.append("Previous loan default found.")

    if credit_record["missed_payments"] >= 3:
        reasons.append("Multiple missed payments found.")

    if reasons:
        return {
            "status": "RISK",
            "reasons": reasons
        }

    return {
        "status": "CLEAR",
        "reasons": ["No major credit red flags found."]
    }