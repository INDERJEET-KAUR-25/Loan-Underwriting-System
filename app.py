
import json
from pathlib import Path

import streamlit as st

from memory.applicant_record import ApplicantRecord
from agents.underwriting_manager import UnderwritingManager


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LoanSphere | Loan Underwriting",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROJECT_DIR = Path(__file__).resolve().parent
LOG_FILE = PROJECT_DIR / "logs" / "run_log.jsonl"


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #f4f7fb;
    }

    [data-testid="stSidebar"] {
        background-color: #10243a;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff;
    }

    .brand {
        font-size: 27px;
        font-weight: 800;
        color: #ffffff;
        padding: 10px 0 2px 0;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #bdcddd;
        margin-bottom: 25px;
    }

    .main-header {
        background: linear-gradient(110deg, #10243a, #1d4568);
        padding: 28px 32px;
        border-radius: 14px;
        color: white;
        margin-bottom: 25px;
    }

    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 30px;
    }

    .main-header p {
        color: #dce8f3;
        margin: 8px 0 0 0;
        font-size: 15px;
    }

    .section-heading {
        color: #183650;
        font-size: 21px;
        font-weight: 700;
        margin-top: 12px;
        margin-bottom: 12px;
    }

    .info-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e9f1;
        min-height: 115px;
        margin-bottom: 12px;
    }

    .info-card h3 {
        color: #183650;
        font-size: 16px;
        margin: 0 0 8px 0;
    }

    .info-card p {
        color: #60758a;
        font-size: 13px;
        margin: 0;
    }

    .decision-card {
        background: white;
        border: 1px solid #e2e9f1;
        border-radius: 12px;
        padding: 22px;
        margin: 10px 0 20px 0;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e9f1;
        padding: 15px;
        border-radius: 10px;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background-color: #174b72;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 10px 18px;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background-color: #23638f;
        color: white;
        border: none;
    }

    .footer {
        text-align: center;
        color: #8293a5;
        font-size: 12px;
        padding: 25px 0 10px 0;
    }

    #MainMenu, footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def load_application_history():
    if not LOG_FILE.exists():
        return []

    records = []

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return records


