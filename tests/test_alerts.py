# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
from app.alerts import alert_rules, sample_alerts, alert_summary, scope_matrix, trigger_alert

def test_scope_has_ai_and_human_boundaries():
    assert set(scope_matrix()["boundary"]) == {"AI IN SCOPE","HUMAN ACCOUNTABILITY"}

def test_all_rules_with_human_boundary_have_owner_and_sla():
    df = alert_rules()
    assert df["human_required"].all()
    assert df["human_owner"].str.len().min() > 0
    assert (df["sla_hours"] > 0).all()

def test_red_alerts_stop_or_bound_ai_action():
    red = alert_rules()[alert_rules()["severity"]=="RED"]
    assert len(red) >= 5
    assert red["out_of_scope"].str.len().min() > 0

def test_sample_alerts_are_auditable():
    df = sample_alerts()
    for col in ["alert_id","subject_id","market","vendor","trigger","ai_action","human_owner","sla_hours","status","audit_id"]:
        assert col in df.columns
    assert df["audit_id"].notna().all()

def test_trigger_alert_routes_pricing_exception():
    a = trigger_alert("ALT-002","BPO-SG-0187","Singapore","Vendor A - Manila")
    assert a["severity"] == "RED"
    assert a["human_owner"] == "Commercial Operations"
    assert a["human_required"] is True
