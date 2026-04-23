# Submission Email

---

**To:** tarun@deepthought.education  
**Subject:** DT Fellowship — Daily Reflection Tree (deterministic behavioral system)

---

Hi Tarun,

Submitting my DT Fellowship assignment: a deterministic behavioral reflection system built on three psychological axes — Locus, Orientation, Radius.

What's in the repo:

- **Tree data** (`reflection-tree.json`) — 28 nodes, 8 profiles, depth modifier layer, fully traceable without running code
- **CLI agent** (`agent/agent.py`) — loads the JSON, walks it, outputs profile + audit trail. No external dependencies.
- **Test suite** (`tests/coverage.py`) — proves all 8 profiles reachable, determinism across 3 runs, 6-question invariant, modifier isolation
- **Two transcripts** — complete sessions for opposing personas showing different paths and outputs

The system uses LLMs for design (question iteration, persona testing, option critique) and zero LLMs at runtime. The intelligence is in the tree structure.

To run:

```bash
make run      # interactive session
make test     # 5/5 tests passing
make trace    # session + full audit trail
```

Repo: https://github.com/dhritigarg04/daily-reflection-tree

Happy to walk through any design trade-off — the branching architecture, the depth modifier layer, the failure modes, or what I'd build next.

— Dhriti Garg
