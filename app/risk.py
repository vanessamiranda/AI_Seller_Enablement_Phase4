# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import pandas as pd

DEFAULT_RISKS = [
    {
        "risk_id": "R-001",
        "risk": "Hallucinated or unsupported seller guidance",
        "domain": "Model / Retrieval",
        "likelihood": 4,
        "impact": 5,
        "controls": "Approved-source retrieval; abstention; human review",
        "owner": "AI Governance",
        "status": "Open",
    },
    {
        "risk_id": "R-002",
        "risk": "Expired knowledge surfaced to sellers",
        "domain": "Knowledge Governance",
        "likelihood": 3,
        "impact": 4,
        "controls": "Status gate; review dates; named owners",
        "owner": "Knowledge Management",
        "status": "Mitigated",
    },
    {
        "risk_id": "R-003",
        "risk": "Sensitive information entered into assistant",
        "domain": "Privacy / Security",
        "likelihood": 3,
        "impact": 5,
        "controls": "Input pattern detection; block; user training",
        "owner": "Privacy / AI Governance",
        "status": "Open",
    },
    {
        "risk_id": "R-004",
        "risk": "Vendor trainers use inconsistent or outdated guidance",
        "domain": "Third-Party / Vendor",
        "likelihood": 3,
        "impact": 4,
        "controls": "Trainer certification; content currency SLA; vendor scorecard",
        "owner": "Vendor Enablement",
        "status": "Open",
    },
    {
        "risk_id": "R-005",
        "risk": "AI adoption increases without seller proficiency",
        "domain": "Change / Adoption",
        "likelihood": 4,
        "impact": 3,
        "controls": "Proficiency measurement; spaced reinforcement; manager follow-up",
        "owner": "Learning & Development",
        "status": "Open",
    },
]

def risk_register():
    df = pd.DataFrame(DEFAULT_RISKS)
    df["inherent_score"] = df["likelihood"] * df["impact"]
    df["risk_tier"] = pd.cut(
        df["inherent_score"], bins=[0, 6, 12, 25], labels=["Low", "Medium", "High"], include_lowest=True
    ).astype(str)
    return df

CONTROL_LIBRARY = [
    ["GOV-01", "Approved-source retrieval", "Preventive", "Automated", "AI Governance", "Critical"],
    ["GOV-02", "Sensitive-data gate", "Preventive", "Automated", "Privacy", "Critical"],
    ["GOV-03", "High-impact routing", "Preventive", "Hybrid", "Commercial / Legal / Policy", "Critical"],
    ["GOV-04", "Source traceability", "Detective", "Automated", "Knowledge Management", "High"],
    ["GOV-05", "Abstention", "Preventive", "Automated", "AI Governance", "Critical"],
    ["GOV-06", "Decision audit ID", "Detective", "Automated", "AI Governance", "High"],
    ["GOV-07", "Human accountability", "Governance", "Human", "Sales Leadership", "Critical"],
    ["GOV-08", "Vendor trainer certification", "Preventive", "Hybrid", "Vendor Enablement", "High"],
    ["GOV-09", "Knowledge lifecycle review", "Preventive", "Hybrid", "Knowledge Management", "High"],
    ["GOV-10", "Adoption/proficiency separation", "Detective", "Automated", "L&D / Analytics", "Medium"],
]

def control_library():
    return pd.DataFrame(CONTROL_LIBRARY, columns=["control_id","control","type","execution","owner","criticality"])

def control_test_results():
    rows = [
        ["GOV-01", "Pass", 0, "Expired content excluded in automated test"],
        ["GOV-02", "Pass", 0, "Email / card-like / government-ID patterns blocked"],
        ["GOV-03", "Pass", 0, "Pricing/legal/policy topics require human review"],
        ["GOV-04", "Pass", 0, "Doc ID, owner and review date visible"],
        ["GOV-05", "Pass", 0, "No approved source => abstain and route"],
        ["GOV-06", "Pass", 0, "Unique audit ID generated"],
        ["GOV-08", "Partial", 1, "Certification modeled; workflow approval not yet persisted"],
        ["GOV-09", "Partial", 1, "Review dates modeled; automated expiry workflow pending"],
    ]
    return pd.DataFrame(rows, columns=["control_id","test_result","open_findings","evidence"])


def model_inventory():
    return pd.DataFrame([
        ["AI-001", "SellerAI Copilot", "Assistive knowledge guidance", "RAG / grounded generation", "Internal sellers + vendors", "Medium", "AI Governance", "Active"],
        ["AI-002", "Enablement Intake Classifier", "Classify/rout enablement demand", "Rules / classifier", "Enablement ops", "Low", "Sales Enablement", "Active"],
        ["AI-003", "Learning Reinforcement Engine", "Generate proficiency reinforcement schedule", "Rules / adaptive logic", "Sellers / trainers", "Low", "L&D", "Active"],
    ], columns=["system_id","system","purpose","technology","users","risk_tier","owner","status"])
