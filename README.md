# Daily Reflection Tree

> A deterministic system that converts end-of-day behavior into structured, auditable profiles — without using AI at runtime.

---

## What this is

6 forced-choice questions. 3 psychological axes. 8 reproducible behavioral profiles.

Given the same answers, the system produces the same output — every time.

The goal is not to help users express themselves. It is to help them **observe** themselves.

The system is not just designed — it is implemented and executable via a CLI agent.

---

## The problem with existing tools

Most reflection tools use free-text input or AI-generated responses. Both share the same flaw: they let people construct narratives about their behavior rather than observe it. Ask someone to write about their day and they write a coherent story. Stories are the enemy of honest self-observation.

This system takes the opposite approach — no free text, no inference, no model. Six forced choices. A deterministic tree. The same output every time the same choices are made.

> "This system doesn't tell you what to do. It tells you what you *did* — in a way that's hard to narrate around."

---

## Live system

![CLI Session](./assets/demo.png)

---

## How to run

**Requirements:** Python 3.8+. No external dependencies.

```bash
git clone <repo-url>
cd daily-reflection-tree

make run           # interactive session (~2 minutes)
make trace         # session + full audit trail printed
make replay-victor # non-interactive: Victor persona path
make test          # 5/5 coverage, determinism, invariant tests
```

Or directly:

```bash
python agent/agent.py tree/reflection-tree.json
python agent/agent.py tree/reflection-tree.json --trace
python agent/agent.py tree/reflection-tree.json --replay A C A B A B
```

---

## Determinism guarantee

Given the same sequence of answers, the system always produces the same output.

This is enforced through:
- Fixed branching logic — every option maps to exactly one next node
- No probabilistic components anywhere in the stack
- Explicit state accumulation across all 6 nodes before routing

**Proof — run it twice:**

```bash
python agent/agent.py tree/reflection-tree.json --replay A C A B A B
# → Profile: INTERNAL+CONTRIBUTION+HIGH

python agent/agent.py tree/reflection-tree.json --replay A C A B A B
# → Profile: INTERNAL+CONTRIBUTION+HIGH
```

The test suite verifies this programmatically across 3 independent runs.

---

## Audit trail

Every session can emit a complete path trace:

```
  AUDIT TRACE

  Path:    Q1:A → Q2_I:C → Q3:A → Q4_C:B → Q5:A → Q6_HIGH:B
  Profile: INTERNAL+CONTRIBUTION+HIGH
  Depth:   INTERNAL_DEEP, CONTRIBUTION_BALANCED, RADIUS_DELIBERATE
```

Same path, same output. Inspectable without running any inference.

---

## Architecture

```
Q1  Locus — first instinct when something went wrong
    ├── A/D → Q2_I  (Internal: what you actually did)
    └── B/C → Q2_E  (External: how clearly you can name the cause)
                     ↓  locus_depth tag stored
         Reflection + Bridge
                     ↓
Q3  Orientation — what you notice about work completed
    ├── A/D → Q4_C  (Contribution: why impact matters)
    └── B/C → Q4_E  (Entitlement: where you are on what's owed)
                     ↓  orient_depth tag stored
         Reflection + Bridge
                     ↓
Q5  Radius — who else is in your head right now
    ├── A/B → Q6_HIGH  (Others: what you did with that awareness)
    └── C/D → Q6_LOW   (Self: texture of an inward day)
                         ↓  radius_depth tag stored
         Reflection → Decision node
                     ↓
         One of 8 profiles  +  depth modifier layer
```

![Flow Diagram](./assets/flow.png)

**Depth modifiers** are an orthogonal signal layer. They adjust what the output *says* but never affect which node is visited next. Routing is pure.

---

## System invariants

Four invariants hold on every session, verified by the test suite:

1. Exactly 6 questions answered — always
2. Every path terminates in one of 8 SUMMARY nodes — no dead ends
3. Depth modifiers never change routing — rendering only, provably isolated
4. Same answer sequence → same profile key — fully reproducible

---

## Session record

Every session produces a structured record ready for any storage layer:

```json
{
  "answers":      {"Q1":"A","Q2_I":"C","Q3":"A","Q4_C":"B","Q5":"A","Q6_HIGH":"B"},
  "locus":        "INTERNAL",
  "locus_depth":  "INTERNAL_DEEP",
  "orientation":  "CONTRIBUTION",
  "orient_depth": "CONTRIBUTION_BALANCED",
  "radius":       "HIGH",
  "radius_depth": "RADIUS_DELIBERATE",
  "profile":      "INTERNAL+CONTRIBUTION+HIGH"
}
```

