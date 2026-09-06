# Phase 2 — AI Governance Operating System

Phase 2 extends SellerAI from a governed retrieval prototype into an **AI enablement operating-system reference architecture**.

## New capabilities

### 1. Grounded-generation layer
A provider abstraction turns approved retrieved knowledge into seller guidance while retaining abstention behavior when evidence is unavailable. The repository runs offline by default so reviewers do not need API keys.

### 2. AI / model / agent inventory
Tracks purpose, technology, users, risk tier, owner and lifecycle status for each AI-enabled component.

### 3. AI risk register
Represents risks across model/retrieval, knowledge governance, privacy/security, third-party/vendor governance and adoption/change.

### 4. Control library and assurance testing
Controls have identifiers, owners, execution type, criticality and test evidence. Automated tests provide a lightweight assurance trail.

### 5. AI incident management
Illustrates incident classification, severity, market, owner, containment status and corrective actions.

### 6. Evaluation harness
A synthetic evaluation suite measures:
- retrieval relevance proxy,
- governance-routing accuracy,
- expired-content leakage,
- grounded-response rate,
- latency,
- model-cost telemetry.

### 7. Adaptive spaced reinforcement
Seller proficiency determines reinforcement cadence. Lower-proficiency sellers receive more frequent practice and human-coach checkpoints.

### 8. Vendor governance
Internal and outsourced vendor populations are compared on adoption, proficiency, certification and escalation metrics.

## What this does *not* claim

This is a reference implementation using synthetic data. It is not evidence that the author deployed the system to 530 real sellers or managed three real BPO vendors.

### 9. Agent lifecycle governance
Human/BPO Joiner-Mover-Leaver controls manage identity, least-privilege access, training, certification, transfer access deltas, revocation and residual-access attestation. AI-agent lifecycle controls cover registration, ownership, risk tiering, tool/data permissions, evaluation, human oversight, change control, kill switch and retirement.

### 10. Step 3 — Alerts & Human Escalation
The system now enforces explicit AI-in-scope versus human-only boundaries and routes policy, legal, commercial, privacy, knowledge, proficiency, access and AI-agent permission triggers to accountable human owners with severity, SLA and audit evidence.
