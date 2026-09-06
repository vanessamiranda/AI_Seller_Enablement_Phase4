# Built-for-Scale Design

The repository deliberately separates **demonstrated architecture** from **claimed deployment scale**.

## Demo scale

- 530 synthetic sellers
- 8 APAC markets
- Internal sales + 3 fictional outsourced vendors
- Role, market and segment context
- Adoption, proficiency, certification and escalation telemetry

## Complexity represented

1. Multi-market localisation
2. Internal + outsourced vendor operating model
3. Role-based access context
4. Knowledge ownership and lifecycle
5. AI risk classification
6. Human escalation
7. Automated enablement intake
8. Adoption vs proficiency measurement
9. Audit traceability
10. Expired-content exclusion

## Production scale path

For thousands of sellers:
- Stateless API services behind load balancing
- SSO + RBAC/ABAC
- Dedicated model gateway with rate limits and model routing
- Vector store partitioned by policy/market/role
- Event streaming for telemetry
- Central policy-as-code service
- Immutable audit logging
- Offline evaluation suite + canary releases
- Observability for latency, cost, retrieval quality and safety
- Vendor tenancy and data-boundary controls
