# Copyright © 2026 Vanessa Miranda. All rights reserved. Proprietary source-available software; see LICENSE.
from app.retrieval import GovernedRetriever

def test_expired_content_not_returned():
    r = GovernedRetriever("data/knowledge_base.csv")
    docs = r.search("outdated product play", market="Malaysia")
    assert all(d["status"] == "Approved" for d in docs)
