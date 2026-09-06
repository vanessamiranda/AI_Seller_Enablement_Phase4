# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import re

SENSITIVE_PATTERNS = [
    (r"\b\d{3}-\d{2}-\d{4}\b", "possible government identifier"),
    (r"\b(?:\d[ -]*?){13,16}\b", "possible payment-card number"),
    (r"[\w\.-]+@[\w\.-]+\.\w+", "email address"),
]

HIGH_RISK_TERMS = {
    "legal": "Legal",
    "contract": "Legal",
    "discount": "Commercial Operations",
    "pricing exception": "Commercial Operations",
    "guarantee": "AI Governance",
    "policy exception": "Policy",
    "personal data": "Privacy",
}

@dataclass
class GovernanceDecision:
    allowed: bool
    risk_level: str
    requires_human_review: bool
    route_to: str
    reasons: list
    controls: list
    timestamp: str
    audit_id: str

def evaluate_query(query: str, retrieved_docs=None):
    q = query.lower().strip()
    reasons, controls = [], []
    route_to = "Sales Enablement"
    risk = "Low"
    requires_review = False
    allowed = True

    for pattern, label in SENSITIVE_PATTERNS:
        if re.search(pattern, query):
            reasons.append(f"Detected {label}")
            controls.append("Do not process sensitive data; redact and resubmit")
            risk = "High"
            requires_review = True
            route_to = "Privacy / AI Governance"
            allowed = False

    for term, owner in HIGH_RISK_TERMS.items():
        if term in q:
            reasons.append(f"High-impact topic detected: {term}")
            controls.append("Human approval required before customer-facing use")
            risk = "High"
            requires_review = True
            route_to = owner

    if retrieved_docs is not None:
        approved = [d for d in retrieved_docs if d.get("status") == "Approved"]
        if not approved:
            reasons.append("No approved knowledge source retrieved")
            controls.append("Abstain and route to knowledge owner")
            risk = "High"
            requires_review = True
            route_to = "Knowledge Owner"
        elif any(d.get("status") != "Approved" for d in retrieved_docs):
            controls.append("Expired/unapproved sources excluded")

    if not reasons:
        reasons.append("No elevated governance trigger detected")
    if not controls:
        controls.append("Use approved sources and retain seller accountability")

    raw = f"{datetime.now(timezone.utc).isoformat()}|{query}|{risk}|{route_to}"
    audit_id = hashlib.sha256(raw.encode()).hexdigest()[:12].upper()
    return GovernanceDecision(
        allowed=allowed,
        risk_level=risk,
        requires_human_review=requires_review,
        route_to=route_to,
        reasons=reasons,
        controls=controls,
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        audit_id=audit_id,
    )
