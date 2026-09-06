# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
from app.lifecycle import human_agent_lifecycle, ai_agent_lifecycle, mover_access_delta, offboarding_checklist

def test_human_jml_has_joiner_mover_leaver():
    stages = set(human_agent_lifecycle()["stage"])
    assert {"Joiner","Mover","Leaver"}.issubset(stages)

def test_ai_lifecycle_has_retirement_controls():
    stages = set(ai_agent_lifecycle()["stage"])
    assert "Retire" in stages
    assert len(offboarding_checklist("AI")) >= 6

def test_mover_access_delta_revokes_obsolete_access():
    d = mover_access_delta(["A","B","C"], ["A","D"])
    assert d["revoke"] == ["B","C"]
    assert d["retain"] == ["A"]
    assert d["grant"] == ["D"]

def test_human_offboarding_checks_zero_residual_access():
    txt = " ".join(offboarding_checklist("Human")["control"]).lower()
    assert "zero residual access" in txt
