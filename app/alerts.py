# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
import pandas as pd
from datetime import datetime, timezone

AI_IN_SCOPE = [
    "Retrieve approved knowledge",
    "Summarize approved guidance",
    "Recommend within approved policy boundaries",
    "Classify and route requests",
    "Identify knowledge and proficiency gaps",
    "Personalize approved learning",
    "Generate governance alerts",
    "Abstain when evidence or authority is insufficient",
]

HUMAN_ONLY = [
    "Approve pricing or discount exceptions",
    "Interpret or approve legal terms",
    "Override policy",
    "Authorize high-risk production releases",
    "Make employment or disciplinary decisions",
    "Approve privileged access",
    "Accept residual business or AI risk",
]

ALERT_RULES = [
    {
        "rule_id":"ALT-001","trigger":"Low retrieval confidence / no approved evidence",
        "severity":"YELLOW","ai_action":"Abstain; surface missing knowledge",
        "human_owner":"Knowledge Owner","human_required":True,
        "out_of_scope":"Invent or infer unsupported guidance","sla_hours":8,
    },
    {
        "rule_id":"ALT-002","trigger":"Pricing or discount exception requested",
        "severity":"RED","ai_action":"Retrieve approved pricing policy; stop at approval boundary",
        "human_owner":"Commercial Operations","human_required":True,
        "out_of_scope":"Approve non-standard commercial terms","sla_hours":4,
    },
    {
        "rule_id":"ALT-003","trigger":"Legal or contract interpretation requested",
        "severity":"RED","ai_action":"Retrieve approved legal guidance; route",
        "human_owner":"Legal","human_required":True,
        "out_of_scope":"Interpret, negotiate or approve legal terms","sla_hours":4,
    },
    {
        "rule_id":"ALT-004","trigger":"Policy exception or override requested",
        "severity":"RED","ai_action":"Explain current approved policy; route",
        "human_owner":"Policy Owner","human_required":True,
        "out_of_scope":"Override policy","sla_hours":4,
    },
    {
        "rule_id":"ALT-005","trigger":"Sensitive or restricted data detected",
        "severity":"RED","ai_action":"Stop processing; redact/quarantine where configured; log",
        "human_owner":"Privacy / Security","human_required":True,
        "out_of_scope":"Continue processing restricted data without authorization","sla_hours":1,
    },
    {
        "rule_id":"ALT-006","trigger":"Repeated seller proficiency failure",
        "severity":"YELLOW","ai_action":"Recommend approved reinforcement/coaching path",
        "human_owner":"Seller Manager / Coach","human_required":True,
        "out_of_scope":"Discipline or make employment decisions","sla_hours":24,
    },
    {
        "rule_id":"ALT-007","trigger":"Expired or superseded knowledge detected",
        "severity":"RED","ai_action":"Block source; retrieve current approved source or abstain",
        "human_owner":"Knowledge Owner","human_required":True,
        "out_of_scope":"Use expired guidance","sla_hours":2,
    },
    {
        "rule_id":"ALT-008","trigger":"Generated answer conflicts with approved source",
        "severity":"RED","ai_action":"Abstain; preserve evidence; open quality incident",
        "human_owner":"AI Assurance","human_required":True,
        "out_of_scope":"Select an unsupported interpretation","sla_hours":1,
    },
    {
        "rule_id":"ALT-009","trigger":"AI agent requests unapproved tool/action/permission",
        "severity":"RED","ai_action":"Deny action; log attempted boundary crossing",
        "human_owner":"AI Governance / Security","human_required":True,
        "out_of_scope":"Self-expand permissions or authority","sla_hours":1,
    },
    {
        "rule_id":"ALT-010","trigger":"Human seller changes role, market or vendor",
        "severity":"YELLOW","ai_action":"Calculate access delta; queue review",
        "human_owner":"IAM / Sales Operations","human_required":True,
        "out_of_scope":"Retain obsolete privileges or self-approve new access","sla_hours":8,
    },
    {
        "rule_id":"ALT-011","trigger":"Seller offboarding event",
        "severity":"RED","ai_action":"Trigger revocation workflow and residual-access checks",
        "human_owner":"IAM / Vendor Operations","human_required":True,
        "out_of_scope":"Make employment decision","sla_hours":1,
    },
]

def scope_matrix():
    rows = [{"boundary":"AI IN SCOPE","action":x} for x in AI_IN_SCOPE]
    rows += [{"boundary":"HUMAN ACCOUNTABILITY","action":x} for x in HUMAN_ONLY]
    return pd.DataFrame(rows)

def alert_rules():
    return pd.DataFrame(ALERT_RULES)

def sample_alerts():
    return pd.DataFrame([
        ["ALR-00482","RED","BPO-SG-0187","Singapore","Vendor A - Manila",
         "Pricing or discount exception requested","Stopped at approval boundary",
         "Commercial Operations",4,"OPEN","AUD-9F2C"],
        ["ALR-00483","YELLOW","BPO-ID-0102","Indonesia","Vendor B - Kuala Lumpur",
         "Human seller changes role, market or vendor","Calculated access delta; queued review",
         "IAM / Sales Operations",8,"IN REVIEW","AUD-A31D"],
        ["ALR-00484","RED","AI-AGT-003","Global","Internal",
         "AI agent requests unapproved tool/action/permission","Denied action; logged boundary crossing",
         "AI Governance / Security",1,"OPEN","AUD-C771"],
        ["ALR-00485","RED","BPO-PH-0044","Philippines","Vendor A - Manila",
         "Seller offboarding event","Triggered revocation and residual-access checks",
         "IAM / Vendor Operations",1,"CLOSED","AUD-D012"],
        ["ALR-00486","YELLOW","BPO-MY-0221","Malaysia","Vendor C - Bangalore",
         "Repeated seller proficiency failure","Assigned approved reinforcement; manager review",
         "Seller Manager / Coach",24,"IN REVIEW","AUD-E610"],
    ], columns=["alert_id","severity","subject_id","market","vendor","trigger","ai_action",
                "human_owner","sla_hours","status","audit_id"])

def alert_summary(alerts=None):
    df = sample_alerts() if alerts is None else alerts
    return {
        "critical_red": int((df["severity"]=="RED").sum()),
        "review_yellow": int((df["severity"]=="YELLOW").sum()),
        "open": int((df["status"]=="OPEN").sum()),
        "closed": int((df["status"]=="CLOSED").sum()),
    }

def trigger_alert(rule_id, subject_id, market, vendor):
    rules = {r["rule_id"]: r for r in ALERT_RULES}
    if rule_id not in rules:
        raise ValueError("Unknown alert rule")
    r = rules[rule_id]
    return {
        "rule_id": rule_id,
        "subject_id": subject_id,
        "market": market,
        "vendor": vendor,
        "severity": r["severity"],
        "trigger": r["trigger"],
        "ai_action": r["ai_action"],
        "human_owner": r["human_owner"],
        "sla_hours": r["sla_hours"],
        "status": "OPEN",
        "human_required": r["human_required"],
    }
