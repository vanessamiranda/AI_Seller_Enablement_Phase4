# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
import pandas as pd

SCHEDULE = [0, 3, 7, 14, 30]

def reinforcement_plan(seller_id: str, proficiency: int, topic: str = "AI seller guidance"):
    if proficiency < 60:
        difficulty = "Foundation"
        cadence = SCHEDULE
    elif proficiency < 80:
        difficulty = "Applied"
        cadence = [0, 7, 14, 30]
    else:
        difficulty = "Advanced"
        cadence = [0, 14, 30]

    rows = []
    for day in cadence:
        activity = (
            "Scenario + guided feedback" if day in [0, 7] else
            "3-question retrieval check" if day == 3 else
            "Objection-handling exercise" if day == 14 else
            "Proficiency reassessment"
        )
        rows.append({
            "seller_id": seller_id,
            "day": day,
            "topic": topic,
            "difficulty": difficulty,
            "activity": activity,
            "human_coach_required": proficiency < 60 and day in [0, 7],
        })
    return pd.DataFrame(rows)


def learning_metrics(sellers: pd.DataFrame):
    df = sellers.copy()
    df["reinforcement_priority"] = pd.cut(
        df["proficiency"], bins=[-1,59,79,100], labels=["High","Medium","Low"]
    ).astype(str)
    return df.groupby("reinforcement_priority", as_index=False, observed=False).agg(
        sellers=("seller_id","count"),
        avg_proficiency=("proficiency","mean"),
        avg_adoption=("weekly_ai_adoption","mean")
    )
