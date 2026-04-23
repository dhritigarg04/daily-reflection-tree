# Daily Reflection Tree — Design Rationale

---

## Why this project

Most reflection tools rely on free-text journaling or AI-generated responses. Both approaches share the same flaw: they reinforce narratives rather than reveal patterns. Ask someone to write about their day and they will write a coherent story. Stories are the enemy of self-observation.

This project takes a different approach:

- No free text
- No AI at runtime
- Only deterministic branching

The goal is not expression — it is structured self-observation.

The system is designed as a behavioral diagnostic tool, not a journaling aid. It does not ask how you feel. It asks what you did, what you noticed, and who was in your field of awareness. Then it routes you — the same way, every time — to an output that describes the pattern those choices reveal.

This is the kind of system DeepThought builds: structured, auditable, and honest before it is comfortable.

---

## 0. Why this system exists

Most reflection tools fail for the same reason: they ask people to explain themselves in free text after the fact. That produces narratives, not insight. People are good at building coherent stories about their behavior. That skill works against honest self-observation.

This system takes the opposite bet. It constrains the user into forced choices at the moment of reflection — before they've had time to compose a flattering account. The goal isn't self-expression. It's self-observation.

The design assumption underneath everything: if you make someone choose between four uncomfortable but plausible descriptions of their own behavior, you surface patterns they would not voluntarily report.

The tree is an attempt to encode that idea into something deterministic and auditable.

---

## 1. Why these questions

**Axis 1 — Locus.** The hardest thing about measuring internal vs. external locus isn't the classification — it's that almost everyone has learned to *say* they believe in personal accountability. The standard self-report locus scales (Rotter, 1966) are trivially gameable.

The tree bypasses this by asking behavioral questions, not attitudinal ones. Q1 asks where attention *went first*, not what the person believes about agency in general. Q2 asks what they *actually did*, not what they think one should do. The behavioral frame is harder to curate under mild time pressure.

Q1's revised framing — "before you had time to think about it" — is doing the most work. It blocks post-hoc rationalization by invoking the moment before the story formed.

**Axis 2 — Orientation.** Contribution vs. Entitlement is a spectrum that almost everyone misreports. Entitlement is invisible to the person holding it (Campbell et al., 2004) — it's experienced as reasonable expectation, not entitlement. Asking "do you have an entitlement orientation?" is useless.

The tree makes it visible through Q3's framing: *not the most important thing, just anything done*. Stripping the importance-framing removes the social pressure to frame output in terms of impact. What someone notices about ordinary, unremarkable work is a cleaner signal than what they say about their most significant contribution.

**Axis 3 — Radius.** Q5's "who else is in the room in your head" is the metaphor the whole axis depends on. It bypasses normative response ("I'm always aware of my team") by making the question spatial and present-tense. You're not asking what they value or who they care about in principle — you're asking what's actually occupying cognitive space at this specific moment.

Maslow's 1969 work on self-transcendence frames the outward orientation not as altruism but as the direction in which meaning becomes available. That's the underlying reason this axis matters: Radius Low is not bad — it's just closed. And closed loops, repeated over time, narrow.

---

## 2. How I designed the branching

**The depth tag architecture.** Early drafts collapsed each axis into a binary (Internal/External, Contribution/Entitlement, High/Low). That worked for routing but threw away useful signal. The depth tags — INTERNAL_DEEP vs. INTERNAL_SHALLOW, CONTRIBUTION_SELECTIVE vs. CONTRIBUTION_BALANCED, etc. — were added as a second layer that doesn't affect routing but modifies output.

This was a specific architectural choice: don't make the tree more complex by adding more branches. Make it more precise by accumulating signal within a fixed structure. The depth modifier appended to the final output is a separate rendering pass — which keeps the core tree clean and the enrichment optional.

**The trade-off I made on Q4_E option A.** When someone routes to Q4_E (Entitlement branch) and selects "Not thinking about it — I'm focused on what I'm building," they're classified ENTITLEMENT_LOW. This is probably a routing error — they may have answered Q3 in terms of completion satisfaction (a genuine response) rather than recognition-seeking. The system doesn't redirect them; it records ENTITLEMENT_LOW as a depth tag and generates no modifier. This is acceptable: over 20 sessions, a user who always lands in Q4_E but always selects A reveals something in the longitudinal pattern even if any single session is ambiguous.

