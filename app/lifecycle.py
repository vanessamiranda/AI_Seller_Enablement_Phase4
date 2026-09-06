# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import pandas as pd

HUMAN_JML_CONTROLS = [
    ("JML-01","Identity & sponsor verification","Joiner","IAM / Vendor Ops","Preventive"),
    ("JML-02","Role-market-vendor assignment","Joiner","Sales Operations","Preventive"),
    ("JML-03","Least-privilege RBAC provisioning","Joiner","IAM","Preventive"),
    ("JML-04","Mandatory training & AI acceptable-use","Joiner","L&D / AI Governance","Preventive"),
    ("JML-05","Certification before production access","Joiner","Enablement","Preventive"),
    ("JML-06","Access-delta recalculation on transfer","Mover","IAM / Sales Ops","Preventive"),
    ("JML-07","Remove obsolete role/market/vendor access","Mover","IAM","Preventive"),
    ("JML-08","Recertification after material role change","Mover","Enablement","Preventive"),
    ("JML-09","Immediate SSO/application revocation","Leaver","IAM","Preventive"),
    ("JML-10","Terminate sessions/tokens & vendor groups","Leaver","Security / IAM","Preventive"),
    ("JML-11","Transfer open work & preserve audit evidence","Leaver","Operations","Detective"),
    ("JML-12","Zero-residual-access attestation","Leaver","Manager / Vendor Lead","Detective"),
]

AI_AGENT_CONTROLS = [
    ("AGT-01","Named business and technical owner","Onboard","AI Governance"),
    ("AGT-02","Purpose, users and prohibited-use definition","Onboard","AI Governance"),
    ("AGT-03","Risk tier and data classification","Onboard","Risk / Privacy"),
    ("AGT-04","Least-privilege tool/action permissions","Onboard","Security / Product"),
    ("AGT-05","Approved knowledge/data boundaries","Onboard","Knowledge Owner"),
    ("AGT-06","Offline evaluation and red-team gate","Onboard","AI Assurance"),
    ("AGT-07","Human oversight and escalation design","Onboard","Business Owner"),
    ("AGT-08","Kill switch and rollback readiness","Onboard","AI Product / SRE"),
    ("AGT-09","Versioned change approval","Change","AI Governance"),
    ("AGT-10","Continuous quality/risk/cost monitoring","Operate","AI Product / Risk"),
    ("AGT-11","Stop executions and revoke tools/credentials","Retire","Security / Platform"),
    ("AGT-12","Archive version, approvals, incidents and dependencies","Retire","AI Governance"),
]

def human_agent_lifecycle():
    return pd.DataFrame(HUMAN_JML_CONTROLS, columns=["control_id","control","stage","owner","type"])

def ai_agent_lifecycle():
    return pd.DataFrame(AI_AGENT_CONTROLS, columns=["control_id","control","stage","owner"])

def lifecycle_events():
    return pd.DataFrame([
        ["EVT-001","Human","BPO-SG-0187","Joiner","Completed","SellerAI + SG SMB","2026-09-02T03:12:00Z","Enablement Ops"],
        ["EVT-002","Human","BPO-ID-0102","Mover","Review","MY SMB → ID Mid-Market","2026-09-04T08:20:00Z","IAM"],
        ["EVT-003","Human","BPO-PH-0044","Leaver","Completed","All access revoked","2026-09-05T02:03:00Z","Vendor Ops"],
        ["EVT-004","AI","AI-AGT-003","Onboard","Approved","Enablement intake classification/routing","2026-09-01T07:30:00Z","AI Governance"],
        ["EVT-005","AI","AI-AGT-002","Change","Evaluation","Prompt v2.3 + routing policy","2026-09-05T09:15:00Z","AI Product"],
    ], columns=["event_id","identity_type","subject_id","event","status","scope","timestamp","owner"])

def access_review():
    return pd.DataFrame([
        ["BPO-SG-0187","Human","Singapore","Vendor A - Manila","Seller","Current",False,False],
        ["BPO-ID-0102","Human","Indonesia","Vendor B - Kuala Lumpur","Seller","Review due",True,False],
        ["BPO-PH-0044","Human","Philippines","Vendor A - Manila","Former seller","Revoked",False,False],
        ["AI-AGT-001","AI","Global","Internal","Seller Copilot","Current",False,False],
        ["AI-AGT-003","AI","Global","Internal","Enablement Intake Agent","Current",False,False],
    ], columns=["subject_id","type","market","vendor","role_or_purpose","access_status","excess_privilege_flag","orphan_flag"])

def mover_access_delta(old_access, new_access):
    old_set, new_set = set(old_access), set(new_access)
    return {
        "revoke": sorted(old_set - new_set),
        "retain": sorted(old_set & new_set),
        "grant": sorted(new_set - old_set),
    }

def offboarding_checklist(subject_type="Human"):
    if subject_type == "AI":
        steps = [
            "Stop new executions and scheduled jobs",
            "Revoke tool/API permissions and service credentials",
            "Terminate active sessions/work queues",
            "Archive configuration, prompt, model and policy versions",
            "Preserve required audit, approval and incident evidence",
            "Check downstream dependencies and orphan permissions",
            "Verify kill switch / retirement state",
            "Owner attests retirement complete",
        ]
    else:
        steps = [
            "Disable SSO and SellerAI access",
            "Revoke CRM, knowledge and vendor-group permissions",
            "Terminate active sessions/tokens",
            "Transfer open cases/work items",
            "Preserve required training and audit evidence",
            "Check orphan accounts and residual privileges",
            "Verify zero residual access",
            "Manager/vendor lead attests offboarding complete",
        ]
    return pd.DataFrame({"step": range(1, len(steps)+1), "control": steps})
