
def calculate_emi(principal, annual_interest_rate, tenure_months):
    """
    Calculate monthly EMI using the reducing-balance method.
    """

    if principal <= 0:
        raise ValueError("Loan amount must be positive.")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if tenure_months <= 0:
        raise ValueError("Tenure must be positive.")

    monthly_rate = annual_interest_rate / (12 * 100)

    # Special case: zero interest rate
    if monthly_rate == 0:
        return round(principal / tenure_months, 2)

    emi = (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** tenure_months
    ) / (
        (1 + monthly_rate) ** tenure_months - 1
    )

    return round(emi, 2)


def calculate_total_repayment(emi, tenure_months, principal):
    """
    Calculate total repayment and total interest.
    """

    if emi <= 0 or tenure_months <= 0 or principal <= 0:
        raise ValueError("Invalid values for repayment calculation.")

    total_repayment = emi * tenure_months
    total_interest = total_repayment - principal

    return {
        "total_repayment": round(total_repayment, 2),
        "total_interest": round(total_interest, 2)
    }
