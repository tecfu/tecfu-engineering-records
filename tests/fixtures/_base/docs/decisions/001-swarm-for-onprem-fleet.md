# 001 — Swarm for on-prem fleet

**Status:** accepted
**Date:** 2026-09-05
**Deciders:** fleet team
**Supersedes:** —

## Context and problem statement

The fleet needs coordination without cloud dependence.

## Decision drivers

- cost
- offline operation

## Considered options

- Swarm — self-coordinating agents
- Central broker — cloud dependency

## Decision matrix

| Criterion (weight) | Swarm | Central broker | Basis |
|---|---|---|---|
| cost (5 / 62.5%) | 4 | 2 | benchmarked on the test fleet |
| ops simplicity (3 / 37.5%) | 3 | 4 | judgment — fewer parts for us to run |
| **Total** | **72.5%** | **60.0%** | — |

Closeness: Swarm leads Central broker by 7 points. A 2-point score drop on
ops simplicity would flip it.

## Trade-offs

Swarm converges slower than a central broker.

## Decision

Swarm.

## Consequences

Agents need the gossip port open on-prem.

## Open questions & unknowns

None.

## References

None.
