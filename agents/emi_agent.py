
from semantic_kernel.functions import kernel_function

from tools.emi_tools import (
    calculate_emi,
    calculate_total_repayment
)


class EMIAgent:

    def __init__(self):
        self.name = "EMI Computation Agent"

    @kernel_function(
        name="compute_monthly_emi",
        description="Calculate monthly loan EMI using reducing balance."
    )
    def compute_monthly_emi(
        self,
        principal: float,
        annual_interest_rate: float,
        tenure_months: int
    ) -> float:
        return calculate_emi(
            principal,
            annual_interest_rate,
            tenure_months
        )

    @kernel_function(
        name="compute_total_repayment",
        description="Calculate total repayment and interest."
    )
    def compute_total_repayment(
        self,
        emi: float,
        tenure_months: int,
        principal: float
    ) -> dict:
        return calculate_total_repayment(
            emi,
            tenure_months,
            principal
        )

    def process(self, applicant):

        print("\n[EMI Agent] Calculating loan EMI...")

        # Tool 1: Calculate monthly EMI
        emi = self.compute_monthly_emi(
            applicant.requested_loan_amount,
            applicant.annual_interest_rate,
            applicant.tenure_months
        )

        applicant.computed_emi = emi

        # Tool 2: Calculate total repayment
        repayment = self.compute_total_repayment(
            emi,
            applicant.tenure_months,
            applicant.requested_loan_amount
        )

        applicant.add_trace(
            "EMI Agent: Calculated monthly EMI."
        )

        applicant.add_trace(
            "EMI Agent: Calculated total repayment and interest."
        )

        print("Monthly EMI:", emi)
        print("Total repayment:", repayment["total_repayment"])
        print("Total interest:", repayment["total_interest"])

        return repayment
