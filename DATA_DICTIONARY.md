# AI Seller Enablement — Data Dictionary

Version: 1.0

## Seller Performance Dataset

| Field | Type | Description |
|------|------|-------------|
| seller_id | String | Anonymous seller identifier |
| seller_name | String | Fictional seller name |
| market | Category | Country or region |
| manager | String | Reporting manager |
| revenue_target | Number | Quarterly sales target |
| revenue_actual | Number | Actual sales achieved |
| revenue_attainment | Percentage | Target attainment |
| pipeline_value | Currency | Qualified pipeline |
| conversion_rate | Percentage | Opportunity conversion |
| training_completion | Percentage | LMS completion |
| certification_level | Category | Foundation / Advanced / Expert |
| skill_gap | Category | Primary capability gap |
| ai_risk_score | Integer | AI-generated priority score (0–100) |
| risk_level | Category | Low / Medium / High |
| recommended_action | Text | Suggested enablement intervention |
| alert_trigger | Text | Business rule causing escalation |

---

## Risk Score Logic

| Score | Priority |
|------|----------|
| 0–39 | Low |
| 40–69 | Medium |
| 70–100 | High |

The score combines weighted performance, learning, and behavioural signals.

---

## Data Governance

- No personal data
- No customer information
- Synthetic seller records only
- Demonstration environment
