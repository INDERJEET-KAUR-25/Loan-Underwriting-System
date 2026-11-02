from semantic_kernel.functions import kernel_function

from tools.affordability_tools import (
    calculate_obligation_ratio,
    evaluate_affordability
)


class AffordabilityAgent:

    def __init__(self):
        self.name = "Affordability Agent"

    @kernel_function(
        name="calculate_obligation_ratio",
        description="Calculates the applicant's monthly obligation ratio."
    )
    def calculate_ratio(
        self,
        net_monthly_income: float,
        existing_monthly_emi: float,
        proposed_emi: float
    ) -> dict:

        return calculate_obligation_ratio(
            net_monthly_income,
            existing_monthly_emi,
            proposed_emi
        )

    @kernel_function(
        name="evaluate_affordability",
        description="Checks affordability using a 40 percent threshold."
    )
    def evaluate(self, obligation_ratio: float) -> dict:

        return evaluate_affordability(obligation_ratio)

    def process(self, applicant):

        print("\n[Affordability Agent] Evaluating loan affordability...")

        result = self.calculate_ratio(
            applicant.net_monthly_income,
            applicant.existing_monthly_emi,
            applicant.computed_emi
        )

        applicant.total_monthly_obligations = (
            result["total_monthly_obligations"]
        )

        applicant.emi_to_income_ratio = result["obligation_ratio"]

        verdict = self.evaluate(result["obligation_ratio"])

        applicant.affordability_verdict = verdict["verdict"]

        applicant.add_trace(
            "Affordability Agent calculated monthly obligation ratio."
        )

        applicant.add_trace(
            f"Affordability verdict: {verdict['verdict']}"
        )

        print(f"Total monthly obligations: ₹{applicant.total_monthly_obligations}")
        print(f"Obligation ratio: {applicant.emi_to_income_ratio}%")
        print(f"Verdict: {applicant.affordability_verdict}")

        return verdict