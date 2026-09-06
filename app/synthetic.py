# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
import random
import pandas as pd

MARKETS = ["Singapore","Malaysia","Indonesia","Thailand","Philippines","Vietnam","Korea","Taiwan"]
VENDORS = ["Internal Sales","Vendor A - Manila","Vendor B - Kuala Lumpur","Vendor C - Bangalore"]
ROLES = ["Account Manager","Sales Manager","Trainer"]
SEGMENTS = ["SMB","Mid-Market"]

def seller_population(n=530, seed=42):
    random.seed(seed)
    rows = []
    for i in range(1, n+1):
        vendor = random.choices(VENDORS, weights=[35,25,22,18])[0]
        adoption = max(0, min(100, int(random.gauss(71 if vendor=="Internal Sales" else 64, 16))))
        proficiency = max(0, min(100, int(random.gauss(78 if vendor=="Internal Sales" else 70, 13))))
        rows.append({
            "seller_id": f"S{i:04d}",
            "market": random.choice(MARKETS),
            "vendor": vendor,
            "role": random.choices(ROLES, weights=[78,12,10])[0],
            "segment": random.choice(SEGMENTS),
            "weekly_ai_adoption": adoption,
            "proficiency": proficiency,
            "certified": proficiency >= 75,
            "human_escalations": random.randint(0,5),
        })
    return pd.DataFrame(rows)
