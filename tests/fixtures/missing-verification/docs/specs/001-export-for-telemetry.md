# Export telemetry to CSV

**Status:** approved
**Date:** 2026-09-05
**Owner:** fleet team

## Summary

Export the in-memory telemetry buffer to CSV on demand.

## Goals & non-goals

Goal: one-click CSV export. Non-goal: real-time streaming.

## Users & scenarios

Fleet operators export a day of telemetry for offline analysis.

## Functional requirements

1. FR-1: The export action writes a CSV file containing every telemetry
   batch in the selected range.

## Acceptance criteria

1. AC-1.1: Exporting a range of 10 batches produces a CSV with 10 rows.

## Open questions & unknowns

None.

## Amendments

None.

## References

None.
