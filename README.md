# Industrial IoT Data Platform

A reproducible, local-first **data engineering portfolio project** for synthetic industrial sensor telemetry.

## Features
- Generate deterministic pressure, flow and temperature readings in JSONL.
- Validate records, reject malformed/out-of-range events and deduplicate by event ID.
- Load into SQLite raw and dimensional tables.
- Calculate hourly aggregates and anomaly flags.
- Automated tests and GitHub Actions CI.

**Scope:** This is a local Python + SQLite ETL demonstration. It does not use Kafka, Airflow, dbt, PostgreSQL or a deployed cloud pipeline.

## Run
Requires Python 3.10+; no external runtime dependencies.

```bash
python -m pipeline.generate --out data/events.jsonl --count 2000
python -m pipeline.load --input data/events.jsonl --db data/telemetry.db
python -m pipeline.report --db data/telemetry.db
python -m unittest discover -s tests -v
```

Synthetic data is generated for demonstration, not collected from real SCADA equipment. Generated database and events are ignored by Git.
