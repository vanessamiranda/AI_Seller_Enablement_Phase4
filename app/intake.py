# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
from collections import Counter

CATEGORIES = {
    "pricing": "Commercial Operations",
    "measurement": "Measurement Enablement",
    "policy": "Policy",
    "training": "Learning & Development",
    "product": "Product Enablement",
    "legal": "Legal",
    "knowledge": "Knowledge Management",
}

def classify_request(text):
    t = text.lower()
    matches = [(k, owner) for k, owner in CATEGORIES.items() if k in t]
    category, owner = matches[0] if matches else ("general enablement", "Sales Enablement")
    urgent = any(x in t for x in ["urgent", "blocked", "customer waiting", "launch today"])
    priority = "P1" if urgent else ("P2" if category in ["pricing","policy","legal"] else "P3")
    return {"category": category, "owner": owner, "priority": priority}

def summarize_intake(requests):
    categories = Counter(r["category"] for r in requests)
    priorities = Counter(r["priority"] for r in requests)
    return {"categories": dict(categories), "priorities": dict(priorities)}
