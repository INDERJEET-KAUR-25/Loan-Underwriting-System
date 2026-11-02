
def extract_application_details(application):
    """
    Extract financial information from the loan application.
    """

    extracted_data = {
        "net_monthly_income": application.get("monthly_income"),
        "existing_monthly_emi": application.get("existing_monthly_emi"),
        "requested_loan_amount": application.get("loan_amount"),
        "tenure_months": application.get("tenure_months"),
        "annual_interest_rate": application.get("annual_interest_rate")
    }

    return extracted_data


def validate_application_details(extracted_data):
    """
    Validate the extracted financial information.
    """

    required_fields = [
        "net_monthly_income",
        "existing_monthly_emi",
        "requested_loan_amount",
        "tenure_months",
        "annual_interest_rate"
    ]

    missing_fields = []

    for field in required_fields:
        value = extracted_data.get(field)

        if value is None:
            missing_fields.append(field)

    if missing_fields:
        return {
            "valid": False,
            "missing_fields": missing_fields,
            "message": "Required application information is missing."
        }

    # Check numeric values and valid ranges
    for field in required_fields:
        value = extracted_data[field]

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return {
                "valid": False,
                "missing_fields": [],
                "message": f"Invalid numeric value for {field}."
            }

    if extracted_data["net_monthly_income"] <= 0:
        return {"valid": False, "missing_fields": [], "message": "Monthly income must be positive."}

    if extracted_data["existing_monthly_emi"] < 0:
        return {"valid": False, "missing_fields": [], "message": "Existing EMI cannot be negative."}

    if extracted_data["requested_loan_amount"] <= 0:
        return {"valid": False, "missing_fields": [], "message": "Loan amount must be positive."}

    if extracted_data["tenure_months"] <= 0 or not isinstance(extracted_data["tenure_months"], int):
        return {"valid": False, "missing_fields": [], "message": "Tenure must be a positive integer."}

    if extracted_data["annual_interest_rate"] < 0:
        return {"valid": False, "missing_fields": [], "message": "Interest rate cannot be negative."}

    return {
        "valid": True,
        "missing_fields": [],
        "message": "Application details are valid."
    }
