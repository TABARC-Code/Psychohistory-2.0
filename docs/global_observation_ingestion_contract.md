# Global observation ingestion: evidence contract (experimental)

Godseye-style monitoring projects are discovery references, not trusted measurement sources. Collect from the original providers using documented APIs and permitted terms. Do not copy dashboards, credentials or data without verifying licences.

## First adapter: USGS earthquakes

Use USGS GeoJSON. Store immutable raw response hashes and per-event snapshots. Preserve source event ID, origin/effective time, provider updated time, first locally observed collection time, query URL, collector version, source attribution and a source-specific measurement ancestry token. A current USGS historical query is **not** a historical vintage. Never substitute origin or provider updated time for availability at an earlier forecast cutoff. Revisions append snapshots; they do not overwrite them.

Validate UTC-aware timestamps, bounded coordinates, finite numerical fields, duplicate IDs, missing data, clock anomalies and consistent snapshot identity. Quarantine malformed observations instead of silently dropping them. Avoid assuming different news reports and a USGS event are independent evidence of separate earthquakes.

## Admission and evaluation

All new feeds remain diagnostic-only. Do not route them into G23 until time-respecting empirical comparisons against base-rate, persistence, exposure-adjusted and common-shock alternatives have passed registered evidence and multiplicity requirements. Preserve G1 lineage and Hawkes equations; physical events are possible exogenous exposures, not automatically meme transmissions. Compare narrative-before-shock and shock-before-narrative directions, including reporting latency and common upstream causes.

## Next adapters

After USGS: one independently timestamped narrative source, then energy disruption, environmental hazards, transport and industrial indicators. Audit provider API limits, retention, licensing, revision behaviour, geographical coverage and outages individually. Prioritise historical reproducibility over dashboard layer count.

Reference: https://earthquake.usgs.gov/fdsnws/event/1/ and https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
