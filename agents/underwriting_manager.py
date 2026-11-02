
from semantic_kernel.functions import kernel_function

from agents.document_agent import DocumentAgent
from agents.emi_agent import EMIAgent
from agents.affordability_agent import AffordabilityAgent
from agents.credit_history_agent import CreditHistoryAgent
from tools.logging_tools import append_run_log

from tools.manager_tools import (
    validate_specialist_results,
    create_decision_record
)


class UnderwritingManager:

    def __init__(self):
        self.name = "Underwriting Manager"

        self.document_agent = DocumentAgent()
        self.emi_agent = EMIAgent()
        self.affordability_agent = AffordabilityAgent()
        self.credit_agent = CreditHistoryAgent()

    @kernel_function(
        name="validate_specialist_results",
        description="Checks whether all specialist agents returned valid results."
    )
    def validate_results(
        self,
        computed_emi: float,
        affordability_verdict: str,
        credit_status: str
    ) -> dict:

        return validate_specialist_results(
            computed_emi,
            affordability_verdict,
            credit_status
        )

    @kernel_function(
        name="create_decision_record",
        description="Creates a structured final loan decision record."
    )
    def create_record(
        self,
        decision: str,
        justification: str,
        computed_emi: float,
        affordability_verdict: str
    ) -> dict:

        return create_decision_record(
            decision,
            justification,
            computed_emi,
            affordability_verdict
        )

    def process_application(self, applicant):

        print("\n========== UNDERWRITING MANAGER ==========")

        applicant.add_trace(
            "Underwriting Manager received application."
        )

        # Step 1: Document verification
        print("\n[Manager] Delegating to Document Agent...")

        validation = self.document_agent.process(applicant)

        if not validation["valid"]:

            applicant.decision = "REFER"

            applicant.justification = (
                "Application referred because required information "
                "is missing or invalid: "
                + ", ".join(validation["missing_fields"])
            )

            applicant.add_trace(
                "Manager stopped processing due to invalid or incomplete details."
            )

            return self.finalize_decision(applicant)

        # Step 2: EMI computation
        print("\n[Manager] Delegating to EMI Computation Agent...")

        self.emi_agent.process(applicant)

        # Step 3: Affordability evaluation
        print("\n[Manager] Delegating to Affordability Agent...")

        affordability = self.affordability_agent.process(applicant)

        # Step 4: Credit-history verification
        print("\n[Manager] Delegating to Credit-History Agent...")

        credit = self.credit_agent.process(applicant)

        # Step 5: Validate specialist results
        print("\n[Manager] Validating specialist results...")

        specialist_validation = self.validate_results(
            applicant.computed_emi,
            applicant.affordability_verdict,
            applicant.credit_status
        )

        if not specialist_validation["valid"]:

            applicant.decision = "REFER"

            applicant.justification = (
                "Manual review required because specialist results "
                "are incomplete: "
                + ", ".join(
                    specialist_validation["missing_results"]
                )
            )

            applicant.add_trace(
                "Manager referred application due to incomplete specialist results."
            )

            return self.finalize_decision(applicant)

        # Step 6: Final decision
        print("\n[Manager] Evaluating specialist results...")

        if affordability["verdict"] == "NOT AFFORDABLE":

            applicant.decision = "DECLINE"

            applicant.justification = (
                f"Total monthly obligations are "
                f"{applicant.emi_to_income_ratio}% of net monthly income, "
                "which exceeds the permitted 40% threshold."
            )

        elif credit["status"] in ["RISK", "UNKNOWN"]:

            applicant.decision = "REFER"

            applicant.justification = (
                "Application requires manual credit review. "
                + " ".join(credit["reasons"])
            )

        else:

            applicant.decision = "SANCTION"

            applicant.justification = (
                "Application satisfies document verification, "
                "affordability requirements, and credit-history checks."
            )

        applicant.add_trace(
            f"Underwriting Manager made final decision: "
            f"{applicant.decision}"
        )

        return self.finalize_decision(applicant)

    def finalize_decision(self, applicant):

        print("\n========== FINAL LOAN DECISION ==========")

        print(f"Applicant ID: {applicant.applicant_id}")
        print(f"Decision: {applicant.decision}")
        print(f"Computed EMI: ₹{applicant.computed_emi}")
        print(
            f"Affordability verdict: "
            f"{applicant.affordability_verdict}"
        )
        print(f"Justification: {applicant.justification}")

        # Create structured decision record
        decision_record = self.create_record(
            applicant.decision,
            applicant.justification,
            applicant.computed_emi or 0.0,
            applicant.affordability_verdict or "NOT EVALUATED"
        )

        applicant.add_trace(
            f"Decision record created: {decision_record['decision']}"
        )

        applicant.add_trace("Final decision generated.")
                # Append application details to the permanent run log
        log_path = append_run_log(applicant)

        print(f"Run log updated: {log_path}")

        return applicant
