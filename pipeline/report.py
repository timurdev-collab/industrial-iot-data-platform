import argparse, sqlite3

def report(db):
    with sqlite3.connect(db) as con:
        for title, query in [
            ('Raw events','SELECT COUNT(*) FROM raw_events'),
            ('Sensors','SELECT COUNT(*) FROM dim_sensor'),
            ('Hourly fact rows','SELECT COUNT(*) FROM fact_sensor_hourly'),
            ('Anomaly flags','SELECT COALESCE(SUM(anomaly_count),0) FROM fact_sensor_hourly')
        ]:
            print(f'{title}: {con.execute(query).fetchone()[0]}')

if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--db', default='data/telemetry.db')
    report(a.parse_args().db)
