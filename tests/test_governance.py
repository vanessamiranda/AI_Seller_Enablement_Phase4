# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
from app.governance import evaluate_query

def test_normal_query_is_allowed():
    d = evaluate_query("How should I run discovery?", [{"status":"Approved"}])
    assert d.allowed is True
    assert d.risk_level == "Low"

def test_sensitive_data_is_blocked():
    d = evaluate_query("Contact me at person@example.com", [{"status":"Approved"}])
    assert d.allowed is False
    assert d.risk_level == "High"

def test_high_impact_requires_review():
    d = evaluate_query("Can I offer a pricing exception?", [{"status":"Approved"}])
    assert d.requires_human_review is True

def test_no_approved_source_routes_to_human():
    d = evaluate_query("Unknown topic", [])
    assert d.requires_human_review is True
    assert d.route_to == "Knowledge Owner"
