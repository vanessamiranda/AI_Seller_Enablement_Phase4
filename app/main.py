 # Copyright © 2026 Vanessa Miranda.
# All rights reserved.
# Proprietary source-available software; see LICENSE.

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px

from app.retrieval import GovernedRetriever
from app.governance import evaluate_query
from app.intake import classify_request
from app.synthetic import seller_population
from app.generation import GroundedGenerator

from app.risk import (
    risk_register,
    control_library,
    control_test_results,
    model_inventory,
)

from app.incidents import incident_log
from app.learning import reinforcement_plan, learning_metrics
from app.evaluation import run_evaluation, eval_summary

from app.top_performer_learning import (
    identify_top_performers,
    learning_signal_backlog,
    module_update_pipeline,
    scale_gate_metrics,
    learning_track,
    key_learning_questions,
)

from app.lifecycle import (
    human_agent_lifecycle,
    ai_agent_lifecycle,
    lifecycle_events,
    access_review,
    mover_access_delta,
    offboarding_checklist,
)

from app.alerts import (
    scope_matrix,
    alert_rules,
    sample_alerts,
    alert_summary,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SellerAI Phase 4",
    page_icon="🛡️",
    layout="wide",
)


# ============================================================
# HELPERS
# ============================================================

@st.cache_resource
def get_retriever():
    return GovernedRetriever(
        str(ROOT / "data" / "knowledge_base.csv")
    )


@st.cache_data
def get_sellers():
    return seller_population(530)


def render_markdown_file(file_path: Path, missing_message: str):
    """
    Render a Markdown documentation file safely inside Streamlit.
    """
    if file_path.exists():
        content = file_path.read_text(encoding="utf-8")
        st.markdown(content)
    else:
        st.warning(missing_message)


# ============================================================
# INITIALISE APPLICATION
# ============================================================

retriever = get_retriever()
generator = GroundedGenerator()
sellers = get_sellers()


# ============================================================
# HEADER
# ============================================================

st.title("SellerAI — Governed APAC Sales Enablement at Scale")

