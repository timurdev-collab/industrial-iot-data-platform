"""Reproducible local performance smoke benchmark, not a cloud throughput claim."""
import json, tempfile, time
from pathlib import Path
from pipeline.generate import generate
from pipeline.load import load

def run(count=10000):
    with tempfile.TemporaryDirectory() as tmp:
        data=Path(tmp)/'events.jsonl'
        db=Path(tmp)/'telemetry.db'
        with data.open('w') as f:
            for record in generate(count):
                f.write(json.dumps(record)+'\n')
        start=time.perf_counter()
        stats=load(data,db)
        elapsed=time.perf_counter()-start
        print(json.dumps({'rows':stats['inserted'],'seconds':round(elapsed,3),
            'rows_per_second':round(stats['inserted']/elapsed,1) if elapsed else None,
            'environment':'local','note':'Results vary by hardware'}))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--count',type=int,default=10000)
    run(p.parse_args().count)
