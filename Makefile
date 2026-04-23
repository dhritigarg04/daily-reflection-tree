TREE = tree/reflection-tree.json
AGENT = agent/agent.py

# Run interactive session
run:
	python $(AGENT) $(TREE)

# Run with audit trace printed after session
trace:
	python $(AGENT) $(TREE) --trace

# Replay a canonical path non-interactively (Victor persona)
replay-victor:
	python $(AGENT) $(TREE) --replay A C A B A B

# Replay the Victim persona
replay-victim:
	python $(AGENT) $(TREE) --replay B C B C D C

# Run full test suite (coverage, determinism, invariants)
test:
	python tests/coverage.py

.PHONY: run trace replay-victor replay-victim test