**Where I held back.** The tree could branch further — the depth tags could drive separate sub-paths rather than just modifier text. I chose not to do this because: (a) it would require 24+ additional nodes to cover meaningfully, (b) the depth signal is most useful aggregated over time, and (c) a 6-question session that takes under 4 minutes is a product; an 8-question session that takes 7 minutes is a chore. Length is a product decision, not just a design decision.

---

## 3. Psychological sources

- **Rotter (1966)** — Locus of Control scale. The tree doesn't use the scale; it uses the construct operationalized behaviorally.
- **Dweck (2006)** — Growth Mindset. Informs the Q2_I depth split: INTERNAL_DEEP (adaptation) vs. INTERNAL_SHALLOW (persistence without learning). Pushing harder on a failing approach is an internal attribution without growth orientation.
- **Campbell, Bonacci, et al. (2004)** — Psychological Entitlement Scale. Q4_E's options map to the three entitlement subtypes in their work: perceived gap (equity-based), comparative (superiority-based), frustrated expectation (structural).
- **Organ (1988)** — Organizational Citizenship Behavior. Contribution orientation in Axis 2 maps to OCB's construct of discretionary effort beyond formal role requirements.
- **Maslow (1969)** — "The farther reaches of human nature." Axis 3's Radius construct draws on Maslow's self-transcendence stage — the shift from self-actualization to concern for something beyond the self. The Q5 metaphor ("who else is in the room in your head") is an attempt to make this observable in daily behavior.

---

## 4. What I would build next

Three directions, in priority order:

**Temporal intelligence.** A single session captures state, not trajectory. The meaningful output is the 20-session rolling window: what is the dominant profile, and what has drifted in the last 5 sessions versus the prior 15? State is situational. Trait is what appears when you remove situation variance. This distinction — between a person having a hard week and a person whose orientation has shifted — is the most actionable thing the system could surface for a manager.

**Manager interface.** Individual profile data (opt-in only) is interesting. Team aggregate data is operationally useful. A manager looking at a 30-day External Locus trend for their team has a 3-week early warning signal before engagement collapses — no existing tool produces this. The interface question is: what's the minimum viable read for a team lead who has 8 minutes before a 1-on-1? A single axis heatmap per team member, updated weekly, is probably the answer.

**Tree variants without LLMs.** The current tree has one entry node for all sessions. After 40+ sessions, users habitualize and stop reading carefully. The solution isn't an LLM — it's 2-3 validated phrasing variants per question, rotated on a 14-day cycle, with identical classification logic. Same tree, different surface. The behavioral signal is preserved; the habituation is broken. This is a knowledge engineering problem, not an AI problem.

The goal in all three cases is not to make the system more complex. It's to make it more *situationally precise* — the same six questions producing richer signal because the context around them is better designed.

---

## 5. Why this stays deterministic at scale

This system is intentionally designed as a tree, not a model. That choice is load-bearing — not a constraint of scope.

It can be extended by:
- **Adding new nodes** — deeper probing on any axis without touching the router
- **Introducing variant trees** — alternate phrasing per question on a 14-day rotation, same classification logic, breaks habituation without breaking determinism
- **Layering longitudinal analysis** — the state schema already logs axis + depth tags per session; a rolling 20-session window reveals trait vs. situational patterns using nothing but tallies and lookups

No step in that roadmap requires introducing non-determinism. The intelligence grows inside the structure, not by replacing it with a model.

---

## 6. One honest limitation

The tree has a mild Internal + Contribution + High bias in what "healthy" looks like. The profile names make this visible — "Integrated Agent" carries more positive valence than "Closed Circuit." This is difficult to eliminate entirely because the psychological frameworks the tree draws on have normative assumptions baked in. Locus of Control research has consistently found that internal orientation correlates with better outcomes. Contribution orientation research shows the same.

The mitigation is not to pretend the tree is value-neutral — it isn't — but to communicate it clearly as a *diagnostic instrument*, not a scorecard. The output should feel like an accurate description of today, not a grade. The rewritten profiles in v2 attempt this: they describe patterns without prescribing corrections. Whether that fully neutralizes the normativity is an empirical question that only longitudinal data can answer.
