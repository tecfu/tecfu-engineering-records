# Fleet overflow lost telemetry batches

**Status:** closed
**Date:** 2026-09-05

## Summary

The telemetry queue overflowed during the fleet update.

## Impact

Roughly 400 batches were dropped across 12 vehicles.

## Timeline

- 09:00 update started
- 09:14 queue overflow
- 10:02 batches restored from the edge cache

## Root causes

The queue bound was sized for the old batch rate.

## Lessons

Queue bounds must be derived from peak rates.

## Actions

- Size queue bounds from the 99th percentile batch rate.

## References

None.
