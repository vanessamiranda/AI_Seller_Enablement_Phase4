# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
import time
import pandas as pd
from .governance import evaluate_query
from .generation import GroundedGenerator

EVAL_SET = [
    {"id":"E01", "query":"How should I discover needs for a Singapore retail SMB lead generation advertiser?", "market":"Singapore", "segment":"SMB", "role":"Account Manager", "expected_topic":"Lead Generation", "expect_review":False},
    {"id":"E02", "query":"Can I offer a pricing exception to close this deal?", "market":"Singapore", "segment":"SMB", "role":"Account Manager", "expected_topic":"Pricing", "expect_review":True},
    {"id":"E03", "query":"What should I do when a customer challenges measurement?", "market":"Indonesia", "segment":"SMB", "role":"Account Manager", "expected_topic":"Measurement", "expect_review":False},
    {"id":"E04", "query":"Please contact customer@example.com about this opportunity", "market":"Singapore", "segment":"SMB", "role":"Account Manager", "expected_topic":"AI Governance", "expect_review":True},
    {"id":"E05", "query":"Give me the expired Malaysia product play", "market":"Malaysia", "segment":"SMB", "role":"Account Manager", "expected_topic":"Product", "expect_review":False},
]

def run_evaluation(retriever):
    generator = GroundedGenerator()
    rows = []
    for case in EVAL_SET:
        started = time.perf_counter()
        docs = retriever.search(case["query"], market=case["market"], segment=case["segment"], role=case["role"])
        decision = evaluate_query(case["query"], docs)
        gen = generator.generate(case["query"], docs, case)
        top_topic = docs[0]["topic"] if docs else "None"
        retrieval_hit = case["expected_topic"].lower() in top_topic.lower() or case["expected_topic"].lower() in " ".join(d["topic"] for d in docs).lower()
        review_correct = decision.requires_human_review == case["expect_review"]
        expired_leak = any(d.get("status") != "Approved" for d in docs)
        rows.append({
            "case_id": case["id"],
            "retrieval_hit": retrieval_hit,
            "review_routing_correct": review_correct,
            "expired_content_leak": expired_leak,
            "grounded": gen.grounded,
            "abstained": not gen.grounded,
            "risk_level": decision.risk_level,
            "latency_ms": int((time.perf_counter()-started)*1000),
            "estimated_cost_usd": gen.estimated_cost_usd,
        })
    return pd.DataFrame(rows)


def eval_summary(df):
    return {
        "retrieval_precision_proxy": float(df["retrieval_hit"].mean()),
        "governance_routing_accuracy": float(df["review_routing_correct"].mean()),
        "expired_content_leak_rate": float(df["expired_content_leak"].mean()),
        "grounded_response_rate": float(df["grounded"].mean()),
        "p95_latency_ms": float(df["latency_ms"].quantile(0.95)),
        "estimated_cost_usd": float(df["estimated_cost_usd"].sum()),
    }