def show_header(title, subtitle):
    st.markdown(
        f"""
        <div class="main-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_decision(decision):
    if decision == "SANCTION":
        st.success("✓ LOAN SANCTIONED — All checks passed.")
    elif decision == "DECLINE":
        st.error("✕ LOAN DECLINED — Affordability criteria not satisfied.")
    else:
        st.warning("! APPLICATION REFERRED — Further review is required.")


def display_result(result):
    decision = result.get("decision", "REFER")

    show_decision(decision)

    st.markdown('<div class="section-heading">Financial Summary</div>',
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    emi = result.get("computed_emi")
    obligations = result.get("total_monthly_obligations")
    ratio = result.get("emi_to_income_ratio")

    with col1:
        st.metric(
            "Monthly EMI",
            f"₹{emi:,.2f}" if emi is not None else "Not calculated"
        )

    with col2:
        st.metric(
            "Total Monthly Obligations",
            f"₹{obligations:,.2f}" if obligations is not None else "Not calculated"
        )

    with col3:
        st.metric(
            "Obligation-to-Income Ratio",
            f"{ratio:.2f}%" if ratio is not None else "Not calculated"
        )

    st.markdown('<div class="section-heading">Assessment Overview</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Affordability Assessment**")
        st.write(result.get("affordability_verdict") or "Not evaluated")

    with col2:
        st.markdown("**Credit-History Assessment**")
        st.write(result.get("credit_status") or "Not evaluated")

    st.markdown('<div class="section-heading">Decision Justification</div>',
                unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="decision-card">
            {result.get("justification") or "No justification available."}
        </div>
        """,
        unsafe_allow_html=True
    )

    if result.get("credit_reasons"):
        st.markdown("**Credit-History Findings**")
        for reason in result["credit_reasons"]:
            st.write(f"- {reason}")

    with st.expander("View Multi-Agent Execution Trace"):
        for index, message in enumerate(result.get("trace", []), start=1):
            st.write(f"**Step {index}.** {message}")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.markdown(
    """
    <div class="brand">🏦 LoanSphere</div>
    <div class="brand-subtitle">MULTI-AGENT LOAN UNDERWRITING</div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "MAIN MENU",
    [
        "Dashboard",
        "New Application",
        "Application History",
        "About System"
    ]
)

st.sidebar.divider()
st.sidebar.caption("CSE476 | Agentic AI Project")
st.sidebar.caption("Powered by Python & Semantic Kernel")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    show_header(
        "Loan Underwriting Dashboard",
        "Intelligent loan assessment through collaborative AI agents."
    )

    history = load_application_history()

    total = len(history)
    sanctioned = sum(1 for r in history if r.get("decision") == "SANCTION")
    declined = sum(1 for r in history if r.get("decision") == "DECLINE")
    referred = sum(1 for r in history if r.get("decision") == "REFER")

    st.markdown('<div class="section-heading">Application Statistics</div>',
                unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Applications", total)
    c2.metric("Sanctioned", sanctioned)
    c3.metric("Declined", declined)
    c4.metric("Referred", referred)

    st.markdown('<div class="section-heading">Our Multi-Agent System</div>',
                unsafe_allow_html=True)

    agent_data = [
        ("01 | Document Agent",
         "Extracts and validates applicant and loan information."),
        ("02 | EMI Computation Agent",
         "Calculates reducing-balance EMI and total repayment."),
        ("03 | Affordability Agent",
         "Evaluates monthly obligations against the 40% income threshold."),
        ("04 | Credit-History Agent",
         "Checks previous records for defaults and missed payments."),
        ("05 | Underwriting Manager",
         "Coordinates specialist agents and generates the final decision.")
    ]

    for start in range(0, len(agent_data), 2):
        columns = st.columns(2)

        for column, (name, description) in zip(
            columns, agent_data[start:start + 2]
        ):
            with column:
                st.markdown(
                    f"""
                    <div class="info-card">
                        <h3>{name}</h3>
                        <p>{description}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.info(
        "Select 'New Application' from the sidebar to evaluate a loan application."
    )

    if history:
        st.markdown('<div class="section-heading">Recent Applications</div>',
                    unsafe_allow_html=True)

        for record in reversed(history[-5:]):
            st.write(
                f"**{record.get('applicant_id', 'Unknown')}** — "
                f"{record.get('decision', 'Unknown')} — "
                f"{record.get('timestamp', '')}"
            )


# --------------------------------------------------
# NEW APPLICATION
# --------------------------------------------------

elif page == "New Application":

    show_header(
        "New Loan Application",
        "Enter applicant details to initiate the multi-agent assessment."
    )

    with st.form("loan_application_form"):

        st.markdown("### Applicant Information")

        applicant_id = st.text_input(
            "Applicant ID",
            placeholder="Example: APP001"
        )

        income_not_available = st.checkbox(
            "Monthly income details are not available"
        )

        col1, col2 = st.columns(2)

        with col1:
            monthly_income = st.number_input(
                "Net Monthly Income (₹)",
                min_value=0.0,
                value=70000.0,
                step=1000.0,
                disabled=income_not_available
            )

        with col2:
            existing_emi = st.number_input(
                "Existing Monthly EMI (₹)",
                min_value=0.0,
                value=5000.0,
                step=500.0
            )

        st.markdown("### Loan Requirements")

        col1, col2 = st.columns(2)

        with col1:
            loan_amount = st.number_input(
                "Requested Loan Amount (₹)",
                min_value=0.0,
                value=500000.0,
                step=10000.0
            )

            tenure = st.number_input(
                "Loan Tenure (Months)",
                min_value=0,
                value=36,
                step=1
            )

        with col2:
            interest_rate = st.number_input(
                "Annual Interest Rate (%)",
                min_value=0.0,
                value=10.0,
                step=0.5
            )

        submitted = st.form_submit_button(
            "Evaluate Application",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if not applicant_id.strip():
            st.error("Please enter an Applicant ID.")

        else:
            application = {
                "existing_monthly_emi": existing_emi,
                "loan_amount": loan_amount,
                "tenure_months": tenure,
                "annual_interest_rate": interest_rate
            }

            if not income_not_available:
                application["monthly_income"] = monthly_income

            applicant = ApplicantRecord(
                applicant_id=applicant_id.strip(),
                application=application
            )

            try:
                with st.spinner(
                    "Our AI agents are evaluating the application..."
                ):
                    manager = UnderwritingManager()
                    assessed_applicant = manager.process_application(applicant)

                st.session_state["latest_result"] = assessed_applicant.to_dict()

            except Exception as error:
                st.error(f"Assessment failed: {error}")

    if "latest_result" in st.session_state:
        st.divider()
        st.markdown("### Latest Assessment")
        display_result(st.session_state["latest_result"])


# --------------------------------------------------
# APPLICATION HISTORY
# --------------------------------------------------

elif page == "Application History":

    show_header(
        "Application History",
        "Review previously assessed loan applications."
    )

    history = load_application_history()

    if not history:
        st.info("No applications have been processed yet.")

    else:
        st.metric("Total Applications Processed", len(history))

        for record in reversed(history):

            applicant = record.get("applicant_id", "Unknown")
            decision = record.get("decision", "Unknown")

            with st.expander(f"{applicant} | {decision}"):

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Timestamp:**", record.get("timestamp", "N/A"))
                    st.write("**Decision:**", decision)
                    st.write("**Credit Status:**", record.get("credit_status", "N/A"))

                with col2:
                    emi = record.get("computed_emi")
                    st.write(
                        "**Monthly EMI:**",
                        f"₹{emi:,.2f}" if emi is not None else "Not calculated"
                    )
                    st.write(
                        "**Affordability:**",
                        record.get("affordability_verdict", "N/A")
                    )

                st.write("**Justification:**", record.get("justification", "N/A"))

                with st.expander("Execution Trace"):
                    for step in record.get("trace", []):
                        st.write(f"- {step}")


# --------------------------------------------------
# ABOUT
# --------------------------------------------------

elif page == "About System":

    show_header(
        "About LoanSphere",
        "A multi-agent approach to automated loan underwriting."
    )

    st.markdown("### Project Description")

    st.write(
        "LoanSphere is an academic Agentic AI project that uses multiple "
        "specialized agents to evaluate loan applications. Each agent "
        "performs a specific task, while the Underwriting Manager coordinates "
        "their results to generate a final decision."
    )

    st.markdown("### Technology Stack")

    st.write("- Python")
    st.write("- Microsoft Semantic Kernel")
    st.write("- Streamlit")
    st.write("- JSON-based credit-history memory")
    st.write("- JSONL append-only execution logs")

    st.markdown("### Decision Outcomes")

    st.success("SANCTION — Required information is valid, affordability passes, and credit history is clear.")

    st.error("DECLINE — The affordability threshold is exceeded.")

    st.warning("REFER — Required information is missing or credit history requires further review.")

    st.markdown("### Assessment Rules")

    st.write("- EMI is calculated using the reducing-balance method.")
    st.write("- Affordability threshold: 40% of net monthly income.")
    st.write("- Missing required information results in referral.")
    st.write("- Unknown or risky credit history results in referral.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        LoanSphere | Multi-Agent Loan Underwriting System | CSE476
    </div>
    """,
    unsafe_allow_html=True
)
