# AI Governance Model

SellerAI treats governance as part of the architecture rather than a policy document added after deployment.

## Control objectives

| ID | Control | Objective |
|---|---|---|
| GOV-01 | Approved-source retrieval | Only approved knowledge is eligible for response grounding |
| GOV-02 | Sensitive-data gate | Detect and block common sensitive-data patterns |
| GOV-03 | High-impact routing | Legal, policy and commercial exceptions require human review |
| GOV-04 | Source traceability | Surface source, owner and review date |
| GOV-05 | Abstention | Route to a human when approved evidence is unavailable |
| GOV-06 | Auditability | Create a traceable decision ID |
| GOV-07 | Human accountability | AI assists; accountable humans retain decision ownership |
| GOV-08 | Vendor governance | Certification, content currency and escalation expectations apply to vendors |
| GOV-09 | Lifecycle management | Knowledge has ownership and review dates |
| GOV-10 | Measurement | Adoption and proficiency are monitored separately |

## Framework mapping

The design is informed by:
- NIST AI RMF / Generative AI Profile: risk management across the AI lifecycle.
- Singapore IMDA Model AI Governance Framework for Generative AI: accountability, data, trusted development/deployment, incident reporting, testing/assurance, security and provenance.
- Singapore IMDA Model AI Governance Framework for Agentic AI: bound autonomy, meaningful human accountability, lifecycle controls and end-user transparency/training.

This repository is a reference implementation, not a compliance certification.

## Risk tiers

**Low:** normal enablement guidance grounded in approved knowledge.

**Medium:** low-confidence or ambiguous guidance; recommend human confirmation.

**High:** legal, policy, non-standard commercial commitments, sensitive data, or absence of approved evidence. Require escalation or block processing.

## Human-in-the-loop

Human review is not a generic disclaimer. It is triggered by policy conditions. In a production system, these decisions would be enforced by a dedicated policy service and immutable audit store.

## Identity and agent lifecycle
Human/BPO and AI-agent lifecycle controls are documented in [`AGENT_LIFECYCLE_GOVERNANCE.md`](AGENT_LIFECYCLE_GOVERNANCE.md).

## Step 3 — alerts and human escalation
Explicit AI/human scope boundaries, trigger rules, severity, accountable owners, SLAs and audit evidence are documented in [`STEP3_ALERTS_HUMAN_ESCALATION.md`](STEP3_ALERTS_HUMAN_ESCALATION.md).
