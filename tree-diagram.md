# Reflection Tree — Branching Diagram

```mermaid
flowchart TD
    START([START]) --> Q1

    Q1["Q1 — Locus\nFirst instinct when something went wrong"]
    Q1 -->|A or D — Internal| Q2_I
    Q1 -->|B or C — External| Q2_E

    Q2_I["Q2_I — What you actually did\nwhen you hit the obstacle"]
    Q2_I -->|A/C = DEEP\nB/D = SHALLOW| REFLECT_INT

    Q2_E["Q2_E — How clearly you\ncan name the blocker"]
    Q2_E -->|A = CONCRETE\nB/C = DIFFUSE\nD = AVOIDANT| REFLECT_EXT

    REFLECT_INT(["Reflection: Locus Internal"]) --> BRIDGE_12
    REFLECT_EXT(["Reflection: Locus External"]) --> BRIDGE_12

    BRIDGE_12["Bridge 1→2"] --> Q3

    Q3["Q3 — Orientation\nWhat crosses your mind about work done"]
    Q3 -->|A or D — Contribution| Q4_C
    Q3 -->|B or C — Entitlement| Q4_E

    Q4_C["Q4_C — Why contribution matters\nto your sense of the day"]
    Q4_C -->|A=DEEP, B=BALANCED\nC=SELECTIVE, D=INTRINSIC| REFLECT_C

    Q4_E["Q4_E — Where you are\non what you're owed"]
    Q4_E -->|A=LOW, B=GAP\nC=COMPARATIVE, D=FRUSTRATED| REFLECT_E

    REFLECT_C(["Reflection: Contribution"]) --> BRIDGE_23
    REFLECT_E(["Reflection: Entitlement"]) --> BRIDGE_23

    BRIDGE_23["Bridge 2→3"] --> Q5

    Q5["Q5 — Radius\nWho else is in your head right now"]
    Q5 -->|A or B — Others| Q6_HIGH
    Q5 -->|C or D — Self| Q6_LOW

    Q6_HIGH["Q6_HIGH — What you did\nwith that awareness"]
    Q6_HIGH -->|A=ACTIVE, B=DELIBERATE\nC=PASSIVE, D=UNCERTAIN| REFLECT_HIGH

    Q6_LOW["Q6_LOW — Texture of a\nself-focused day"]
    Q6_LOW -->|A=JUSTIFIED, B=REFLECTIVE\nC=DEFAULT, D=PROTECTIVE| REFLECT_LOW

    REFLECT_HIGH(["Reflection: High Radius"]) --> DECISION
    REFLECT_LOW(["Reflection: Low Radius"]) --> DECISION

    DECISION{{"Final Profile\nDecision Node"}}

    DECISION -->|INT+CON+HIGH| ICH["The Integrated Agent"]
    DECISION -->|INT+CON+LOW| ICL["The Productive Isolate"]
    DECISION -->|INT+ENT+HIGH| IEH["The Aware Deficit Tracker"]
    DECISION -->|INT+ENT+LOW| IEL["The Self-Referential Agent"]
    DECISION -->|EXT+CON+HIGH| ECH["The Generous Attributor"]
    DECISION -->|EXT+CON+LOW| ECL["The Disconnected Contributor"]
    DECISION -->|EXT+ENT+HIGH| EEH["The Sensitized Observer"]
    DECISION -->|EXT+ENT+LOW| EEL["The Closed Circuit"]

    ICH --> END([END])
    ICL --> END
    IEH --> END
    IEL --> END
    ECH --> END
    ECL --> END
    EEH --> END
    EEL --> END
```

---

## Node count

| Type | Count |
|------|-------|
| start | 1 |
| question | 6 |
| decision | 1 (final routing) |
| reflection | 6 |
| bridge | 2 |
| summary | 8 |
| end | 1 |
| **Total** | **25** |

---

## All possible conversation paths

Every session traverses exactly 6 questions. The path is:

```
START → Q1 → [Q2_I or Q2_E] → REFLECT_LOCUS → BRIDGE_1_2
     → Q3 → [Q4_C or Q4_E] → REFLECT_ORIENT → BRIDGE_2_3
     → Q5 → [Q6_HIGH or Q6_LOW] → REFLECT_RADIUS
     → DECISION_FINAL → [one of 8 SUMMARY nodes] → END
```

Total distinct full paths: **2³ = 8 terminal profiles × 4 option combinations per question = 4096 unique answer sequences**, all mapping into 8 profile keys.

---

## Depth modifier overlay

Depth tags are stored at Q2, Q4, and Q6 and appended to the summary output post-render. They do not change the branching path — only the modifier text appended to the final profile.
