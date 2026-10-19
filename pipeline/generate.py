import argparse, datetime as dt, json, random
from pathlib import Path

def generate(count=2000, seed=42):
    rng = random.Random(seed)
    start = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
    records = []
    for i in range(count):
        sensor = f"S-{i % 8:02d}"
        abnormal = (i % 97 == 0)
        records.append({"event_id": f"EV-{i:07d}", "sensor_id": sensor,
          "timestamp": (start + dt.timedelta(minutes=i * 3)).isoformat(),
          "pressure_bar": round(rng.uniform(3.0, 5.0) - (1.8 if abnormal else 0), 3),
          "flow_lpm": round(rng.uniform(80, 110) - (50 if abnormal else 0), 3),
          "temperature_c": round(rng.uniform(18, 27), 2)})
    return records

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='data/events.jsonl')
    parser.add_argument('--count', type=int, default=2000)
    a = parser.parse_args()
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, 'w', encoding='utf-8') as f:
        for row in generate(a.count):
            f.write(json.dumps(row) + '\n')
    print('Generated', a.count, 'events in', a.out)