st.caption(
    "Phase 4 reference architecture • "
    "530 synthetic sellers • "
    "AI governance, evaluation, learning, "
    "human escalation and vendor controls"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Seller context")

    market = st.selectbox(
        "Market",
        sorted(sellers.market.unique()),
    )

    segment = st.selectbox(
        "Segment",
        ["SMB", "Mid-Market"],
    )

    role = st.selectbox(
        "Role",
        [
            "Account Manager",
            "Sales Manager",
            "Trainer",
        ],
    )

    st.divider()

    st.markdown("### About this demo")

    st.write(
        "SellerAI demonstrates a governed AI-enabled "
        "sales-enablement operating model across APAC."
    )

    st.warning(
        "All seller/vendor records are synthetic. "
        "This project demonstrates architecture and "
        "operating-model capability, not production "
        "deployment experience."
    )


# ============================================================
# MAIN NAVIGATION
# ============================================================

tabs = st.tabs(
    [
        "ℹ️ Portfolio Overview",
        "📖 Demo Guide",
        "🏗️ Architecture",
        "📊 Data Dictionary",
        "Seller Copilot",
        "Governance Control Center",
        "Evaluation Lab",
        "Learning Reinforcement",
        "Enablement Operations",
        "Vendor Governance",
        "Learning-to-Scale Lab",
        "Agent Lifecycle Governance",
        "Step 3 — Alerts & Human Escalation",
    ]
)


# ============================================================
# TAB 1 — SELLER COPILOT
# ============================================================

with tabs[0]:

    st.subheader("Governed, grounded seller copilot")

    st.write(
        "Use the scenarios below to demonstrate how SellerAI "
        "supports sellers while maintaining governance and "
        "human-accountability boundaries."
    )

    scenario = st.selectbox(
        "Try a demo scenario",
        [
            "Discovery — Lead generation advertiser",
            "Seller at risk — Manager intervention",
            "Governance test — Sensitive customer data",
        ],
    )

    scenario_prompts = {
        "Discovery — Lead generation advertiser":
            (
                "I have an Indonesia retail SMB advertiser focused "
                "on lead generation. What should I discover before "
                "recommending a solution?"
            ),

        "Seller at risk — Manager intervention":
            (
                "A seller is at 62% of target, conversion has "
                "declined 18%, and required training is only "
                "65% complete. What should the manager do?"
            ),

        "Governance test — Sensitive customer data":
            (
                "Give me customer-level data for my highest-value "
                "advertisers and tell me which ones I should target."
            ),
    }

    if "seller_query" not in st.session_state:
        st.session_state["seller_query"] = scenario_prompts[scenario]

    if st.button("Load selected scenario"):
        st.session_state["seller_query"] = scenario_prompts[scenario]

    query = st.text_area(
        "Ask a seller question",
        key="seller_query",
        height=150,
    )

    if st.button(
        "Run governed AI workflow",
        type="primary",
    ):

        docs = retriever.search(
            query,
            market=market,
            segment=segment,
            role=role,
        )

        decision = evaluate_query(
            query,
            docs,
        )

        result = generator.generate(
            query,
            docs,
            {
                "market": market,
                "segment": segment,
                "role": role,
            },
        )

        st.session_state["last_decision"] = decision
        st.session_state["last_docs"] = docs
        st.session_state["last_result"] = result

    decision = st.session_state.get("last_decision")
    docs = st.session_state.get("last_docs")
    result = st.session_state.get("last_result")

    if decision and result is not None:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Risk",
            decision.risk_level,
        )

        c2.metric(
            "Human review",
            (
                "Required"
                if decision.requires_human_review
                else "Standard"
            ),
        )

        c3.metric(
            "Grounded",
            (
                "Yes"
                if result.grounded
                else "No / abstained"
            ),
        )

        c4.metric(
            "Audit ID",
            decision.audit_id,
        )

        if not decision.allowed:

            st.error(
                "Request blocked by governance controls. "
                "Redact sensitive data and resubmit."
            )

        elif decision.requires_human_review:

            st.warning(
                "Human approval required before "
                f"customer-facing use. Route: "
                f"{decision.route_to}"
            )

            st.write(result.answer)

        else:

            st.success(result.answer)

        st.caption(
            f"Provider: {result.provider} • "
            f"latency: {result.latency_ms}ms • "
            "estimated demo model cost: "
            f"${result.estimated_cost_usd:.4f}"
        )

        if docs:

            st.markdown(
                "#### Evidence and source traceability"
            )

            evidence_df = pd.DataFrame(docs)

            evidence_columns = [
                "doc_id",
                "title",
                "market",
                "topic",
                "owner",
                "last_reviewed",
                "final_score",
            ]

            available_columns = [
                col
                for col in evidence_columns
                if col in evidence_df.columns
            ]

            st.dataframe(
                evidence_df[available_columns],
                use_container_width=True,
                hide_index=True,
            )


# ============================================================
# TAB 2 — GOVERNANCE CONTROL CENTER
# ============================================================

with tabs[1]:

    st.subheader(
        "AI Governance Control Center"
    )

    inv = model_inventory()
    risks = risk_register()
    tests = control_test_results()
    incidents = incident_log()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "AI systems / agents",
        len(inv),
    )

    c2.metric(
        "High inherent risks",
        int(
            (risks.risk_tier == "High").sum()
        ),
    )

    c3.metric(
        "Controls tested",
        len(tests),
    )

    c4.metric(
        "Open / contained incidents",
        int(
            incidents.status.isin(
                ["Contained", "Open"]
            ).sum()
        ),
    )

    st.markdown(
        "#### AI / model / agent inventory"
    )

    st.dataframe(
        inv,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "#### AI risk register"
    )

    st.dataframe(
        risks,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "#### Control library + assurance results"
    )

    merged = control_library().merge(
        tests,
        on="control_id",
        how="left",
    )

    st.dataframe(
        merged,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "#### Incident and corrective-action log"
    )

    st.dataframe(
        incidents,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# TAB 3 — EVALUATION LAB
# ============================================================

with tabs[2]:

    st.subheader("Evaluation Lab")

    st.write(
        "Offline evaluation checks retrieval relevance, "
        "governance routing, expired-content leakage, "
        "grounding, latency and cost telemetry."
    )

    if st.button(
        "Run evaluation suite"
    ):

        df_eval = run_evaluation(
            retriever
        )

        st.session_state[
            "eval_df"
        ] = df_eval

    df_eval = st.session_state.get(
        "eval_df"
    )

    if df_eval is not None:

        summary = eval_summary(
            df_eval
        )

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Retrieval hit",
            f"{summary['retrieval_precision_proxy'] * 100:.0f}%",
        )

        c2.metric(
            "Governance routing",
            f"{summary['governance_routing_accuracy'] * 100:.0f}%",
        )

        c3.metric(
            "Expired leak rate",
            f"{summary['expired_content_leak_rate'] * 100:.0f}%",
        )

        c4.metric(
            "Grounded response",
            f"{summary['grounded_response_rate'] * 100:.0f}%",
        )

        c5.metric(
            "P95 latency",
            f"{summary['p95_latency_ms']:.0f} ms",
        )

        st.dataframe(
            df_eval,
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            "These are reference-test results from "
            "a small synthetic evaluation set, "
            "not production quality claims."
        )


