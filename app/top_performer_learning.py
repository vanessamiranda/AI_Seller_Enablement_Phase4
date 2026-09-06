# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
import pandas as pd
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

LEARNING_DIMENSIONS = [
    "discovery_quality",
    "objection_handling",
    "solution_fit",
    "commercial_discipline",
    "compliance_adherence",
    "customer_empathy",
    "next_best_action",
]

def identify_top_performers(sellers: pd.DataFrame, percentile: float = 0.85):
    """Synthetic top-performer cohort based on proficiency + adoption, with guardrails."""
    df = sellers.copy()
    df["performance_index"] = (
        df["proficiency"] * 0.65 +
        df["weekly_ai_adoption"] * 0.20 +
        df["certified"].astype(int) * 10 -
        df["human_escalations"] * 1.5
    )
    threshold = df["performance_index"].quantile(percentile)
    return df[df["performance_index"] >= threshold].sort_values("performance_index", ascending=False)

def learning_signal_backlog():
    """Synthetic, non-customer learning signals for the demonstration environment."""
    return pd.DataFrame([
        ["LS-001","Objection handling","Top sellers confirm measurement objective before discussing tactics",18,0.91,"SME review","Measurement Enablement"],
        ["LS-002","Discovery","High performers ask business outcome, audience, conversion event and data-readiness questions early",26,0.94,"SME review","Sales Enablement"],
        ["LS-003","Commercial discipline","Top sellers escalate non-standard pricing instead of improvising commitments",14,0.97,"Governance review","Commercial Operations"],
        ["LS-004","Knowledge gap","Repeated questions show weak retrieval coverage for market-specific measurement guidance",31,0.86,"Knowledge update","Knowledge Management"],
        ["LS-005","Coaching","Lower-proficiency cohort benefits from scenario feedback more than generic refreshers",22,0.84,"L&D review","Learning & Development"],
    ], columns=["signal_id","theme","candidate_learning","observations","confidence","next_gate","owner"])

def module_update_pipeline():
    """Governed lifecycle from field learning to scaled LLM/learning module."""
    return pd.DataFrame([
        [1,"Observe","Interaction/QA/feedback signal detected","Learning signal","Enablement Analytics","No model change"],
        [2,"Compare","Contrast top-performer and cohort behavior","Candidate best practice","Enablement + QA","Bias/representativeness check"],
        [3,"Validate","SME verifies business truth and policy alignment","Approved learning","SME / Policy Owner","Human approval required"],
        [4,"Author","Create knowledge article, prompt/context or microlearning change","Candidate module vNext","Knowledge / L&D","Version controlled"],
        [5,"Red-team","Test unsupported claims, sensitive data, policy and edge cases","Safety evidence","AI Governance","Must pass critical controls"],
        [6,"Offline eval","Test retrieval, groundedness, abstention and routing","Evaluation report","AI Product","Threshold gate"],
        [7,"Pilot cohort","A/B test against current module with synthetic/sandbox cohort","Experiment result","Enablement Ops","No broad rollout"],
        [8,"Scale gate","Review proficiency, QA, conversion proxy, incidents and fairness","Go / revise / stop","Governance Council","Human decision"],
        [9,"Progressive rollout","10% → 25% → 50% → 100% with monitoring","Release telemetry","AI Product + Ops","Rollback enabled"],
        [10,"Continuous learn","Feed approved new evidence back into backlog","Next learning cycle","Enablement Analytics","Drift monitoring"],
    ], columns=["stage","name","activity","artifact","accountable_owner","governance_gate"])

def scale_gate_metrics():
    return pd.DataFrame([
        ["Grounded answer rate",">= 95%","Quality","Block scale if below threshold"],
        ["Critical policy violations","0","Safety","Immediate stop / rollback"],
        ["Sensitive-data leakage","0","Privacy","Immediate stop / incident"],
        ["Correct human escalation",">= 95%","Governance","Revise routing if below"],
        ["Knowledge retrieval success",">= 90%","RAG","Improve corpus/retrieval before scale"],
        ["Proficiency uplift",">= +8 pp vs baseline","Learning","Revise module if no uplift"],
        ["QA score uplift",">= +5 pp vs control","BPO quality","Require calibration review"],
        ["Adoption",">= 70% weekly active in target cohort","Change","Investigate friction"],
        ["Seller helpfulness",">= 4.2/5","Experience","Review low-scoring intents"],
        ["P95 latency","<= 2.5 sec","Operations","Optimize before broad rollout"],
        ["Cost per assisted interaction","Within approved budget","FinOps","Route/model optimization"],
        ["Incident rate","No Sev-1/Sev-2 attributable increase","Risk","Stop or rollback"],
    ], columns=["metric","example_gate","dimension","action_if_failed"])

def learning_track():
    return pd.DataFrame([
        [1,"Foundation & certification","Product/offer knowledge; CRM workflow; customer and data handling; AI acceptable use","Knowledge check + scenario","Certified to handle assisted interactions"],
        [2,"Discovery excellence","Business outcomes; qualification; needs diagnosis; listening; questioning","Observed role-play + QA rubric","Discovery proficiency"],
        [3,"Solution & value selling","Map need to approved solution; value articulation; next-best action","Scenario simulation","Solution-fit proficiency"],
        [4,"Objection handling","Measurement, price, trust, timing and competitor objections without unsupported claims","Objection simulation","Objection proficiency"],
        [5,"Commercial & compliance discipline","Pricing boundaries; disclosures; escalation; privacy; record keeping","Critical-control assessment","Zero critical-error certification"],
        [6,"AI copilot mastery","Prompt/context discipline; source checking; abstention; escalation; feedback","Live sandbox tasks","AI-assisted seller certification"],
        [7,"QA-calibrated coaching","Use interaction evidence and scorecards; targeted coaching; calibration","Coach review","Individual improvement plan"],
        [8,"Spaced reinforcement","Day 3/7/14/30 microlearning tied to observed gaps","Adaptive quizzes/scenarios","Retention + proficiency uplift"],
        [9,"Top-performer learning loop","Extract repeatable behaviors; separate correlation from approved best practice","SME validation","Approved reusable play"],
        [10,"Train-the-trainer / BPO scale","Trainer certification; calibration; localization; content currency; escalation SLA","Trainer calibration","Vendor readiness to scale"],
    ], columns=["level","module","learning_outcomes","assessment","exit_criterion"])

def key_learning_questions():
    return [
        "What do top performers consistently do differently at the same customer moment?",
        "Which behavior is repeatable and coachable rather than personality-dependent?",
        "Does the behavior improve quality/proficiency without increasing policy or customer risk?",
        "Is the learning valid across markets, languages, segments and vendor teams—or only locally?",
        "What approved evidence supports adding this learning to the knowledge base or LLM context?",
        "Should the change update knowledge, retrieval metadata, prompt/context, learning content, or routing policy?",
        "What failure modes could the update introduce, and what red-team tests are required?",
        "What offline evaluation threshold must pass before a cohort test?",
        "What metric proves learning transfer: proficiency, QA, conversion proxy, customer outcome, or error reduction?",
        "What is the rollback trigger, owner and decision authority if the new module underperforms?",
    ]
