def calculate_obligation_ratio(
    net_monthly_income,
    existing_monthly_emi,
    proposed_emi
):
    if net_monthly_income <= 0:
        raise ValueError("Monthly income must be positive.")

    total_obligations = existing_monthly_emi + proposed_emi

    ratio = (total_obligations / net_monthly_income) * 100

    return {
        "total_monthly_obligations": round(total_obligations, 2),
        "obligation_ratio": round(ratio, 2)
    }


def evaluate_affordability(obligation_ratio, threshold=40):
    if obligation_ratio < 0:
        raise ValueError("Obligation ratio cannot be negative.")

    affordable = obligation_ratio <= threshold

    return {
        "verdict": "AFFORDABLE" if affordable else "NOT AFFORDABLE",
        "threshold": threshold,
        "message": (
            "Applicant meets the affordability criteria."
            if affordable
            else "Applicant exceeds the 40% affordability limit."
        )
    }