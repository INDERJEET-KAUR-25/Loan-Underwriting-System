
from memory.applicant_record import ApplicantRecord

# Create a sample applicant
applicant = ApplicantRecord(
    applicant_id="APP001",
    application={
        "monthly_income": 50000,
        "existing_monthly_emi": 5000,
        "loan_amount": 500000,
        "tenure_months": 36,
        "annual_interest_rate": 10
    }
)

# Simulate an agent updating shared memory
applicant.net_monthly_income = 50000
applicant.computed_emi = 16134.73

applicant.add_trace("Document Agent extracted applicant information.")
applicant.add_trace("EMI Agent calculated the monthly EMI.")

# Display the record
print("APPLICANT RECORD")
print("----------------")
print(applicant.to_dict())

print("\nAGENT TRACE")
for event in applicant.trace:
    print("-", event)
