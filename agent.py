#!/usr/bin/env python3
"""
Daily Reflection Tree — CLI Agent
Loads tree from JSON, walks it deterministically, accumulates state,
interpolates reflections, outputs final profile + depth modifiers.

Usage:
  python agent.py ../tree/reflection-tree.json
  python agent.py ../tree/reflection-tree.json --trace
  python agent.py ../tree/reflection-tree.json --replay A C A B A B
"""

import json
import re
import sys
import time
import textwrap
from typing import Optional

# System invariants (documented, enforced at test time):
#   1. Exactly 6 question nodes per session.
#   2. Every path terminates in one of 8 SUMMARY nodes.
#   3. Depth modifiers never change routing — rendering only.
#   4. Same answer sequence → same profile key. Always.

WIDTH = 72

def hr(char="─"):
    print(char * WIDTH)

def wrap(text: str, indent: int = 0):
    prefix = " " * indent
    for line in text.split("\n"):
        if line.strip() == "":
            print()
        else:
            for w in textwrap.wrap(line, WIDTH - indent, break_long_words=False):
                print(prefix + w)

def pause(seconds: float = 0.6):
    time.sleep(seconds)

def ask(prompt: str = "  Press Enter to continue..."):
    input(prompt)


class SessionState:
    def __init__(self):
        self.answers: dict         = {}
        self.classifications: dict = {}
        self.locus:        Optional[str] = None
        self.locus_depth:  Optional[str] = None
        self.orientation:  Optional[str] = None
        self.orient_depth: Optional[str] = None
        self.radius:       Optional[str] = None
        self.radius_depth: Optional[str] = None
        self._path: list        = []
        self._question_count: int = 0

    def record_question(self, node_id: str, key: str, option: dict):
        self.answers[node_id] = key
        classification = option.get("classification", "")
        self.classifications[node_id] = classification
        self._path.append(f"{node_id}:{key}")
        self._question_count += 1

        if   node_id == "Q2_I":    self.locus = "INTERNAL";    self.locus_depth  = classification
        elif node_id == "Q2_E":    self.locus = "EXTERNAL";    self.locus_depth  = classification
        elif node_id == "Q4_C":    self.orientation = "CONTRIBUTION"; self.orient_depth = classification
        elif node_id == "Q4_E":    self.orientation = "ENTITLEMENT";  self.orient_depth = classification
        elif node_id == "Q6_HIGH": self.radius = "HIGH"; self.radius_depth = classification
        elif node_id == "Q6_LOW":  self.radius = "LOW";  self.radius_depth = classification

    def profile_key(self) -> str:
        return f"{self.locus}+{self.orientation}+{self.radius}"

    def interpolate(self, text: str) -> str:
        def replace(m):
            return self.answers.get(m.group(1), m.group(0))
        return re.sub(r"\{(\w+)\.answer\}", replace, text)

    def trace_string(self) -> str:
        path = " → ".join(self._path)
        return (
            f"Path:    {path}\n"
            f"Profile: {self.profile_key()}\n"
            f"Depth:   {self.locus_depth}, {self.orient_depth}, {self.radius_depth}"
        )

    def as_record(self) -> dict:
        return {
            "answers":      self.answers,
            "locus":        self.locus,
            "locus_depth":  self.locus_depth,
            "orientation":  self.orientation,
            "orient_depth": self.orient_depth,
            "radius":       self.radius,
            "radius_depth": self.radius_depth,
            "profile":      self.profile_key(),
        }


def walk_start(node, state, replay):
    print(); hr("═"); print()
    wrap(node["text"]); print(); pause(1.0)
    return node["next"]

