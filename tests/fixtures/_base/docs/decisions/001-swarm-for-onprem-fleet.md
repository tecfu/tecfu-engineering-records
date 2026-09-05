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

| Criterion (weight) | Swarm | Basis |
|---|---|---|
| cost (5) | 4 | benchmarked on the test fleet |

Closeness: Swarm 80%.

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