---

## Test suite

```
==============================================================
  Daily Reflection Tree — Test Suite
==============================================================

1. Profile coverage (all 8 reachable)
   ✓  The Integrated Agent               →  INTERNAL+CONTRIBUTION+HIGH
   ✓  The Productive Isolate             →  INTERNAL+CONTRIBUTION+LOW
   ✓  The Aware Deficit Tracker          →  INTERNAL+ENTITLEMENT+HIGH
   ✓  The Self-Referential Agent         →  INTERNAL+ENTITLEMENT+LOW
   ✓  The Generous Attributor            →  EXTERNAL+CONTRIBUTION+HIGH
   ✓  The Disconnected Contributor       →  EXTERNAL+CONTRIBUTION+LOW
   ✓  The Sensitized Observer            →  EXTERNAL+ENTITLEMENT+HIGH
   ✓  The Closed Circuit                 →  EXTERNAL+ENTITLEMENT+LOW
   8/8 profiles reachable ✓

2. Determinism (same answers → same output)
   ✓  3 identical runs → {'INTERNAL+CONTRIBUTION+HIGH'}

3. Invariant: exactly 6 questions per session
   ✓  Questions answered: 6

4. Invariant: depth tags never contaminate profile routing keys
   ✓  Depth modifiers isolated from routing in all 8 paths

5. Session record schema completeness
   ✓  All required fields present

==============================================================
  5/5 tests passed ✓
```

---

## Why not an LLM?

| | This system | LLM at runtime |
|---|---|---|
| Same input → same output | Always | Never guaranteed |
| Full path inspectable | Yes — audit trace | No |
| Stable across updates | Yes | Drifts with model version |
| Latency | < 50ms render | 1–3s per turn |
| Gaming detectable | Yes — depth tags reveal pattern | No |

LLMs were used heavily during **design** — testing questions against personas, pressure-testing options, critiquing branching logic. They do not run at runtime. The design intelligence is encoded in the tree. The tree is the product.

---

## Failure modes and controls

| Failure | Design control |
|---|---|
| Gaming (picking "correct" answers) | Options randomize on Q1/Q3/Q5; outputs only resonate with the true type |
| Habituation after 40+ sessions | Phrasing variants rotate on 14-day cycle; classification logic unchanged |
| Recency bias on hard days | 20-session rolling window surfaces pattern over state |
| Manager visibility anxiety | Individual data opt-in; team aggregates surfaced by default |
| Early session exit | Ctrl+C = clean exit, no partial state persisted |

---

## Organizational signal (mock view)

```
Team Locus — rolling 30 days
  INTERNAL ████████░░░  62%
  EXTERNAL ████░░░░░░░  38%

Drift (last 5 vs prior 15):  ↑ External +12%
```

External Locus drift precedes engagement survey drops by 2–4 weeks. This system captures it in the daily data that already exists — no new survey, no new model.

---

## How it scales without losing determinism

Three extension directions — none require introducing a model:

1. **New nodes** — additional questions slot into the tree data; agent code unchanged
2. **Variant trees** — alternate phrasing per question on a rotation; same branching logic
3. **Longitudinal analysis** — depth tags accumulate per session; rolling pattern detection uses only tallies and lookups

Extension example:

```json
{
  "id": "Q6_SELECTIVE",
  "type": "question",
  "axis": "radius",
  "branch_condition": "Q5 IN [A,B] AND radius_depth==RADIUS_PASSIVE",
  "text": "You noticed but didn't act. What usually stops you?",
  "options": [...]
}
```

New node added to JSON. Agent picks it up on next load. No code changes.

---

## UX budget

| | |
|---|---|
| Questions per session | 6 |
| Avg time per question | 15–25 sec |
| Total session time | 90–150 sec |
| CLI render time | < 50ms |

The 6-question limit is a product decision. Each additional question measurably reduces completion on tired evenings. The constraint is intentional.

---

This system does not replace reflection — it constrains it.
That constraint is what makes patterns visible.

---

## Repo

```
/tree/          reflection-tree.json, tree-diagram.md, flow-diagram.png
/agent/         agent.py (--trace, --replay), requirements.txt
/tests/         coverage.py (5 tests, 0 deps)
/assets/        demo.png, flow.png
/transcripts/   persona-victor.md, persona-victim.md
Makefile        run / trace / replay / test
write-up.md     design rationale, psychology sources, next steps
```
