# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
from dataclasses import dataclass
from typing import List, Dict
import time

@dataclass
class GenerationResult:
    answer: str
    grounded: bool
    citations: list
    latency_ms: int
    estimated_cost_usd: float
    provider: str

class GroundedGenerator:
    """Offline-safe grounded generation layer.

    Phase 2 deliberately keeps the demo runnable without external API keys.
    The interface can be replaced by an enterprise model gateway later.
    """

    def generate(self, query: str, docs: List[Dict], context: Dict | None = None) -> GenerationResult:
        started = time.perf_counter()
        context = context or {}
        approved = [d for d in docs if d.get("status") == "Approved"]
        if not approved:
            answer = (
                "I do not have an approved source for this request. "
                "I have routed it to the appropriate knowledge owner rather than generating an unsupported answer."
            )
            citations = []
            grounded = False
        else:
            lead = approved[0]
            market = context.get("market", "the selected market")
            segment = context.get("segment", "the selected segment")
            role = context.get("role", "the selected role")
            answer = (
                f"For {role} supporting {segment} in {market}: {lead['content']} "
                "Use this as assistive guidance only, verify customer-specific assumptions, "
                "and escalate any pricing, legal, policy, or unsupported commitment before customer-facing use."
            )
            citations = [d.get("doc_id") for d in approved[:3]]
            grounded = True

        latency = int((time.perf_counter() - started) * 1000)
        return GenerationResult(
            answer=answer,
            grounded=grounded,
            citations=citations,
            latency_ms=max(latency, 1),
            estimated_cost_usd=0.0,
            provider="offline-grounded-reference",
        )
