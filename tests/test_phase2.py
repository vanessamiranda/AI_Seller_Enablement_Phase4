# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
from app.learning import reinforcement_plan
from app.risk import risk_register, model_inventory
from app.evaluation import run_evaluation, eval_summary
from app.retrieval import GovernedRetriever
from app.generation import GroundedGenerator


def test_reinforcement_more_intensive_for_low_proficiency():
    low = reinforcement_plan("S1", 50)
    high = reinforcement_plan("S2", 90)
    assert len(low) > len(high)
    assert low["human_coach_required"].any()


def test_risk_register_scores():
    df = risk_register()
    assert "inherent_score" in df.columns
    assert (df["inherent_score"] > 0).all()


def test_model_inventory_has_copilot():
    df = model_inventory()
    assert (df["system"] == "SellerAI Copilot").any()


def test_grounded_generator_abstains_without_docs():
    result = GroundedGenerator().generate("unknown", [])
    assert result.grounded is False


def test_evaluation_runs():
    r = GovernedRetriever("data/knowledge_base.csv")
    df = run_evaluation(r)
    s = eval_summary(df)
    assert len(df) >= 5
    assert 0 <= s["expired_content_leak_rate"] <= 1