def walk_question(node, state, replay):
    print(); hr(); print()
    wrap(node["text"]); print()
    options = node["options"]
    for opt in options:
        wrap(f"  {opt['key']}.  {opt['text']}"); print()
    while True:
        if replay:
            raw = replay.pop(0).strip().upper()
            print(f"  Your answer: {raw}")
        else:
            raw = input("  Your answer: ").strip().upper()
        match = next((o for o in options if o["key"] == raw), None)
        if match:
            state.record_question(node["id"], raw, match)
            return match["next"]
        print("  Enter one of: " + ", ".join(o["key"] for o in options))

def walk_decision(node, state, replay):
    for route in node["routes"]:
        if _eval_condition(route["condition"], state):
            return route["next"]
    raise ValueError(f"No route matched for: {state.profile_key()}")

def _eval_condition(cond, state):
    for part in cond.split(" AND "):
        k, v = part.strip().split("==")
        if getattr(state, k.strip(), None) != v.strip():
            return False
    return True

def walk_reflection(node, state, replay):
    print(); print("·" * WIDTH); print()
    wrap(state.interpolate(node["text"]), indent=2); print(); pause(0.4)
    if not replay:
        ask("  (Continue) ")
    return node["next"]

def walk_bridge(node, state, replay):
    print(); wrap("  ─── " + node["text"]); print(); pause(0.8)
    return node["next"]

def walk_summary(node, state, tree, replay):
    print(); hr("═"); print()
    wrap(f"  {node['title'].upper()}"); print()
    wrap(node["text"], indent=2)
    modifiers = tree.get("depth_modifiers", {})
    fired = []
    for axis, depth_key in [
        ("locus",       state.locus_depth),
        ("orientation", state.orient_depth),
        ("radius",      state.radius_depth),
    ]:
        txt = modifiers.get(axis, {}).get(depth_key)
        if txt:
            fired.append(txt)
    if fired:
        print(); print("·" * WIDTH); print()
        for line in fired:
            wrap(line, indent=2); print()
    print(); hr(); print()
    print(f"  Locus       {state.locus}  ({state.locus_depth})")
    print(f"  Orientation {state.orientation}  ({state.orient_depth})")
    print(f"  Radius      {state.radius}  ({state.radius_depth})")
    print(f"  Profile     {state.profile_key()}")
    print(); hr("═"); print()
    return node["next"]

def walk_end(node, state, show_trace, replay):
    wrap("  " + node["text"]); print()
    if show_trace:
        print(); hr(); print()
        print("  AUDIT TRACE"); print()
        for line in state.trace_string().split("\n"):
            print(f"  {line}")
        print(); hr(); print()


def run(tree_path: str, show_trace: bool = False, replay: list = None):
    replay = list(replay) if replay else []
    with open(tree_path, "r") as f:
        tree = json.load(f)
    nodes = tree["nodes"]
    state = SessionState()
    current_id = tree["meta"]["entry_node"]
    while current_id is not None:
        node = nodes.get(current_id)
        if node is None:
            raise KeyError(f"Node '{current_id}' not found.")
        ntype = node["type"]
        if   ntype == "start":      current_id = walk_start(node, state, replay)
        elif ntype == "question":   current_id = walk_question(node, state, replay)
        elif ntype == "decision":   current_id = walk_decision(node, state, replay)
        elif ntype == "reflection": current_id = walk_reflection(node, state, replay)
        elif ntype == "bridge":     current_id = walk_bridge(node, state, replay)
        elif ntype == "summary":    current_id = walk_summary(node, state, tree, replay)
        elif ntype == "end":        walk_end(node, state, show_trace, replay); current_id = None
        else: raise ValueError(f"Unknown node type: {ntype}")
    return state


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python agent.py <tree.json> [--trace] [--replay A C A B A B]")
        sys.exit(1)
    tree_path   = args[0]
    show_trace  = "--trace" in args
    replay_answers = []
    if "--replay" in args:
        idx = args.index("--replay")
        replay_answers = args[idx + 1:]
    try:
        run(tree_path, show_trace=show_trace, replay=replay_answers)
    except KeyboardInterrupt:
        print("\n\n  Session ended early. No state saved.\n")
        sys.exit(0)
