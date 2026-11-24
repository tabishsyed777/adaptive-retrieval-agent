# Adaptive Retrieval Agent

Route each lookup through exact title matching, then lexical retrieval if needed. For comparison, decompose the question by tier, retrieve evidence separately, and synthesize only when the retrieved topics agree.

## Quick start

From this directory, run these commands with Python 3.12 or 3.13. The example corpus is fictional and runs offline with the standard library.

```sh
python3 core.py ask 'Find artifact retention for basic'
python3 core.py build data/source.json snapshot.json
python3 core.py ask 'Find build archives for plus' --snapshot snapshot.json
python3 -m unittest discover -v
python3 evaluate.py
```

## Asking questions

Ask “Find build archives for plus” for lexical fallback or “Compare artifact retention across tiers” for multi-step retrieval.

## Using your own sources

Use the records in `data/source.json` as a schema example. Supply unique citation IDs and usable source locators. Build a new snapshot after additions, edits, or deletions. A successful build atomically replaces the previous snapshot. Results contain the answer, retrieval method and source locators. Unsupported queries return `insufficient_evidence`.

A deterministic, bounded routing policy supports lookup and tier comparison. Token-set similarity needs vocabulary overlap. Ties abstain.

See [QA.md](QA.md) for measured results, review status and release limits.
