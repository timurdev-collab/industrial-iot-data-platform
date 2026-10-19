"""Executable SQL data-quality checks for the local telemetry warehouse."""
import argparse
import json
import sqlite3

CHECKS = {
    "no_null_business_keys": """
        SELECT COUNT(*) FROM raw_events
        WHERE event_id IS NULL OR sensor_id IS NULL OR timestamp IS NULL
    """,
    "no_orphan_sensors": """
        SELECT COUNT(*) FROM raw_events r
        LEFT JOIN dim_sensor d ON r.sensor_id = d.sensor_id
        WHERE d.sensor_id IS NULL
    """,
    "no_invalid_numeric_ranges": """
        SELECT COUNT(*) FROM raw_events
        WHERE pressure_bar < 0 OR pressure_bar > 20
           OR flow_lpm < 0 OR flow_lpm > 1000
           OR temperature_c < -40 OR temperature_c > 120
    """,
    "fact_counts_match_raw": """
        SELECT ABS(
          (SELECT COUNT(*) FROM raw_events) -
          (SELECT COALESCE(SUM(event_count),0) FROM fact_sensor_hourly)
        )
    """,
    "no_negative_anomaly_counts": """
        SELECT COUNT(*) FROM fact_sensor_hourly
        WHERE anomaly_count < 0 OR anomaly_count > event_count
    """
}

def check(db_path):
    with sqlite3.connect(db_path) as con:
        results = {name: con.execute(sql).fetchone()[0] for name, sql in CHECKS.items()}
    return {"passed": all(value == 0 for value in results.values()),
            "violations": results}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--db", default="data/telemetry.db")
    result = check(p.parse_args().db)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
