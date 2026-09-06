# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
from app.synthetic import seller_population
from app.top_performer_learning import identify_top_performers, learning_track, module_update_pipeline, scale_gate_metrics, key_learning_questions

def test_top_performer_cohort_is_subset():
    sellers = seller_population(530)
    top = identify_top_performers(sellers)
    assert 0 < len(top) < len(sellers)

def test_learning_track_has_bpo_scale_elements():
    track = learning_track()
    assert len(track) >= 10
    assert track['module'].str.contains('Train-the-trainer').any()
    assert track['module'].str.contains('AI copilot', case=False).any()

def test_update_pipeline_requires_human_approval_and_progressive_rollout():
    pipe = module_update_pipeline()
    assert pipe['governance_gate'].str.contains('Human approval', case=False).any()
    assert pipe['activity'].str.contains('10%').any()

def test_scale_gates_include_safety_and_learning():
    metrics = ' '.join(scale_gate_metrics()['metric'].tolist()).lower()
    assert 'policy' in metrics and 'proficiency' in metrics and 'incident' in metrics

def test_key_learning_questions_cover_rollback():
    assert 'rollback' in ' '.join(key_learning_questions()).lower()
