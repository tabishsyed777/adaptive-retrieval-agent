"""Adaptive Retrieval Agent domain retrieval and answer rules."""
NAME = '10-adaptive-retrieval-agent'

import re
from common import norm,require
FIELDS=("title","keywords","tier","value")

def validate(rows):
    seen=set()
    for r in rows:
        key=norm(r["tier"]),norm(r["title"])
        require(key not in seen,"duplicate tier/topic")
        seen.add(key)

def retrieve(rows,topic,tier):
    pool=[r for r in rows if norm(r["tier"])==tier]
    exact=[r for r in pool if norm(r["title"])==topic]
    if exact: return exact[0],"exact title"
    terms=set(topic.split())
    if terms & {"no","not","never","except","without"}: return
    scored=[]
    for r in pool:
        signatures=[set(norm(r[k]).split()) for k in ("title","keywords")]
        score=max(len(terms & s)/len(terms | s) for s in signatures)
        if score>=0.65: scored.append((score,r))
    scored.sort(key=lambda item:-item[0])
    if not scored or (len(scored)>1 and scored[0][0]==scored[1][0]): return
    return scored[0][1],"lexical fallback"

def solve(rows,q):
    q=q.rstrip("?")
    m=re.fullmatch(r"find (.+?) for (.+)",q)
    if m:
        hit=retrieve(rows,*m.groups())
        if hit: return hit[0]["value"],[hit[0]],hit[1]
        return
    m=re.fullmatch(r"compare (.+?) across tiers",q)
    if not m: return
    tiers=sorted({norm(r["tier"]) for r in rows})
    if len(tiers)<2: return
    hits=[retrieve(rows,m[1],tier) for tier in tiers]
    if not all(hits): return
    ev=[h[0] for h in hits]
    if len({norm(r["title"]) for r in ev})!=1: return
    return " | ".join(r["tier"]+": "+r["value"] for r in ev),ev,"decompose by tier: "+", ".join(h[1] for h in hits)
