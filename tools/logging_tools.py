import json
from pathlib import Path
from datetime import datetime


LOG_FILE = (
    Path(__file__).resolve().parent.parent
    / "logs"
    / "run_log.jsonl"
)


def append_run_log(applicant):
    """
    Appends one completed application record to the run log.
    Existing log entries are never overwritten.
    """

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "applicant_id": applicant.applicant_id,
        "decision": applicant.decision,
        "computed_emi": applicant.computed_emi,
        "affordability_verdict": applicant.affordability_verdict,
        "credit_status": applicant.credit_status,
        "justification": applicant.justification,
        "trace": applicant.trace
    }

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return str(LOG_FILE)