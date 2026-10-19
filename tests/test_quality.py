import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from pipeline.generate import generate
from pipeline.load import load
from pipeline.quality import check

class WarehouseQualityTests(unittest.TestCase):
    def test_clean_warehouse_passes_and_corruption_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "events.jsonl"
            db = Path(folder) / "warehouse.db"
            source.write_text("".join(json.dumps(r) + "\n" for r in generate(100)), encoding="utf-8")
            load(source, db)
            self.assertTrue(check(db)["passed"])
            with sqlite3.connect(db) as con:
                con.execute("UPDATE fact_sensor_hourly SET event_count = event_count + 1 WHERE rowid = 1")
                con.commit()
            result = check(db)
            self.assertFalse(result["passed"])
            self.assertGreater(result["violations"]["fact_counts_match_raw"], 0)

if __name__ == "__main__":
    unittest.main()
