
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any


@dataclass
class ApplicantRecord:
    """
    Shared memory record used by all agents
    during the loan underwriting process.
    """

    # Applicant information
    applicant_id: str
    application: Dict[str, Any]

    # Extracted financial information
    net_monthly_income: Optional[float] = None
    existing_monthly_emi: Optional[float] = None
    requested_loan_amount: Optional[float] = None
    tenure_months: Optional[int] = None
    annual_interest_rate: Optional[float] = None

    # EMI computation results
    computed_emi: Optional[float] = None
    total_monthly_obligations: Optional[float] = None

    # Affordability results
    affordability_verdict: Optional[str] = None
    emi_to_income_ratio: Optional[float] = None

    # Credit history results
    credit_status: Optional[str] = None
    credit_reasons: List[str] = field(default_factory=list)

    # Final underwriting results
    decision: Optional[str] = None
    justification: Optional[str] = None

    # Agent execution trace
    trace: List[str] = field(default_factory=list)

    def add_trace(self, message: str):
        """Record an agent's activity."""
        self.trace.append(message)

    def to_dict(self):
        """Convert the shared record into a dictionary."""
        return asdict(self)
