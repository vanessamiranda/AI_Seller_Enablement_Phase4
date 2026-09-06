# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
import pandas as pd

INCIDENTS = [
    ["INC-001", "Retrieval", "Medium", "Indonesia", "Assistant failed to retrieve a relevant measurement article", "Contained", "Knowledge Management", "Added retrieval test and knowledge-gap review"],
    ["INC-002", "Knowledge", "High", "Malaysia", "Expired product guidance detected in corpus", "Resolved", "Product Enablement", "Status gate prevents expired content from surfacing"],
    ["INC-003", "Privacy", "High", "Singapore", "Synthetic user entered an email address into prompt", "Contained", "Privacy / AI Governance", "Input blocked and user prompted to redact"],
]

def incident_log():
    return pd.DataFrame(INCIDENTS, columns=["incident_id","type","severity","market","description","status","owner","corrective_action"])
