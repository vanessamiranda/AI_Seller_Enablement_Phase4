# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class GovernedRetriever:
    def __init__(self, csv_path="data/knowledge_base.csv"):
        self.df = pd.read_csv(csv_path).fillna("")
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
        corpus = (
            self.df["title"] + " " + self.df["topic"] + " " +
            self.df["market"] + " " + self.df["segment"] + " " +
            self.df["role"] + " " + self.df["content"]
        )
        self.matrix = self.vectorizer.fit_transform(corpus)

    def search(self, query, market="Global", segment="All", role="All", top_k=4):
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix).flatten()
        work = self.df.copy()
        work["score"] = scores

        # Governance gate: only Approved content may reach generation.
        work = work[work["status"] == "Approved"]

        # Context-aware ranking: boosts relevant market/segment/role without
        # blocking global or cross-role guidance.
        work["context_boost"] = (
            work["market"].isin([market, "Global"]).astype(float) * 0.08 +
            work["segment"].isin([segment, "All"]).astype(float) * 0.05 +
            work["role"].isin([role, "All"]).astype(float) * 0.05
        )
        work["final_score"] = work["score"] + work["context_boost"]
        work = work.sort_values("final_score", ascending=False).head(top_k)
        return work.to_dict("records")
