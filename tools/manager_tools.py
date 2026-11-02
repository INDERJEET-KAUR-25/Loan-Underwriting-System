
def validate_specialist_results(
    computed_emi,
    affordability_verdict,
    credit_status
):
    missing = []

    if computed_emi is None or computed_emi <= 0:
        missing.append("Computed EMI")

    if affordability_verdict not in ["AFFORDABLE", "NOT AFFORDABLE"]:
        missing.append("Affordability verdict")

    if credit_status not in ["CLEAR", "RISK", "UNKNOWN"]:
        missing.append("Credit status")

    return {
        "valid": len(missing) == 0,
        "missing_results": missing
    }


def create_decision_record(
    decision,
    justification,
    computed_emi,
    affordability_verdict
):
    return {
        "decision": decision,
        "justification": justification,
        "computed_emi": computed_emi,
        "affordability_verdict": affordability_verdict
    }