# ============================================================
# TAB 4 — LEARNING REINFORCEMENT
# ============================================================

with tabs[3]:

    st.subheader(
        "Adaptive spaced-learning reinforcement"
    )

    seller_id = st.selectbox(
        "Seller",
        sellers.seller_id.head(50).tolist(),
    )

    row = sellers[
        sellers.seller_id == seller_id
    ].iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Current proficiency",
        f"{row.proficiency}%",
    )

    c2.metric(
        "Weekly AI adoption",
        f"{row.weekly_ai_adoption}%",
    )

    c3.metric(
        "Certified",
        "Yes" if row.certified else "No",
    )

    plan = reinforcement_plan(
        seller_id,
        int(row.proficiency),
        "Governed AI seller guidance",
    )

    st.dataframe(
        plan,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "#### Organisation-wide reinforcement demand"
    )

    st.dataframe(
        learning_metrics(sellers).round(1),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# TAB 5 — ENABLEMENT OPERATIONS
# ============================================================

with tabs[4]:

    st.subheader(
        "AI-enabled intake, prioritisation "
        "and operating telemetry"
    )

    req = st.text_input(
        "New enablement request",
        "Urgent: customer waiting for a pricing exception",
    )

    if st.button(
        "Classify and route request"
    ):

        st.json(
            classify_request(req)
        )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Synthetic sellers",
        f"{len(sellers):,}",
    )

    c2.metric(
        "Weekly AI adoption",
        f"{sellers.weekly_ai_adoption.mean():.0f}%",
    )

    c3.metric(
        "Average proficiency",
        f"{sellers.proficiency.mean():.0f}%",
    )

    c4.metric(
        "Certified",
        f"{sellers.certified.mean() * 100:.0f}%",
    )

    market_perf = (
        sellers
        .groupby(
            "market",
            as_index=False,
        )
        .agg(
            adoption=(
                "weekly_ai_adoption",
                "mean",
            ),
            proficiency=(
                "proficiency",
                "mean",
            ),
            sellers=(
                "seller_id",
                "count",
            ),
        )
    )

    fig = px.scatter(
        market_perf,
        x="adoption",
        y="proficiency",
        size="sellers",
        hover_name="market",
        title="Market adoption vs proficiency",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# TAB 6 — VENDOR GOVERNANCE
# ============================================================

with tabs[5]:

    st.subheader(
        "Distributed seller and "
        "outsourced-vendor governance"
    )

    vendor = (
        sellers
        .groupby(
            "vendor",
            as_index=False,
        )
        .agg(
            sellers=(
                "seller_id",
                "count",
            ),
            adoption=(
                "weekly_ai_adoption",
                "mean",
            ),
            proficiency=(
                "proficiency",
                "mean",
            ),
            certification=(
                "certified",
                "mean",
            ),
            escalations=(
                "human_escalations",
                "sum",
            ),
        )
    )

    vendor["certification"] *= 100

    st.dataframe(
        vendor.round(1),
        use_container_width=True,
        hide_index=True,
    )

    fig = px.bar(
        vendor,
        x="vendor",
        y=[
            "adoption",
            "proficiency",
            "certification",
        ],
        barmode="group",
        title="Vendor enablement scorecard",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.markdown(
        "#### Multi-tier operating model"
    )

    st.code(
        """
Global AI / Enablement Governance
        ↓
APAC Enablement Owner
        ↓
Vendor Enablement Lead
        ↓
Certified Trainer
        ↓
Seller
        ↓
Feedback / telemetry / escalation
        ↺ APAC Enablement Owner
"""
    )


# ============================================================
# TAB 7 — LEARNING TO SCALE
# ============================================================

with tabs[6]:

    st.subheader(
        "Top-performer learning → "
        "governed module update → test → scale"
    )

    st.write(
        "This lab models how a mature BPO/"
        "sales-enablement function can turn "
        "performance evidence into approved learning "
        "and controlled AI/LLM updates without "
        "automatically learning from raw seller interactions."
    )

    top = identify_top_performers(
        sellers
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Synthetic top-performer cohort",
        len(top),
    )

    c2.metric(
        "Avg proficiency",
        f"{top.proficiency.mean():.0f}%",
    )

    c3.metric(
        "Avg AI adoption",
        f"{top.weekly_ai_adoption.mean():.0f}%",
    )

    c4.metric(
        "Markets represented",
        top.market.nunique(),
    )

    st.markdown(
        "#### 1. BPO sales learning track"
    )

    st.dataframe(
        learning_track(),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "#### 2. Candidate learning signals"
    )

    st.caption(
        "Synthetic signals only. Raw interaction "
        "patterns never update the model or "
        "knowledge base automatically."
    )

    st.dataframe(
        learning_signal_backlog(),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "#### 3. Questions the system must ask "
        "before an LLM/module update"
    )

    for q in key_learning_questions():
        st.write("•", q)

    st.markdown(
        "#### 4. Governed update pipeline"
    )

    st.dataframe(
        module_update_pipeline(),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "#### 5. Test-and-scale gates"
    )

    st.dataframe(
        scale_gate_metrics(),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "#### Progressive rollout"
    )

    st.code(
        """
Candidate learning
    ↓ human SME validation
Versioned knowledge / prompt / module update
    ↓ red-team + offline evaluation
Sandbox / control cohort
    ↓ governance scale gate
10% → 25% → 50% → 100%
    ↓
Continuous monitoring + rollback + new learning signals
"""
    )


# ============================================================
# TAB 8 — AGENT LIFECYCLE GOVERNANCE
# ============================================================

with tabs[7]:

    st.subheader(
        "Human + AI Agent Lifecycle Governance"
    )

    st.write(
        "Joiner–Mover–Leaver controls for human/BPO "
        "sellers run alongside onboarding, change "
        "control and retirement controls for AI agents."
    )

    human_tab, ai_tab, access_tab = st.tabs(
        [
            "Human/BPO JML",
            "AI Agent Lifecycle",
            "Access Review",
        ]
    )

    with human_tab:

        st.markdown(
            "#### Human/BPO onboarding, "
            "movement and offboarding"
        )

        st.dataframe(
            human_agent_lifecycle(),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(
            "#### Example mover access delta"
        )

        delta = mover_access_delta(
            [
                "SellerAI",
                "CRM-MY-SMB",
                "KB-MY-SMB",
                "Vendor-B",
            ],
            [
                "SellerAI",
                "CRM-ID-MID",
                "KB-ID-MID",
                "Vendor-B",
            ],
        )

        c1, c2, c3 = st.columns(3)

        c1.write("**Revoke**")
        c1.write(delta["revoke"])

        c2.write("**Retain**")
        c2.write(delta["retain"])

        c3.write(
            "**Grant after approval**"
        )
        c3.write(delta["grant"])

        st.markdown(
            "#### Human offboarding checklist"
        )

        st.dataframe(
            offboarding_checklist("Human"),
            use_container_width=True,
            hide_index=True,
        )

    with ai_tab:

        st.markdown(
            "#### AI agent onboarding → "
            "operate/change → retirement"
        )

        st.dataframe(
            ai_agent_lifecycle(),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(
            "#### AI agent retirement checklist"
        )

        st.dataframe(
            offboarding_checklist("AI"),
            use_container_width=True,
            hide_index=True,
        )

    with access_tab:

        events = lifecycle_events()
        review = access_review()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Lifecycle events",
            len(events),
        )

        c2.metric(
            "Access reviews due",
            int(
                (
                    review.access_status
                    == "Review due"
                ).sum()
            ),
        )

        c3.metric(
            "Excess privilege flags",
            int(
                review.excess_privilege_flag.sum()
            ),
        )

        c4.metric(
            "Orphan identities",
            int(
                review.orphan_flag.sum()
            ),
        )

        st.markdown(
            "#### Lifecycle event log"
        )

        st.dataframe(
            events,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(
            "#### Access-review control center"
        )

        st.dataframe(
            review,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# TAB 9 — ALERTS & HUMAN ESCALATION
# ============================================================

with tabs[8]:

    st.subheader(
        "Step 3 — Alerts & Human Escalation"
    )

    st.caption(
        "AI autonomy stops at explicit policy, authority, "
        "data and risk boundaries. Boundary crossings "
        "create governed human escalation."
    )

    alerts = sample_alerts()
    summary = alert_summary(alerts)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🔴 Critical",
        summary["critical_red"],
    )

    c2.metric(
        "🟡 Human review",
        summary["review_yellow"],
    )

    c3.metric(
        "Open",
        summary["open"],
    )

    c4.metric(
        "Closed",
        summary["closed"],
    )

    scope_tab, rules_tab, queue_tab = st.tabs(
        [
            "Scope Boundary",
            "Trigger Rules",
            "Alert Queue",
        ]
    )

    with scope_tab:

        matrix = scope_matrix()

        st.markdown(
            "#### AI in scope"
        )

        st.dataframe(
            matrix[
                matrix.boundary
                == "AI IN SCOPE"
            ][["action"]],
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(
            "#### Human accountability / "
            "out of AI scope"
        )

        st.dataframe(
            matrix[
                matrix.boundary
                == "HUMAN ACCOUNTABILITY"
            ][["action"]],
            use_container_width=True,
            hide_index=True,
        )

    with rules_tab:

        st.markdown(
            "#### Trigger → AI action → "
            "human owner → SLA"
        )

        st.dataframe(
            alert_rules(),
            use_container_width=True,
            hide_index=True,
        )

    with queue_tab:

        st.markdown(
            "#### Governed alert queue"
        )

        st.dataframe(
            alerts,
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            "Each alert preserves subject, market, vendor, "
            "trigger, AI action, accountable human owner, "
            "SLA, status and audit ID."
        )


# ============================================================
# TAB 10 — DEMO GUIDE
# ============================================================

with tabs[9]:

    st.subheader(
        "📖 SellerAI Demo Guide"
    )

    st.caption(
        "How to navigate and demonstrate the "
        "SellerAI Phase 4 experience."
    )

    render_markdown_file(
        ROOT / "USER_GUIDE.md",
        "USER_GUIDE.md could not be found in the repository root.",
    )


# ============================================================
# TAB 11 — DATA DICTIONARY
# ============================================================

with tabs[10]:

    st.subheader(
        "📊 Data Dictionary"
    )

    st.caption(
        "Definitions for the synthetic seller, "
        "performance and governance data used in this demo."
    )

    render_markdown_file(
        ROOT / "DATA_DICTIONARY.md",
        "DATA_DICTIONARY.md could not be found in the repository root.",
    )


# ============================================================
# TAB 12 — ARCHITECTURE
# ============================================================

with tabs[11]:

    st.subheader(
        "🏗️ Solution Architecture"
    )

    st.caption(
        "Reference architecture, data flow, "
        "AI components and governance design."
    )

    render_markdown_file(
        ROOT / "ARCHITECTURE.md",
        "ARCHITECTURE.md could not be found in the repository root.",
    )


# ============================================================
# TAB 13 — PORTFOLIO OVERVIEW
# ============================================================

with tabs[12]:

    st.subheader(
        "ℹ️ Portfolio Overview"
    )

    st.caption(
        "Business context, capabilities and "
        "portfolio positioning for SellerAI."
    )

    # Supports either location:
    # docs/README_PORTFOLIO.md
    # OR README_PORTFOLIO.md in repository root.

    portfolio_docs_path = (
        ROOT
        / "docs"
        / "README_PORTFOLIO.md"
    )

    portfolio_root_path = (
        ROOT
        / "README_PORTFOLIO.md"
    )

    if portfolio_docs_path.exists():

        render_markdown_file(
            portfolio_docs_path,
            "",
        )

    elif portfolio_root_path.exists():

        render_markdown_file(
            portfolio_root_path,
            "",
        )

    else:

        st.warning(
            "README_PORTFOLIO.md could not be found "
            "in either /docs or the repository root."
        )
