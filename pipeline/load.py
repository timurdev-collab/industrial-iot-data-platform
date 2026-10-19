import argparse, datetime as dt, json, sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS raw_events (
 event_id TEXT PRIMARY KEY, sensor_id TEXT NOT NULL, timestamp TEXT NOT NULL,
 pressure_bar REAL NOT NULL, flow_lpm REAL NOT NULL, temperature_c REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS dim_sensor (sensor_id TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS fact_sensor_hourly (
 sensor_id TEXT NOT NULL, hour TEXT NOT NULL, event_count INTEGER NOT NULL,
 avg_pressure_bar REAL NOT NULL, avg_flow_lpm REAL NOT NULL,
 anomaly_count INTEGER NOT NULL, PRIMARY KEY(sensor_id,hour)
);
"""

def validate(record):
    keys = ('event_id','sensor_id','timestamp','pressure_bar','flow_lpm','temperature_c')
    if any(key not in record for key in keys):
        return False
    try:
        dt.datetime.fromisoformat(record['timestamp'])
        return (bool(record['event_id']) and bool(record['sensor_id']) and
            0 <= float(record['pressure_bar']) <= 20 and
            0 <= float(record['flow_lpm']) <= 1000 and
            -40 <= float(record['temperature_c']) <= 120)
    except (ValueError, TypeError):
        return False

def load(input_path, db_path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    try:
        con.executescript(SCHEMA)
        inserted = invalid = 0
        with open(input_path, encoding='utf-8') as f:
            for line in f:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    invalid += 1
                    continue
                if not isinstance(row, dict) or not validate(row):
                    invalid += 1
                    continue
                before = con.total_changes
                con.execute('INSERT OR IGNORE INTO raw_events VALUES(?,?,?,?,?,?)',
                    tuple(row[k] for k in ('event_id','sensor_id','timestamp','pressure_bar','flow_lpm','temperature_c')))
                inserted += con.total_changes-before
        con.execute('INSERT OR IGNORE INTO dim_sensor SELECT DISTINCT sensor_id FROM raw_events')
        con.execute('DELETE FROM fact_sensor_hourly')
        con.execute("""INSERT INTO fact_sensor_hourly
          SELECT sensor_id, substr(timestamp,1,13)||':00:00', COUNT(*),
                 AVG(pressure_bar), AVG(flow_lpm),
                 SUM(CASE WHEN pressure_bar < 2.5 OR flow_lpm < 65 THEN 1 ELSE 0 END)
            FROM raw_events GROUP BY sensor_id, substr(timestamp,1,13)""")
        con.commit()
        return {'inserted': inserted, 'invalid': invalid,
                'total': con.execute('SELECT COUNT(*) FROM raw_events').fetchone()[0]}
    finally:
        con.close()

if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--input', default='data/events.jsonl')
    a.add_argument('--db', default='data/telemetry.db')
    args = a.parse_args()
    print(load(args.input,args.db))
